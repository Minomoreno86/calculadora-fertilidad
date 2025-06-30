# app.py
import streamlit as st
from calculadora_fertilidad import EvaluacionFertilidad
from ui_components import ui_perfil_basico, ui_historial_clinico, ui_laboratorio, mostrar_informe_completo

# --- Configuración y Título ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("Calculadora Profesional de Fertilidad 👶")
st.write("Herramienta de evaluación multifactorial para el pronóstico de fertilidad de pareja.")

# --- Inicialización del Session State ---
if 'step' not in st.session_state:
    st.session_state.step = 1
    # Paso 1
    st.session_state.edad = 30
    st.session_state.duracion_ciclo = 28
    st.session_state.imc = 0
    # Paso 2
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
    # Paso 3
    st.session_state.use_amh = True
    st.session_state.amh = 2.5
    st.session_state.use_prolactina = True
    st.session_state.prolactina = 15.0
    st.session_state.use_tsh = True
    st.session_state.tsh = 2.0
    st.session_state.tpo_radio = "No"
    st.session_state.use_homa = True
    st.session_state.insulina_ayunas = 8.0
    st.session_state.glicemia_ayunas = 90.0

# --- Estructura de Pestañas ---
st.header("📝 Por favor, completa los siguientes pasos:")
tab1, tab2, tab3, tab4 = st.tabs([" PASO 1: Perfil Básico ", " PASO 2: Historial Clínico ", " PASO 3: Laboratorio ", " PASO 4: Factor Masculino "])

with tab1:
    ui_perfil_basico()
with tab2:
    ui_historial_clinico()
with tab3:
    ui_laboratorio()
with tab4:
    st.info("Próximamente: Moveremos aquí la sección de factor masculino.")

# --- Botón de Envío y Lógica Principal ---
st.divider()
if st.button("Generar Informe de Fertilidad", type="primary", use_container_width=True):
    try:
        tiene_miomas_val = (st.session_state.get("miomas_radio", "No") == 'Sí')
        evaluacion = EvaluacionFertilidad(
            edad=st.session_state.edad,
            duracion_ciclo=st.session_state.duracion_ciclo,
            imc=st.session_state.imc,
            tiene_sop=(st.session_state.get("sop_radio", "No") == 'Sí'),
            grado_endometriosis=st.session_state.get("grado_endometriosis", 1) if st.session_state.get("endo_radio", "No") == 'Sí' else 0,
            tiene_miomas=tiene_miomas_val,
            mioma_submucoso=(st.session_state.get("mioma_submucoso_radio", "No") == 'Sí') and tiene_miomas_val,
            mioma_submucoso_multiple=(st.session_state.get("mioma_submucoso_multiple_radio", "No") == 'Sí') and tiene_miomas_val,
            mioma_intramural_significativo=(st.session_state.get("mioma_intramural_radio", "No") == 'Sí') and tiene_miomas_val,
            mioma_subseroso_grande=(st.session_state.get("mioma_subseroso_radio", "No") == 'Sí') and tiene_miomas_val,
            tipo_adenomiosis=st.session_state.get("tipo_adenomiosis", "focal") if st.session_state.get("adeno_radio", "No") == 'Sí' else "",
            tipo_polipo=st.session_state.get("tipo_polipo", "pequeno_unico") if st.session_state.get("polipo_radio", "No") == 'Sí' else "",
            resultado_hsg=st.session_state.get("resultado_hsg", "normal") if st.session_state.get("hsg_radio", "No") == 'Sí' else None,
            amh=st.session_state.get("amh") if st.session_state.get("use_amh") else None,
            prolactina=st.session_state.get("prolactina") if st.session_state.get("use_prolactina") else None,
            tsh=st.session_state.get("tsh") if st.session_state.get("use_tsh") else None,
            tpo_ab_positivo=(st.session_state.get("tpo_radio", "No") == 'Sí') if st.session_state.get("use_tsh") else False,
            insulina_ayunas=st.session_state.get("insulina_ayunas") if st.session_state.get("use_homa") else None,
            glicemia_ayunas=st.session_state.get("glicemia_ayunas") if st.session_state.get("use_homa") else None
        )
        evaluacion.ejecutar_evaluacion()
        mostrar_informe_completo(evaluacion)
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado al generar el informe: {e}")
        st.error("Detalle técnico: " + str(e))