# app.py
import streamlit as st
from calculadora_fertilidad import EvaluacionFertilidad
# CORRECCIÓN: Comentamos las funciones que aún no existen en ui_components.py
from ui_components import ui_perfil_basico, mostrar_informe_completo
# from ui_components import ui_historial_clinico, ui_laboratorio, ui_factor_masculino

# --- Configuración y Título ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("Calculadora Profesional de Fertilidad 👶")
st.write("Herramienta de evaluación multifactorial para el pronóstico de fertilidad de pareja.")

# --- Inicialización del Session State ---
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.edad = 30
    st.session_state.duracion_ciclo = 28
    st.session_state.imc = 0 # Inicializamos imc también

# --- Estructura de Pestañas ---
st.header("📝 Por favor, completa los siguientes pasos:")
tab1, tab2, tab3, tab4 = st.tabs([" PASO 1: Perfil Básico ", " PASO 2: Historial Clínico ", " PASO 3: Laboratorio ", " PASO 4: Factor Masculino "])

with tab1:
    ui_perfil_basico()

with tab2:
    st.info("Próximamente: Moveremos aquí la sección de historial clínico.")

with tab3:
    st.info("Próximamente: Moveremos aquí la sección de laboratorio.")

with tab4:
    st.info("Próximamente: Moveremos aquí la sección de factor masculino.")

# --- Botón de Envío y Lógica Principal ---
st.divider()
if st.button("Generar Informe de Fertilidad (Prueba Paso 1)", type="primary", use_container_width=True):
    try:
        # Por ahora, solo pasamos los datos del Paso 1 que ya están en el estado
        evaluacion = EvaluacionFertilidad(
            edad=st.session_state.edad,
            duracion_ciclo=st.session_state.duracion_ciclo,
            imc=st.session_state.imc
        )
        
        evaluacion.ejecutar_evaluacion()
        mostrar_informe_completo(evaluacion)

    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado al generar el informe: {e}")