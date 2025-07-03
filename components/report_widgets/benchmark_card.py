# Contenido para: components/report_widgets/benchmark_card.py
import streamlit as st

def render_benchmark_card(evaluacion):
    """Muestra la tarjeta de comparación con el benchmark de edad."""
    with st.container(border=True):
        st.subheader("📊 Comparativa de Desempeño")
        st.write(evaluacion.benchmark_frase)