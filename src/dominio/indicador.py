from datetime import date
from math import isfinite

class Indicador:
    def __init__(self, fecha, valor, fuente="mindicador.cl", unidad="CLP/USD"):
        date.fromisoformat(fecha)
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not isfinite(valor) or valor <= 0:
            raise ValueError("Valor del indicador invalido.")
        self.fecha = fecha
        self.valor = float(valor)
        self.fuente = fuente
        self.unidad = unidad
