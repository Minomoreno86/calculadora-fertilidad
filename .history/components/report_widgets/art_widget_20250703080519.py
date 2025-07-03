# Contenido para: components/report_widgets/art_widget.py

import streamlit as st
from recomendaciones_reproduccion import obtener_recomendaciones

def render_art_recommendation(evaluacion):
    """
    Obtiene y muestra la recomendación de técnica de reproducción asistida.
    ART = Assisted Reproduction Techniques.
    """
    st.subheader("🔬 Recomendación de Técnicas de Reproducción Asistida")
    
    # 1. Prepara el diccionario de datos para la función de recomendaciones
    datos_reproduccion = {
        'edad': evaluacion.edad,
        'tiene_otb': evaluacion.tiene_otb,
        'amh': evaluacion.amh,
        'concentracion_esperm': evaluacion.concentracion_esperm,
        'motilidad_progresiva': evaluacion.motilidad_progresiva,
        'resultado_hsg': evaluacion.resultado_hsg,
        'tiene_sop': evaluacion.tiene_sop
    }

    # 2. Llama a la función para obtener la recomendación
    recomendaciones_repro, tecnica_sugerida = obtener_recomendaciones(datos_reproduccion)
    
    # 3. Muestra los resultados en la interfaz
    with st.container(border=True):
        st.success(f"**Técnica Recomendada:** {tecnica_sugerida}")
        for rec in recomendaciones_repro:
            st.write(rec)