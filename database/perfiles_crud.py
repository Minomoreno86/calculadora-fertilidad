# En: database/perfiles_crud.py
import pandas as pd
from datetime import datetime
import streamlit as st


def preparar_registro_db(evaluacion):
    """
    Toma un objeto de evaluación y lo transforma en una tupla de 27 elementos,
    lista para ser insertada en la base de datos.
    """
    try:
        pronostico_num = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
    except:
        pronostico_num = 0.0

    # Construye la tupla con todos los datos en el orden correcto para la BBDD
    registro_tuple = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        evaluacion.edad,
        evaluacion.duracion_ciclo,
        round(evaluacion.imc, 2) if evaluacion.imc is not None else None,
        1 if evaluacion.tiene_sop else 0,
        evaluacion.grado_endometriosis,
        1 if evaluacion.tiene_miomas else 0,
        1 if getattr(evaluacion, 'mioma_submucoso', False) else 0,
        0, # mioma_submucoso_multiple no está en el modelo, se asume 0
        1 if getattr(evaluacion, 'mioma_intramural_significativo', False) else 0,
        1 if getattr(evaluacion, 'mioma_subseroso_grande', False) else 0,
        evaluacion.tipo_adenomiosis,
        evaluacion.tipo_polipo,
        evaluacion.resultado_hsg,
        evaluacion.amh,
        evaluacion.prolactina,
        evaluacion.tsh,
        1 if evaluacion.tpo_ab_positivo else 0,
        evaluacion.insulina_ayunas,
        evaluacion.glicemia_ayunas,
        evaluacion.volumen_seminal,
        evaluacion.concentracion_esperm,
        evaluacion.motilidad_progresiva,
        evaluacion.morfologia_normal,
        evaluacion.vitalidad_esperm,
        pronostico_num,
        st.session_state.get('tema', 'light')
    )
    return registro_tuple

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