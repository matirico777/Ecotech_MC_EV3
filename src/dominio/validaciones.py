import re
from datetime import date, datetime
from math import isfinite


def texto_obligatorio(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{campo} no puede estar vacio.")
    return valor.strip()


def fecha_valida(valor, campo, permitir_futura=True):
    if isinstance(valor, datetime):
        valor = valor.date()
    elif isinstance(valor, str):
        try:
            valor = date.fromisoformat(valor)
        except ValueError:
            raise ValueError(f"{campo} debe tener formato AAAA-MM-DD.") from None
    if not isinstance(valor, date):
        raise ValueError(f"{campo} no es valida.")
    if not permitir_futura and valor > date.today():
        raise ValueError(f"{campo} no puede ser futura.")
    return valor


def numero_positivo(valor, campo, maximo=None):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not isfinite(valor) or valor <= 0:
        raise ValueError(f"{campo} debe ser un numero mayor que cero.")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{campo} no puede superar {maximo}.")
    return valor


def correo_valido(valor):
    valor = texto_obligatorio(valor, "El correo")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
        raise ValueError("El correo electronico no es valido.")
    return valor
