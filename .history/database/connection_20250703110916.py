# En: database/connection.py
import sqlite3
import os

def _crear_tabla_registros(conn):
    sql = """ CREATE TABLE IF NOT EXISTS registros (id INTEGER PRIMARY KEY, timestamp TEXT, ...); """ # Tu SQL completo aquí
    conn.cursor().execute(sql)

def _crear_tabla_riesgo_aborto(conn):
    sql = """ CREATE TABLE IF NOT EXISTS riesgo_aborto (id INTEGER PRIMARY KEY, ...); """ # Tu SQL completo aquí
    conn.cursor().execute(sql)

def _crear_tabla_logros(conn):
    sql = """ CREATE TABLE IF NOT EXISTS logros (id INTEGER PRIMARY KEY, ...); """ # Tu SQL completo aquí
    conn.cursor().execute(sql)

def crear_conexion_y_tablas(db_file="fertilidad.db"):
    """
    Crea una conexión a la base de datos y asegura que todas las tablas existan.
    """
    conn = sqlite3.connect(db_file)
    _crear_tabla_registros(conn)
    _crear_tabla_riesgo_aborto(conn)
    _crear_tabla_logros(conn)
    # La inicialización de logros debería ir aquí si es parte de la configuración inicial
    # from .logros_crud import inicializar_logros
    # inicializar_logros(conn)
    conn.commit()
    return conn