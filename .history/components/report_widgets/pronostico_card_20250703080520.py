# Contenido para: components/report_widgets/pronostico_card.py

import streamlit as st

def render_pronostico_card(evaluacion):
    """Muestra la tarjeta principal del pronóstico en el informe."""
    
    st.header("🎯 Tu Pronóstico de Fertilidad")
    col1, col2 = st.columns([1, 2])

    with col1:
        # Usamos markdown para poder controlar el tamaño del emoji
        st.markdown(f"<p style='font-size: 120px; text-align: center; line-height: 1.2;'>{evaluacion.pronostico_emoji}</p>", unsafe_allow_html=True)
    
    with col2:
        st.metric(
            label=f"Probabilidad de Concepción por Ciclo ({evaluacion.pronostico_categoria})",
            value=evaluacion.probabilidad_ajustada_final
        )
        st.info(f"**Conclusión:** {evaluacion.pronostico_frase}")