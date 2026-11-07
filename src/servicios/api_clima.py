"""Consulta clima actual en Open-Meteo; no requiere clave API."""
import math
import re

def validar_ciudad(ciudad):
    if not isinstance(ciudad, str):
        raise ValueError("Ciudad invalida.")
    ciudad = ciudad.strip()
    if not 2 <= len(ciudad) <= 80 or not re.fullmatch(r"[\wÀ-ÿ .'-]+", ciudad, re.UNICODE):
        raise ValueError("Ingrese una ciudad valida (2 a 80 caracteres).")
    return ciudad

CIUDADES = [
    ("Antofagasta", -23.6509, -70.3975),
    ("Santiago", -33.4489, -70.6693),
    ("Coquimbo", -29.9533, -71.3395),
    ("Concepción", -36.8269, -73.0498),
]

def consultar(ciudad, sesion_http=None):
    ciudad = validar_ciudad(ciudad)
    ubicacion = next(((nombre, lat, lon) for nombre, lat, lon in CIUDADES if nombre.casefold() == ciudad.casefold()), None)
    if ubicacion is None:
        raise ValueError("Seleccione una ciudad del listado.")
    try:
        import requests
    except ImportError as error:
        raise RuntimeError("Instale requests.") from error
    cliente = sesion_http or requests
    try:
        respuesta = cliente.get("https://api.open-meteo.com/v1/forecast",
            params={"latitude": ubicacion[1], "longitude": ubicacion[2],
                    "current": "temperature_2m,relative_humidity_2m,weather_code",
                    "timezone": "America/Santiago"}, timeout=(3, 5))
        respuesta.raise_for_status()
        actual = respuesta.json()["current"]
        temperatura = float(actual["temperature_2m"])
        humedad = float(actual["relative_humidity_2m"])
        codigo = int(actual["weather_code"])
        if not math.isfinite(temperatura) or not 0 <= humedad <= 100 or not 0 <= codigo <= 99:
            raise ValueError("Datos climaticos invalidos.")
        return {"ciudad": ubicacion[0], "pais": "Chile", "temperatura": temperatura,
                "humedad": humedad, "codigo": codigo, "fecha": actual["time"], "origen": "Open-Meteo"}
    except (requests.Timeout, requests.ConnectionError) as error:
        raise RuntimeError("No hay conexion con el servicio del clima.") from error
    except (requests.HTTPError, KeyError, TypeError, ValueError, IndexError) as error:
        raise RuntimeError("No se pudo obtener un clima valido para esa ciudad.") from error
