# ui_components.py
import streamlit as st
import plotly.express as px # plotly lo necesita mostrar_informe_completo

def ui_perfil_basico():
    """Crea la UI para el Paso 1 y usa st.session_state para guardar los valores."""
    st.markdown("Introduce tus datos básicos. Estos se guardarán automáticamente mientras avanzas.")
    
    st.number_input("Edad", 18, 55, key="edad")
    st.number_input("Duración promedio del ciclo (días)", 20, 90, key="duracion_ciclo")
    
    st.write("**Cálculo del IMC**")
    # Para el IMC, como es un cálculo, no usamos la 'key' directamente.
    peso = st.number_input("Peso (kg)", 30.0, 200.0, 65.0, format="%.1f")
    talla = st.number_input("Talla (m)", 1.0, 2.5, 1.65, format="%.2f")

    if talla > 0:
        imc_calculado = peso / (talla ** 2)
        st.info(f"IMC calculado: {imc_calculado:.2f} kg/m²")
        st.session_state.imc = imc_calculado
    else:
        st.session_state.imc = 0

# CORRECCIÓN: He restaurado esta función que había omitido por error.
def mostrar_informe_completo(evaluacion):
    """
    Dibuja el informe completo usando expanders para una mejor organización.
    """
    st.header("📋 Tu Informe de Fertilidad Personalizado")
    
    st.subheader("1. Pronóstico de Concepción por Ciclo")
    st.metric(label="PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")

    st.subheader("2. Análisis Detallado de Factores")
    
    with st.expander("🔬 Ver desglose de factores evaluados", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("Factores Gineco-Anatómicos")
            st.write(f"* **IMC:** {evaluacion.comentario_imc or 'No reportado'}")
            st.write(f"* **SOP:** {evaluacion.severidad_sop or 'No reportado'}")
            # ... y así para el resto de factores
        with col2:
            st.info("Factores Endocrino-Metabólicos")
            # ...
        with col3:
            st.info("Factor Masculino")
            # ...

    if evaluacion.recomendaciones_lista:
        with st.expander("💡 Ver plan de acción y recomendaciones sugeridas"):
            # ...
            pass
            
    with st.expander("📊 Ver comparativa visual del pronóstico"):
        # ...
        pass