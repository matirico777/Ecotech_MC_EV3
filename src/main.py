from dominio.Gestion_departamento import GestionDepartamento
from dominio.gestionPermisos import GestionPermisos
from persistencia.crear_bd import crear_tablas
from menus.menu_dominio_empleado import menu_dominio_empleado
from menus.menu_dominio_departamento import menu_dominio_departamento
from menus.menu_dominio_proyecto import menu_dominio_proyecto
from menus.menu_dominio_registroTiempo import menu_dominio_registro_tiempo
from menus.menu_dominio_usuario import menu_dominio_usuario
from menus.menu_dominio_gestionPermisos import menu_dominio_gestionPermisos
from menus.menu_dominio_gestionDepartamento import menu_dominio_gestionDepartamento
from complementos.complementos import limpiar_pantalla
from getpass import getpass
from servicios.autenticacion import preparar_cuentas, crear_admin_inicial, autenticar, registrar, pedir_clave_confirmada
from persistencia.indicador_dao import preparar as preparar_indicadores
from menus.menu_evaluacion3 import menu_evaluacion3
from menus.menu_mis_datos import menu_mis_datos
from persistencia.conexion import abrir_conexion
import sqlite3

def main():
    preparar_cuentas()
    preparar_indicadores()
    crear_admin_inicial()
    sesion = None
    usuarios = []
    gestion_permisos = GestionPermisos()
    gestion_departamentos = GestionDepartamento()

    while True:
        limpiar_pantalla()
        print("\n===== ECOTECH SOLUTIONS =====")
        print("Sesion:", sesion["usuario"] if sesion else "sin iniciar")
        if sesion is None:
            print("1. Iniciar sesion")
            print("0. Salir")
        elif sesion["rol"] == "admin":
            print("1. Empleado")
            print("2. Departamento")
            print("3. Proyecto")
            print("4. Registro de Tiempo")
            print("5. Usuario")
            print("6. Gestion de Permisos")
            print("7. Gestion de Departamento")
            print("8. Servicios externos (dolar y clima)")
            print("9. Registrar cuenta de empleado")
            print("10. Cerrar sesion")
            print("0. Salir")
        elif sesion["rol"] == "empleado":
            print("8. Servicios externos (dolar y clima)")
            print("9. Mis datos y registros")
            print("10. Cerrar sesion")
            print("0. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "10" or (opcion == "1" and sesion is None):
            if sesion:
                sesion = None
                print("Sesion cerrada.")
            else:
                nombre = input("Usuario: ")
                clave = getpass("Contrasena: ")
                sesion = autenticar(nombre, clave)
                print("Acceso correcto." if sesion else "Credenciales incorrectas.")
            input("Presione Enter para continuar...")
            limpiar_pantalla()
            continue
        if opcion == "0":
            limpiar_pantalla()
            print("Hasta luego.")
            break
        if opcion == "9" and sesion and sesion["rol"] == "admin":
            if not sesion or sesion["rol"] != "admin":
                print("Acceso denegado.")
            else:
                try:
                    nombre = input("Nuevo usuario: ")
                    empleado_id = int(input("ID de empleado existente: "))
                    clave = pedir_clave_confirmada()
                    registrar(nombre, clave, empleado_id)
                    print("Cuenta registrada.")
                except (ValueError, sqlite3.IntegrityError):
                    print("No se pudo registrar: verifique datos, empleado y duplicados.")
            input("Presione Enter para continuar...")
            limpiar_pantalla()
            continue
        if opcion == "9" and sesion and sesion["rol"] == "empleado":
            if sesion and sesion["rol"] == "empleado":
                menu_mis_datos(sesion)
                limpiar_pantalla()
            else:
                print("Acceso restringido a empleados.")
                input("Presione Enter para continuar...")
            limpiar_pantalla()
            continue
        if opcion == "8":
            if sesion:
                menu_evaluacion3(sesion)
                limpiar_pantalla()
            else:
                print("Debe iniciar sesion.")
                input("Presione Enter para continuar...")
            limpiar_pantalla()
            continue
        if opcion in ("1", "2", "3", "4", "5", "6", "7") and (not sesion or sesion["rol"] != "admin"):
            print("Acceso restringido al administrador.")
            input("Presione Enter para continuar...")
            limpiar_pantalla()
            continue
        if opcion == "1":
            limpiar_pantalla()
            menu_dominio_empleado()
        elif opcion == "2":
            limpiar_pantalla()
            menu_dominio_departamento()
        elif opcion == "3":
            limpiar_pantalla()
            menu_dominio_proyecto()
        elif opcion == "4":
            limpiar_pantalla()
            menu_dominio_registro_tiempo()
        elif opcion == "5":
            limpiar_pantalla()
            menu_dominio_usuario(usuarios)
        elif opcion == "6":
            limpiar_pantalla()
            menu_dominio_gestionPermisos(usuarios, gestion_permisos)
        elif opcion == "7":
            limpiar_pantalla()
            menu_dominio_gestionDepartamento(gestion_departamentos)
        else:
            print("Opcion no valida.")
            input("Presione Enter para continuar...")
            limpiar_pantalla()

if __name__ == "__main__":
    try:
        crear_tablas()
    except Exception as error:
        print("Error al preparar la base de datos:", error)
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("\nPrograma interrumpido por el usuario.")
        except EOFError:
            print("\nEntrada finalizada. Cerrando programa.")
