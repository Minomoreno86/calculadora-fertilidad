# Contenido final para: components/informe_ui.py

import streamlit as st
from models import EvaluacionFertilidad

# ✅ Importamos todas las "tarjetas" desde nuestro nuevo paquete
from .report_widgets import (
    render_pronostico_card,
    render_benchmark_card,
    render_factores_card,
    render_recommendations_widget,
    render_art_widget,
    render_sharing_buttons
)

def mostrar_informe_completo(evaluacion: EvaluacionFertilidad):
    """
    Muestra el informe completo al usuario, orquestando las diferentes
    tarjetas de componentes visuales.
    """
    # --- Tarjeta 1: Pronóstico Principal ---
    render_pronostico_card(evaluacion)
    st.divider()
    
    # --- Tarjeta 2: Comparativa ---
    render_benchmark_card(evaluacion)
    
    # --- Tarjeta 3: Desglose de Factores ---
    st.subheader("2. Análisis Detallado")
    render_factores_card(evaluacion)
    
    # --- Tarjeta 4: Recomendaciones y Recursos ---
    render_recommendations_widget(evaluacion)
    st.divider()

    # --- Tarjeta 5: Sugerencia de Tratamiento de Reproducción Asistida ---
    render_art_widget(evaluacion)
    st.divider()
    
    # --- Tarjeta 6: Botones para Compartir ---
    render_sharing_buttons(evaluacion)