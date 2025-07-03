# Contenido completo para: components/report_widgets/pronostico_card.py

import streamlit as st

def render_pronostico_card(evaluacion):
    """
    Muestra la tarjeta completa del pronóstico, incluyendo el medidor visual
    y el resumen detallado.
    """
    st.header("🎯 Tu Pronóstico de Fertilidad")
    
    # --- Parte Visual (del antiguo main_score_widget) ---
    value = evaluacion.pronostico_numerico
    if value < 5: color, performance_text = "#EF553B", "Bajo"
    elif value < 15: color, performance_text = "#FECB52", "Moderado"
    else: color, performance_text = "#00CC96", "Bueno"
    
    st.markdown(f"<style>.stProgress > div > div > div > div {{background-color: {color};}}</style>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label="Pronóstico por Ciclo", value=f"{value:.1f} %")
    with col2:
        st.progress(value / 25) # Se normaliza a 25% como el máximo esperado
        st.write(f"**Evaluación:** Un pronóstico considerado **{performance_text}**.")
    
    st.divider()

    # --- Parte de Texto (del antiguo prognosis_summary_widget) ---
    st.subheader(f"1. {evaluacion.pronostico_emoji} Análisis General: **{evaluacion.pronostico_categoria}**")
    
    if evaluacion.pronostico_categoria == "BUENO": st.success(evaluacion.pronostico_frase)
    elif evaluacion.pronostico_categoria == "MODERADO": st.warning(evaluacion.pronostico_frase)
    else: st.error(evaluacion.pronostico_frase)