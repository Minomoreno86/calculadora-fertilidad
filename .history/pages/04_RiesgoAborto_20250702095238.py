# pages/04_RiesgoAborto.py

import streamlit as st
from calculadora_riesgo_aborto import CalculadoraRiesgoAborto
import sqlite3
from db_manager import crear_conexion, insertar_riesgo_aborto
from datetime import datetime

def crear_conexion(db_file):
    """Crea una conexión a la base de datos SQLite especificada por db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def insertar_riesgo_aborto(conn, datos):
    """
    Inserta una nueva evaluación de riesgo de aborto en la base de datos.
    """
    sql = ''' INSERT INTO riesgo_aborto(
    timestamp, edad, imc, abortos_previos, tiene_miomas, tiene_adenomiosis,
    tiene_sop, tiene_diabetes, tiene_tiroides, prolactina_alta, infecciones_previas,
    calidad_semen_alterada, riesgo_final, categoria
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, datos)
    conn.commit()

st.set_page_config(page_title="Calculadora de Riesgo de Aborto", page_icon="⚠️", layout="wide")
st.title("⚠️ Calculadora Predictiva de Riesgo de Aborto")

edad = st.number_input("Edad materna", min_value=18, max_value=55, value=30)
imc = st.number_input("IMC", min_value=15.0, max_value=50.0, value=22.0, step=0.1)
abortos_previos = st.number_input("Número de abortos previos", min_value=0, max_value=5, value=0)
tiene_miomas = st.toggle("Diagnóstico de miomas uterinos")
tiene_adenomiosis = st.toggle("Diagnóstico de adenomiosis")
tiene_sop = st.toggle("Diagnóstico de SOP")
tiene_diabetes = st.toggle("Antecedentes de diabetes")
tiene_tiroides = st.toggle("Antecedentes de hipotiroidismo o hipertiroidismo")
prolactina_alta = st.toggle("Prolactina alta en controles previos")
infecciones_previas = st.toggle("Infecciones previas en el útero (ej. endometritis)")
calidad_semen_alterada = st.toggle("Calidad espermática alterada")

if st.button("Calcular Riesgo"):
    calculadora = CalculadoraRiesgoAborto(
        edad=edad, imc=imc, abortos_previos=abortos_previos,
        tiene_miomas=tiene_miomas, tiene_adenomiosis=tiene_adenomiosis, tiene_sop=tiene_sop,
        tiene_diabetes=tiene_diabetes, tiene_tiroides=tiene_tiroides,
        prolactina_alta=prolactina_alta, infecciones_previas=infecciones_previas,
        calidad_semen_alterada=calidad_semen_alterada
    )
    resultado = calculadora.calcular_riesgo()

    # 👇 Guardamos en session_state
    st.session_state.riesgo_aborto_resultado = resultado
    st.session_state.riesgo_aborto_datos = {
        "edad": edad,
        "imc": imc,
        "abortos_previos": abortos_previos,
        "tiene_miomas": tiene_miomas,
        "tiene_adenomiosis": tiene_adenomiosis,
        "tiene_sop": tiene_sop,
        "tiene_diabetes": tiene_diabetes,
        "tiene_tiroides": tiene_tiroides,
        "prolactina_alta": prolactina_alta,
        "infecciones_previas": infecciones_previas,
        "calidad_semen_alterada": calidad_semen_alterada
    }

    st.subheader(f"{resultado['color']} {resultado['categoria']}")
    st.metric(label="Riesgo Estimado de Aborto", value=f"{resultado['riesgo_final']} %")
    st.info(resultado['mensaje'])
if st.button("Guardar Evaluación de Riesgo"):
    if 'riesgo_aborto_resultado' in st.session_state:
        resultado = st.session_state.riesgo_aborto_resultado
        datos = st.session_state.riesgo_aborto_datos

        conn = crear_conexion("fertilidad.db")
        if conn is not None:
            try:
                datos_registro = (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datos['edad'], datos['imc'], datos['abortos_previos'], 
                    int(datos['tiene_miomas']), int(datos['tiene_adenomiosis']),
                    int(datos['tiene_sop']), int(datos['tiene_diabetes']), int(datos['tiene_tiroides']),
                    int(datos['prolactina_alta']), int(datos['infecciones_previas']), int(datos['calidad_semen_alterada']),
                    resultado['riesgo_final'], resultado['categoria']
                )
                insertar_riesgo_aborto(conn, datos_registro)
                st.toast('¡Evaluación guardada con éxito!', icon='✅')
                conn.close()
            except Exception as e:
                st.error(f"Error al guardar: {e}")
                conn.close()
    else:
        st.warning("⚠️ Primero debes calcular el riesgo antes de poder guardarlo.")