from complementos.complementos import limpiar_pantalla
"""Menu de autoservicio del empleado autenticado."""
from servicios.mi_cuenta import consultar_ficha, actualizar_mis_datos, consultar_mis_registros


def menu_mis_datos(sesion):
    if not sesion or sesion.get("rol") != "empleado":
        print("Acceso restringido a empleados.")
        input("Presione Enter para continuar...")
        return
    while True:
        limpiar_pantalla()
        print("\n===== MIS DATOS =====")
        print("1. Consultar mi ficha")
        print("2. Modificar mi nombre y correo")
        print("3. Consultar mis registros de tiempo")
        print("0. Volver")
        opcion = input("Seleccione una opcion: ").strip()
        if opcion == "0":
            return
        try:
            if opcion == "1":
                ficha = consultar_ficha(sesion)
                if ficha is None:
                    print("No se encontro la ficha asociada a su cuenta.")
                else:
                    etiquetas = ("ID", "Nombre", "Direccion", "Telefono", "Correo", "Fecha de contrato", "Salario", "Cargo")
                    for etiqueta, valor in zip(etiquetas, ficha):
                        print(f"{etiqueta}: {valor}")
            elif opcion == "2":
                ficha = consultar_ficha(sesion)
                if ficha is None:
                    print("No se encontro la ficha asociada a su cuenta.")
                else:
                    print("Solo puede modificar su nombre y correo.")
                    nombre = input("Nuevo nombre: ")
                    correo = input("Nuevo correo: ")
                    actualizar_mis_datos(sesion, nombre, correo)
                    print("Datos actualizados correctamente.")
            elif opcion == "3":
                registros = consultar_mis_registros(sesion)
                if not registros:
                    print("No tiene registros de tiempo.")
                for identificador, fecha, horas, descripcion, proyecto in registros:
                    print(f"#{identificador} | {fecha} | {horas} horas | {proyecto} | {descripcion}")
            else:
                print("Opcion no valida.")
        except (ValueError, TypeError, PermissionError) as error:
            print("No se pudo completar la operacion:", error)
        except Exception:
            print("Ocurrio un error al consultar o guardar los datos.")
        input("Presione Enter para continuar...")
