# pages/04_RiesgoAborto.py

import streamlit as st
from calculadora_riesgo_aborto import CalculadoraRiesgoAborto

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
    st.subheader(f"{resultado['color']} {resultado['categoria']}")
    st.metric(label="Riesgo Estimado de Aborto", value=f"{resultado['riesgo_final']} %")
    st.info(resultado['mensaje'])
