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
    """
    Inserta un nuevo registro en la tabla 'registros'.
    """
    # ✅ CORRECTION: The SQL command is now complete.
    sql = ''' INSERT INTO registros(
        timestamp, edad, duracion_ciclo, imc, tiene_sop, 
        grado_endometriosis, tiene_miomas, mioma_submucoso, 
        mioma_submucoso_multiple, mioma_intramural_significativo, 
        mioma_subseroso_grande, tipo_adenomiosis, tipo_polipo, 
        resultado_hsg, amh, prolactina, tsh, tpo_ab_positivo, 
        insulina_ayunas, glicemia_ayunas, volumen_seminal, 
        concentracion_esperm, motilidad_progresiva, morfologia_normal, 
        vitalidad_esperm, pronostico_final, tema
    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''' # 27 placeholders

    try:
        cursor = conn.cursor()
        cursor.execute(sql, registro_data)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error detallado al insertar registro: {e}")
        raise e

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