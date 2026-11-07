from servicios import api_dolar
from datetime import datetime
from zoneinfo import ZoneInfo
from persistencia import indicador_dao

def consultar_y_guardar(sesion):
    if not sesion:
        raise PermissionError("Debe iniciar sesion.")
    try:
        indicador = api_dolar.consultar()
        indicador_dao.guardar(indicador)
        return {"fecha": indicador.fecha, "valor": indicador.valor,
                "unidad": indicador.unidad, "origen": "API (guardado en SQLite)", "actualizado_hoy": True}
    except RuntimeError:
        respaldo = indicador_dao.ultimo()
        if respaldo:
            fecha, valor, unidad, fuente = respaldo
            hoy = datetime.now(ZoneInfo("America/Santiago")).date().isoformat()
            return {"fecha": fecha, "valor": valor, "unidad": unidad,
                    "origen": "SQLite (respaldo, NO actualizado hoy)" if fecha != hoy else "SQLite (guardado hoy; sin conexion)",
                    "actualizado_hoy": fecha == hoy}
        raise
