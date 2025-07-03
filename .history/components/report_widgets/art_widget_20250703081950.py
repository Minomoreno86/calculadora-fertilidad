# Contenido para: components/report_widgets/art_widget.py

import streamlit as st
# Asegúrate de que este import apunte al archivo correcto
from recomendaciones_reproduccion import obtener_recomendaciones

# ✅ El nombre de la función debe ser este:
def render_art_widget(evaluacion):
    """
    Obtiene y muestra la recomendación de técnica de reproducción asistida.
    """
    st.subheader("🔬 Recomendación de Técnicas de Reproducción Asistida")
    
    datos_reproduccion = {
        'edad': evaluacion.edad,
        'tiene_otb': evaluacion.tiene_otb,
        'amh': evaluacion.amh,
        'concentracion_esperm': evaluacion.concentracion_esperm,
        'motilidad_progresiva': evaluacion.motilidad_progresiva,
        'resultado_hsg': evaluacion.resultado_hsg,
        'tiene_sop': evaluacion.tiene_sop
    }

    recomendaciones_repro, tecnica_sugerida = obtener_recomendaciones(datos_reproduccion)
    
    with st.container(border=True):
        st.success(f"**Técnica Recomendada:** {tecnica_sugerida}")
        for rec in recomendaciones_repro:
            st.write(rec)