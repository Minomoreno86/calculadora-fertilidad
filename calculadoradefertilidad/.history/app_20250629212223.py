# app.py
import streamlit as st
from calculadora_fertilidad import EvaluacionFertilidad
# CORRECCIÓN: Descomentamos ui_historial_clinico
from ui_components import ui_perfil_basico, ui_historial_clinico, mostrar_informe_completo
# from ui_components import ui_laboratorio, ui_factor_masculino

# --- Configuración y Título ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("Calculadora Profesional de Fertilidad 👶")
st.write("Herramienta de evaluación multifactorial para el pronóstico de fertilidad de pareja.")

# --- Inicialización del Session State ---
if 'step' not in st.session_state:
    st.session_state.step = 1
    # --- Datos Paso 1 ---
    st.session_state.edad = 30
    st.session_state.duracion_ciclo = 28
    st.session_state.imc = 0
    # --- Datos Paso 2 ---
    st.session_state.sop_radio = "No"
    st.session_state.endo_radio = "No"
    st.session_state.grado_endometriosis = 1
    st.session_state.miomas_radio = "No"
    st.session_state.mioma_submucoso_radio = "No"
    st.session_state.mioma_submucoso_multiple_radio = "No"
    st.session_state.mioma_intramural_radio = "No"
    st.session_state.mioma_subseroso_radio = "No"
    st.session_state.adeno_radio = "No"
    st.session_state.tipo_adenomiosis = "focal"
    st.session_state.polipo_radio = "No"
    st.session_state.tipo_polipo = "pequeno_unico"
    st.session_state.hsg_radio = "No"
    st.session_state.resultado_hsg = "normal"

# --- Estructura de Pestañas ---
st.header("📝 Por favor, completa los siguientes pasos:")
tab1, tab2, tab3, tab4 = st.tabs([" PASO 1: Perfil Básico ", " PASO 2: Historial Clínico ", " PASO 3: Laboratorio ", " PASO 4: Factor Masculino "])

with tab1:
    ui_perfil_basico()

with tab2:
    # CORRECCIÓN: Llamamos a la nueva función
    ui_historial_clinico()

with tab3:
    st.info("Próximamente: Moveremos aquí la sección de laboratorio.")

with tab4:
    st.info("Próximamente: Moveremos aquí la sección de factor masculino.")

# --- Botón de Envío y Lógica Principal ---
st.divider()
if st.button("Generar Informe de Fertilidad (Prueba Pasos 1-2)", type="primary", use_container_width=True):
    try:
        # CORRECCIÓN: Añadimos los parámetros del historial, convirtiendo los 'Sí'/'No' a Booleanos
        evaluacion = EvaluacionFertilidad(
            # Datos Paso 1
            edad=st.session_state.edad,
            duracion_ciclo=st.session_state.duracion_ciclo,
            imc=st.session_state.imc,
            # Datos Paso 2
            tiene_sop=(st.session_state.sop_radio == 'Sí'),
            grado_endometriosis=st.session_state.grado_endometriosis if st.session_state.endo_radio == 'Sí' else 0,
            tiene_miomas=(st.session_state.miomas_radio == 'Sí'),
            mioma_submucoso=(st.session_state.mioma_submucoso_radio == 'Sí'),
            mioma_submucoso_multiple=(st.session_state.mioma_submucoso_multiple_radio == 'Sí'),
            mioma_intramural_significativo=(st.session_state.mioma_intramural_radio == 'Sí'),
            mioma_subseroso_grande=(st.session_state.mioma_subseroso_radio == 'Sí'),
            tipo_adenomiosis=st.session_state.tipo_adenomiosis if st.session_state.adeno_radio == 'Sí' else "",
            tipo_polipo=st.session_state.tipo_polipo if st.session_state.polipo_radio == 'Sí' else "",
            resultado_hsg=st.session_state.resultado_hsg if st.session_state.hsg_radio == 'Sí' else ""
        )
        
        evaluacion.ejecutar_evaluacion()
        mostrar_informe_completo(evaluacion)

    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado al generar el informe: {e}")