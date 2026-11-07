import os
import sqlite3
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass


def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").strip().lower()


def marcador_sql():
    return "?" if obtener_motor() == "sqlite" else "%s"


def abrir_conexion():
    motor = obtener_motor()
    if motor == "sqlite":
        ruta = Path(os.getenv("DB_NAME", "ecotech.db"))
        if not ruta.is_absolute():
            ruta = Path(__file__).resolve().parents[2] / ruta
        conexion = sqlite3.connect(str(ruta))
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion
    if motor == "mysql":
        try:
            import pymysql
        except ImportError as error:
            raise RuntimeError("Instale PyMySQL para utilizar MySQL.") from error
        return pymysql.connect(host=os.getenv("DB_HOST", "localhost"),
                               port=int(os.getenv("DB_PORT", "3306")),
                               user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
                               database=os.getenv("DB_NAME"), charset="utf8mb4")
    raise ValueError("Motor de base de datos no permitido.")
