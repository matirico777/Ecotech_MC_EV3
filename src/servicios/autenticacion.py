"""Acceso persistente y sesiones, sin guardar claves en texto plano."""
import hashlib
import hmac
import secrets
import sqlite3
from persistencia.conexion import abrir_conexion

ROLES = ("admin", "empleado")

def crear_hash(clave):
    if not isinstance(clave, str) or len(clave) < 8:
        raise ValueError("La contrasena debe tener al menos 8 caracteres.")
    sal = secrets.token_bytes(16)
    resultado = hashlib.pbkdf2_hmac("sha256", clave.encode(), sal, 600000)
    return sal.hex() + ":" + resultado.hex()

def verificar_clave(clave, almacenado):
    try:
        sal_hex, hash_hex = almacenado.split(":")
        resultado = hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(sal_hex), 600000)
        return hmac.compare_digest(resultado, bytes.fromhex(hash_hex))
    except (ValueError, AttributeError, TypeError):
        return False

def preparar_cuentas():
    with abrir_conexion() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS usuario_acceso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            empleado_id INTEGER UNIQUE,
            rol TEXT NOT NULL CHECK(rol IN ('admin','empleado')),
            FOREIGN KEY(empleado_id) REFERENCES empleado(id))""")

def registrar(nombre, clave, empleado_id, rol="empleado"):
    nombre = nombre.strip().lower()
    if not 3 <= len(nombre) <= 40 or not all(c.isascii() and (c.isalnum() or c == "_") for c in nombre):
        raise ValueError("Usuario: 3 a 40 caracteres, letras, numeros o guion bajo.")
    if rol not in ROLES:
        raise ValueError("Rol no permitido.")
    if rol == "empleado" and (type(empleado_id) is not int or empleado_id <= 0):
        raise ValueError("Se necesita un empleado existente.")
    with abrir_conexion() as con:
        con.execute("INSERT INTO usuario_acceso (nombre_usuario,password_hash,empleado_id,rol) VALUES (?,?,?,?)",
                    (nombre, crear_hash(clave), empleado_id, rol))

def autenticar(nombre, clave):
    if not isinstance(nombre, str) or not isinstance(clave, str) or not nombre.strip() or not clave:
        return None
    with abrir_conexion() as con:
        fila = con.execute("SELECT id,nombre_usuario,password_hash,empleado_id,rol FROM usuario_acceso WHERE nombre_usuario=?",
                           (nombre.strip().lower(),)).fetchone()
    if fila and verificar_clave(clave, fila[2]):
        return {"id":fila[0], "usuario":fila[1], "empleado_id":fila[3], "rol":fila[4]}
    return None

def requiere_rol(sesion, rol):
    if not sesion or sesion.get("rol") != rol:
        raise PermissionError("No tiene permisos para esta operacion.")

def pedir_clave_confirmada():
    from getpass import getpass
    while True:
        try:
            clave = getpass("Contrasena (minimo 8 caracteres): ")
            if len(clave) < 8:
                raise ValueError("La contrasena debe tener al menos 8 caracteres.")
            while True:
                repetida = getpass("Repita la contrasena: ")
                if clave == repetida:
                    return clave
                print("Las contrasenas no coinciden. Repita solo la confirmacion.")
        except ValueError as error:
            print(error)


def crear_admin_inicial():
    with abrir_conexion() as con:
        cantidad = con.execute("SELECT COUNT(*) FROM usuario_acceso WHERE rol = 'admin'").fetchone()[0]
    if cantidad:
        return
    print("Primera ejecucion: cree una cuenta administradora.")
    while True:
        nombre = input("Nombre de administrador: ").strip()
        if not 3 <= len(nombre) <= 40 or not all(c.isascii() and (c.isalnum() or c == "_") for c in nombre):
            print("Usuario: 3 a 40 caracteres, letras, numeros o guion bajo.")
            continue
        with abrir_conexion() as con:
            existente = con.execute("SELECT 1 FROM usuario_acceso WHERE nombre_usuario=?", (nombre.lower(),)).fetchone()
        if existente:
            print("Ese usuario ya existe. Escriba otro nombre.")
            continue
        clave = pedir_clave_confirmada()
        try:
            registrar(nombre, clave, None, "admin")
            print("Administrador creado correctamente.")
            return
        except (ValueError, sqlite3.IntegrityError) as error:
            print("No se pudo crear el administrador:", error)
