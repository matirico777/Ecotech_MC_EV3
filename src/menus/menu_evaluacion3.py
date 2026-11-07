from complementos.complementos import limpiar_pantalla
from servicios import api_clima, indicadores
from servicios.api_dolar import fecha_chile
from persistencia import indicador_dao


def menu_evaluacion3(sesion):
    if not sesion:
        raise PermissionError("Inicie sesion.")

    while True:
        limpiar_pantalla()
        print("\n=== SERVICIOS EXTERNOS ===")
        try:
            print(f"Fecha de hoy en Chile: {fecha_chile().isoformat()}")
        except (ValueError, RuntimeError, OSError, ImportError) as error:
            print(f"No se pudo obtener la fecha de Chile: {error}")

        print("1. Consultar dólar")
        print("2. Historial del dólar")
        print("3. Convertir presupuesto CLP a USD")
        print("4. Consultar clima por ciudad")
        print("0. Volver")

        try:
            opcion = input("Seleccione una opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nVolviendo al menú principal.")
            return

        if opcion == "0":
            return

        try:
            if opcion == "1":
                dato = indicadores.consultar_y_guardar(sesion)
                print(f"Dólar: {dato['valor']:.2f} CLP/USD | Fecha: {dato['fecha']} | Origen: {dato['origen']}")
                if not dato["actualizado_hoy"]:
                    print("Atención: el valor disponible es histórico, no corresponde a hoy.")

            elif opcion == "2":
                filas = indicador_dao.historial()
                if not filas:
                    print("Todavía no hay datos guardados.")
                for fecha, valor, unidad, fuente in filas:
                    print(f"{fecha}: {valor:.2f} {unidad} | {fuente}")

            elif opcion == "3":
                entrada = input("Presupuesto en CLP: ").strip()
                monto = float(entrada)
                if not 0 < monto < 1e15:
                    raise ValueError("Ingrese un monto positivo y válido.")
                dato = indicadores.consultar_y_guardar(sesion)
                if not dato["actualizado_hoy"]:
                    print("No se puede convertir: no hay cotización confirmada de hoy.")
                else:
                    print(f"{monto:.2f} CLP = {monto / dato['valor']:.2f} USD | Fecha: {dato['fecha']}")

            elif opcion == "4":
                print("\n=== CIUDADES DISPONIBLES ===")
                for numero, (ciudad, _, _) in enumerate(api_clima.CIUDADES, 1):
                    print(f"{numero}. {ciudad}")
                print("0. Volver")
                seleccion = input("Seleccione una ciudad: ").strip()
                if seleccion == "0":
                    continue
                try:
                    numero = int(seleccion)
                except ValueError:
                    print("Error: ingrese un número del listado.")
                    input("Presione Enter para continuar...")
                    continue
                if not 1 <= numero <= len(api_clima.CIUDADES):
                    print("Error: seleccione una ciudad del listado.")
                    input("Presione Enter para continuar...")
                    continue
                ciudad = api_clima.CIUDADES[numero - 1][0]
                dato = api_clima.consultar(ciudad)
                print(f"Ciudad: {dato['ciudad']}, {dato['pais']}")
                print(f"Fecha y hora de medición: {dato['fecha']}")
                print(f"Temperatura: {dato['temperatura']} °C")
                print(f"Humedad: {dato['humedad']}%")
                print(f"Código del clima: {dato['codigo']}")

            else:
                print("Opción inválida. Intente nuevamente.")

        except ValueError as error:
            print(f"Error de dato ingresado: {error}")
        except (RuntimeError, ConnectionError, TimeoutError, OSError) as error:
            print(f"Error al consultar el servicio: {error}")
        except (KeyError, TypeError, ZeroDivisionError, OverflowError) as error:
            print(f"No se pudo procesar la respuesta: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada. Volviendo al menú principal.")
            return

        input("Presione Enter para continuar...")
