"""API de mindicador.cl: consulta HTTPS y validacion del JSON."""
from datetime import datetime
from zoneinfo import ZoneInfo
from dominio.indicador import Indicador

URL = "https://mindicador.cl/api/dolar"

def fecha_chile():
    return datetime.now(ZoneInfo("America/Santiago")).date()

def deserializar(datos):
    if not isinstance(datos, dict) or datos.get("codigo") != "dolar":
        raise ValueError("Respuesta de dolar no valida.")
    serie = datos.get("serie")
    if not isinstance(serie, list) or not serie or not isinstance(serie[0], dict):
        raise ValueError("La API no entrego registros.")
    fecha = datetime.fromisoformat(serie[0]["fecha"].replace("Z", "+00:00")).date().isoformat()
    if fecha != fecha_chile().isoformat():
        raise ValueError(f"El dolar disponible corresponde a {fecha}, no al dia de hoy. No se presentara como actualizado.")
    return Indicador(fecha, serie[0]["valor"])

def consultar(sesion_http=None):
    try:
        import requests
    except ImportError as error:
        raise RuntimeError("Instale requests: python -m pip install -r requirements.txt") from error
    cliente = sesion_http or requests
    try:
        respuesta = cliente.get(URL, timeout=(3, 5))
        respuesta.raise_for_status()
        return deserializar(respuesta.json())
    except (requests.Timeout, requests.ConnectionError) as error:
        raise RuntimeError("No fue posible conectar con el servicio del dolar.") from error
    except (requests.HTTPError, ValueError, KeyError, TypeError) as error:
        raise RuntimeError("La API del dolar no entrego datos utilizables.") from error
