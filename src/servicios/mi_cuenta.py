"""Consultas y cambios limitados a la cuenta autenticada."""
from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.empleado import Empleado


def _empleado_id(sesion):
    if not isinstance(sesion, dict) or sesion.get("rol") != "empleado":
        raise PermissionError("Debe iniciar sesion como empleado.")
    identificador = sesion.get("empleado_id")
    if type(identificador) is not int or identificador <= 0:
        raise PermissionError("La cuenta no tiene un empleado asociado.")
    return identificador


def consultar_ficha(sesion):
    identificador = _empleado_id(sesion)
    with abrir_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute(f"SELECT id, nombre, direccion, numero, correo, fecha_contrato, salario, cargo FROM empleado WHERE id = {marcador_sql()}", (identificador,))
        return cursor.fetchone()


def actualizar_mis_datos(sesion, nombre, correo):
    identificador = _empleado_id(sesion)
    nombre = Empleado.validar_nombre(nombre) if hasattr(Empleado, "validar_nombre") else nombre
    
    from dominio.validaciones import texto_obligatorio, correo_valido
    nombre = texto_obligatorio(nombre, "El nombre")
    if not 2 <= len(nombre) <= 100:
        raise ValueError("El nombre debe tener entre 2 y 100 caracteres.")
    correo = correo_valido(correo)
    with abrir_conexion() as conexion:
        cursor = conexion.cursor()
        marca = marcador_sql()
        cursor.execute(f"SELECT 1 FROM empleado WHERE LOWER(TRIM(correo)) = LOWER(TRIM({marca})) AND id <> {marca}", (correo, identificador))
        if cursor.fetchone():
            raise ValueError("Ese correo ya esta registrado por otro empleado.")
        cursor.execute(f"UPDATE empleado SET nombre = {marca}, correo = {marca} WHERE id = {marca}", (nombre, correo, identificador))
        if cursor.rowcount != 1:
            raise ValueError("No se encontro la ficha del empleado.")
        conexion.commit()


def consultar_mis_registros(sesion):
    identificador = _empleado_id(sesion)
    with abrir_conexion() as conexion:
        cursor = conexion.cursor()
        cursor.execute(f"""SELECT r.id, r.fecha_trabajada, r.horas_trabajadas,
                            r.descripcion_tarea, p.nombre
                       FROM registro_tiempo r
                       JOIN proyecto p ON p.id = r.proyecto_id
                       WHERE r.empleado_id = {marcador_sql()}
                       ORDER BY r.fecha_trabajada DESC, r.id DESC""", (identificador,))
        return cursor.fetchall()
