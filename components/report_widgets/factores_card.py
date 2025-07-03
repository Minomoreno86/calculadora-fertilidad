# Contenido para: components/report_widgets/factores_card.py
import streamlit as st
import pandas as pd

def render_factores_card(evaluacion):
    """Muestra una tabla con el desglose de los factores que influyeron."""
    st.subheader("💡 Factores Clave en tu Evaluación")
    
    datos_factores = {
        "Factor": ["IMC", "Ciclo Menstrual", "Reserva Ovárica (AMH)", "Factor Masculino", "Trompas (HSG/OTB)"],
        "Estado": [evaluacion.comentario_imc, evaluacion.comentario_ciclo, evaluacion.diagnostico_reserva, evaluacion.diagnostico_masculino_detallado, evaluacion.comentario_hsg or "No OTB"],
        "Impacto en Pronóstico": [f"x{evaluacion.imc_factor}", f"x{evaluacion.ciclo_factor}", f"x{evaluacion.amh_factor}", f"x{evaluacion.male_factor}", f"x{evaluacion.hsg_factor * evaluacion.otb_factor}"]
    }
    df = pd.DataFrame(datos_factores)
    st.table(df)