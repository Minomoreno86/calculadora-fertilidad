# app.py
import streamlit as st
from calculadora_fertilidad import EvaluacionFertilidad
# ui_components ahora tendrá funciones más pequeñas y específicas
from ui_components import ui_perfil_basico, ui_historial_clinico, ui_laboratorio, ui_factor_masculino, mostrar_informe_completo

# --- Configuración y Título ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("Calculadora Profesional de Fertilidad 👶")
st.write("Herramienta de evaluación multifactorial para el pronóstico de fertilidad de pareja.")

# --- Inicialización del Session State ---
# Esto se ejecuta solo una vez al principio de la sesión.
if 'step' not in st.session_state:
    st.session_state.step = 1
    # Inicializamos todas las claves que vamos a necesitar
    st.session_state.edad = 30
    st.session_state.duracion_ciclo = 28
    # ... y así para todos los demás inputs que usaremos.
    # Por ahora, nos centramos en los del primer paso.

# --- Estructura de Pestañas ---
st.header("📝 Por favor, completa los siguientes pasos:")

tab1, tab2, tab3, tab4 = st.tabs([" PASO 1: Perfil Básico ", " PASO 2: Historial Clínico ", " PASO 3: Laboratorio ", " PASO 4: Factor Masculino "])

with tab1:
    # Esta función ahora leerá y escribirá directamente en st.session_state
    ui_perfil_basico()

with tab2:
    st.write("Contenido del historial clínico irá aquí.")
    # ui_historial_clinico()

with tab3:
    st.write("Contenido del laboratorio irá aquí.")
    # ui_laboratorio()

with tab4:
    st.write("Contenido del factor masculino irá aquí.")
    # ui_factor_masculino()


# --- Botón de Envío y Lógica Principal ---
st.divider()
if st.button("Generar Informe de Fertilidad Completo", type="primary", use_container_width=True):
    try:
        # Recogemos los datos desde st.session_state en lugar de un diccionario
        evaluacion = EvaluacionFertilidad(
            edad=st.session_state.edad,
            duracion_ciclo=st.session_state.duracion_ciclo
            # ... y el resto de parámetros que iremos añadiendo
        )
        
        evaluacion.ejecutar_evaluacion()
        mostrar_informe_completo(evaluacion)

    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado al generar el informe: {e}")