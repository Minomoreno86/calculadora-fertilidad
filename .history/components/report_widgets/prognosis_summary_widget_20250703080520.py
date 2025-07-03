import streamlit as st

def render_prognosis_summary(evaluacion):
    st.header("📋 Análisis Detallado del Informe")
    st.subheader(f"1. {evaluacion.pronostico_emoji} Tu Pronóstico General es: **{evaluacion.pronostico_categoria}**")
    if evaluacion.pronostico_categoria == "BUENO": st.success(evaluacion.pronostico_frase)
    elif evaluacion.pronostico_categoria == "MODERADO": st.warning(evaluacion.pronostico_frase)
    else: st.error(evaluacion.pronostico_frase)
    st.metric(label="PROBABILIDAD AJUSTADA DE CONCEPCIÓN POR CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")
    if evaluacion.benchmark_frase: st.info(f"💡 **Contexto Poblacional:** {evaluacion.benchmark_frase}")