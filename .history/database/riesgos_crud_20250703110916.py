# En: database/riesgos_crud.py
import pandas as pd

def insertar_riesgo_aborto(conn, datos):
    sql = ''' INSERT INTO riesgo_aborto(...) VALUES(...) ''' # Tu SQL completo aquí
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return cursor.lastrowid

def leer_todos_los_riesgos(conn):
    return pd.read_sql_query("SELECT * FROM riesgo_aborto", conn)