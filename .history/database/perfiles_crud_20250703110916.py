# En: database/perfiles_crud.py
import pandas as pd
from datetime import datetime
import streamlit as st

def preparar_registro_db(evaluacion):
    pronostico_num = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
    return (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        evaluacion.edad, # ... y el resto de tu tupla de datos
        pronostico_num,
        st.session_state.get('tema', 'light')
    )

def insertar_registro(conn, registro_data):
    sql = ''' INSERT INTO registros(...) VALUES(...) ''' # Tu SQL completo aquí
    cursor = conn.cursor()
    cursor.execute(sql, registro_data)
    conn.commit()
    return cursor.lastrowid

def leer_todos_los_registros(conn):
    return pd.read_sql_query("SELECT * FROM registros", conn)

def eliminar_registro_por_id(conn, id):
    sql = 'DELETE FROM registros WHERE id = ?'
    conn.cursor().execute(sql, (id,))
    conn.commit()

def eliminar_todos_los_registros(conn):
    sql = 'DELETE FROM registros'
    conn.cursor().execute(sql)
    conn.commit()