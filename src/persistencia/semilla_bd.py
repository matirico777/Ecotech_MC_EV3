from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from persistencia.crear_bd import crear_tablas
from persistencia.conexion import abrir_conexion, obtener_motor
from servicios.autenticacion import preparar_cuentas, registrar, pedir_clave_confirmada
from persistencia.indicador_dao import preparar as preparar_indicadores


def cargar_semillas():
    if obtener_motor() != "sqlite":
        raise RuntimeError("Esta semilla esta preparada para SQLite.")
    crear_tablas()
    preparar_cuentas()
    preparar_indicadores()

    hoy = datetime.now(ZoneInfo("America/Santiago")).date()
    departamentos = [
        ("Soporte Tecnico", 0), ("Desarrollo", 1), ("Redes", 2),
        ("Seguridad", 3), ("Administracion", 4)
    ]
    empleados = [
        ("Ana Torres", "Av. Central 101", "912345601", "ana.torres@ecotech.example", hoy.isoformat(), 850000, "Soporte"),
        ("Bruno Diaz", "Calle Norte 202", "912345602", "bruno.diaz@ecotech.example", hoy.isoformat(), 920000, "Desarrollador"),
        ("Camila Rojas", "Calle Sur 303", "912345603", "camila.rojas@ecotech.example", hoy.isoformat(), 950000, "Redes"),
        ("Diego Perez", "Av. Oriente 404", "912345604", "diego.perez@ecotech.example", hoy.isoformat(), 990000, "Seguridad"),
        ("Elena Soto", "Av. Poniente 505", "912345605", "elena.soto@ecotech.example", hoy.isoformat(), 880000, "Administracion"),
        ("Patricia Admin", "Av. Principal 606", "912345606", "patricia.admin@ecotech.example", hoy.isoformat(), 1200000, "Jefatura")
    ]
    proyectos = [
        ("Mesa de ayuda", hoy.isoformat(), "Atencion a usuarios"),
        ("Portal interno", hoy.isoformat(), "Desarrollo de portal"),
        ("Red corporativa", hoy.isoformat(), "Configuracion de red"),
        ("Auditoria de acceso", hoy.isoformat(), "Revision de seguridad"),
        ("Inventario digital", hoy.isoformat(), "Control de equipos")
    ]
    with abrir_conexion() as con:
        for nombre, _ in departamentos:
            if not con.execute("SELECT 1 FROM departamento WHERE nombre=?", (nombre,)).fetchone():
                con.execute("INSERT INTO departamento(nombre,id_gerente) VALUES(?,NULL)", (nombre,))
        for fila in empleados:
            if not con.execute("SELECT 1 FROM empleado WHERE correo=?", (fila[3],)).fetchone():
                con.execute("INSERT INTO empleado(nombre,direccion,numero,correo,fecha_contrato,salario,cargo) VALUES(?,?,?,?,?,?,?)", fila)
        for fila in proyectos:
            if not con.execute("SELECT 1 FROM proyecto WHERE nombre=?", (fila[0],)).fetchone():
                con.execute("INSERT INTO proyecto(nombre,fecha_inicio,descripcion) VALUES(?,?,?)", fila)
        ids_emp = [con.execute("SELECT id FROM empleado WHERE correo=?", (e[3],)).fetchone()[0] for e in empleados]
        ids_dep = [con.execute("SELECT id FROM departamento WHERE nombre=?", (d[0],)).fetchone()[0] for d in departamentos]
        ids_pro = [con.execute("SELECT id FROM proyecto WHERE nombre=?", (pr[0],)).fetchone()[0] for pr in proyectos]
        for i in range(5):
            con.execute("UPDATE departamento SET id_gerente=? WHERE id=? AND id_gerente IS NULL", (ids_emp[i],ids_dep[i]))
            con.execute("INSERT OR IGNORE INTO departamento_empleado(departamento_id,empleado_id) VALUES(?,?)", (ids_dep[i],ids_emp[i]))
            con.execute("INSERT OR IGNORE INTO departamento_proyecto(departamento_id,proyecto_id) VALUES(?,?)", (ids_dep[i],ids_pro[i]))
            con.execute("INSERT OR IGNORE INTO proyecto_empleado(proyecto_id,empleado_id) VALUES(?,?)", (ids_pro[i],ids_emp[i]))
            fecha=(hoy-timedelta(days=i)).isoformat()
            descripcion=f"Trabajo de prueba {i+1}"
            if not con.execute("SELECT 1 FROM registro_tiempo WHERE empleado_id=? AND proyecto_id=? AND fecha_trabajada=? AND descripcion_tarea=?", (ids_emp[i],ids_pro[i],fecha,descripcion)).fetchone():
                con.execute("INSERT INTO registro_tiempo(horas_trabajadas,fecha_trabajada,descripcion_tarea,empleado_id,proyecto_id) VALUES(?,?,?,?,?)", (i+3,fecha,descripcion,ids_emp[i],ids_pro[i]))
        con.commit()

    cuentas = [("ana_torres",ids_emp[0]),("bruno_diaz",ids_emp[1]),("camila_rojas",ids_emp[2]),("diego_perez",ids_emp[3]),("elena_soto",ids_emp[4])]
    with abrir_conexion() as con:
        pendientes = [(nombre,identificador) for nombre,identificador in cuentas if not con.execute("SELECT 1 FROM usuario_acceso WHERE nombre_usuario=? OR empleado_id=?", (nombre,identificador)).fetchone()]
    if pendientes:
        print("Se crearan",len(pendientes),"cuentas de empleado. Elija una contrasena de prueba para estas cuentas.")
        clave = pedir_clave_confirmada()
        for nombre,identificador in pendientes:
            registrar(nombre,clave,identificador,"empleado")
    with abrir_conexion() as con:
        admins = con.execute("SELECT COUNT(*) FROM usuario_acceso WHERE rol='admin'").fetchone()[0]
    if admins:
        with abrir_conexion() as con:
            con.execute("UPDATE usuario_acceso SET empleado_id=? WHERE rol='admin' AND empleado_id IS NULL AND NOT EXISTS (SELECT 1 FROM usuario_acceso WHERE empleado_id=?)", (ids_emp[5],ids_emp[5]))
            con.commit()
    if not admins:
        print("Se necesita una cuenta administradora vinculada a un empleado, segun Clase 3.")
        while True:
            nombre = input("Nombre del usuario administrador: ").strip().lower()
            if not 3 <= len(nombre) <= 40 or not all(c.isascii() and (c.isalnum() or c == "_") for c in nombre):
                print("Nombre de acceso no valido.")
                continue
            with abrir_conexion() as con:
                existe = con.execute("SELECT 1 FROM usuario_acceso WHERE nombre_usuario=?", (nombre,)).fetchone()
            if existe:
                print("El usuario ya existe. Pruebe otro.")
                continue
            clave = pedir_clave_confirmada()
            registrar(nombre,clave,ids_emp[5],"admin")
            break
    print("Semillas listas con fechas relativas a hoy en Chile:", hoy.isoformat())
    print("No se inventaron valores del dolar: estos se obtienen exclusivamente de la API.")
    print("Puede ejecutar el script nuevamente sin duplicar datos.")


if __name__ == "__main__":
    cargar_semillas()
