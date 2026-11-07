from persistencia.conexion import abrir_conexion
from dominio.indicador import Indicador

def preparar():
    with abrir_conexion() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS indicador (
            fuente TEXT NOT NULL, codigo TEXT NOT NULL, fecha TEXT NOT NULL,
            valor REAL NOT NULL CHECK(valor > 0), unidad TEXT NOT NULL,
            PRIMARY KEY(fuente,codigo,fecha))""")

def guardar(indicador):
    with abrir_conexion() as con:
        con.execute("""INSERT INTO indicador(fuente,codigo,fecha,valor,unidad)
            VALUES(?,?,?,?,?) ON CONFLICT(fuente,codigo,fecha)
            DO UPDATE SET valor=excluded.valor, unidad=excluded.unidad""",
            (indicador.fuente,"dolar",indicador.fecha,indicador.valor,indicador.unidad))

def historial(limite=10):
    with abrir_conexion() as con:
        return con.execute("SELECT fecha,valor,unidad,fuente FROM indicador WHERE codigo=? ORDER BY fecha DESC LIMIT ?", ("dolar", limite)).fetchall()

def ultimo():
    filas = historial(1)
    return filas[0] if filas else None
