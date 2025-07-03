# Contenido final para: components/informe_ui.py

import streamlit as st
from models import EvaluacionFertilidad
from .report_widgets import (
    render_main_score,
    render_prognosis_summary,
    render_factors_details,
    render_recommendations_widget,  # <-- Importado
    render_art_recommendation,
    render_sharing_buttons
)

def mostrar_informe_completo(evaluacion: EvaluacionFertilidad):
    render_main_score(evaluacion)
    st.divider()

    render_prognosis_summary(evaluacion)
    st.divider()

    st.subheader("2. Análisis Detallado y Recomendaciones")
    render_factors_details(evaluacion)
    render_recommendations_widget(evaluacion) # <-- Llamado aquí
    st.divider()

    render_art_recommendation(evaluacion)
    st.divider()

    render_sharing_buttons(evaluacion)