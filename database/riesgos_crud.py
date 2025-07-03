# En: database/riesgos_crud.py
import pandas as pd

def insertar_riesgo_aborto(conn, datos):
    """
    Inserta un nuevo registro en la tabla 'riesgo_aborto'.
    La sentencia SQL ahora está completa y correcta.
    """
    sql = ''' INSERT INTO riesgo_aborto(
        timestamp, edad, imc, abortos_previos, tiene_miomas, tiene_adenomiosis,
        tiene_sop, tiene_diabetes, tiene_tiroides, prolactina_alta, 
        infecciones_previas, calidad_semen_alterada, riesgo_final, categoria
    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''' # <-- 14 columnas y 14 '?'

    try:
        cursor = conn.cursor()
        # 'datos' debe ser una tupla con exactamente 14 elementos
        cursor.execute(sql, datos)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error detallado al insertar riesgo: {e}")
        raise e

def leer_todos_los_riesgos(conn):
    return pd.read_sql_query("SELECT * FROM riesgo_aborto", conn)