# Contenido para: components/report_widgets/recommendations_widget.py

import streamlit as st

def render_recommendations_widget(evaluacion):
    """
    Muestra los expanders con insights clínicos, recomendaciones de acción
    y recursos educativos.
    """
    if evaluacion.insights_clinicos:
        with st.expander("💎 Perlas de Sabiduría Clínica Personalizadas"):
            for insight in evaluacion.insights_clinicos:
                st.info(f"🧠 {insight}")

    if evaluacion.recomendaciones_lista:
        with st.expander("💡 Ver plan de acción y recomendaciones sugeridas"):
            # Usamos set para eliminar recomendaciones duplicadas si las hubiera
            recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
            for rec in recomendaciones_unicas:
                st.warning(f"• {rec}")

    with st.expander("🔗 Recursos Educativos y Sociedades Científicas"):
        st.markdown("""
        * **[American Society for Reproductive Medicine (ASRM)](https://www.asrm.org/)**
        * **[European Society of Human Reproduction and Embryology (ESHRE)](https://www.eshre.eu/)**
        * **[Red Latinoamericana de Reproducción Asistida (REDLARA)](https://redlara.com/)**
        """)