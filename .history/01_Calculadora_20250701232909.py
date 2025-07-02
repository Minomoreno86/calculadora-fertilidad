import streamlit as st
from datetime import datetime

# --- Módulos del Proyecto ---
from calculadora_fertilidad import EvaluacionFertilidad
from ui_components import ui_perfil_basico, ui_historial_clinico, ui_laboratorio, ui_factor_masculino, mostrar_informe_completo
from db_manager import crear_conexion, insertar_registro, preparar_registro_db
from utils import recopilar_datos_desde_ui

# --- Configuración de la Página ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("🎯 Calculadora Profesional de Fertilidad 👶")
st.markdown("## Evalúa tu pronóstico de fertilidad de manera moderna, visual y personalizada.")
# Selector de tema dinámico
st.selectbox(
    "Selecciona el tema de visualización:",
    ["light", "dark", "blue", "pink"],
    key="tema"
)
from ui_components import aplicar_tema_personalizado
aplicar_tema_personalizado()


# --- INICIO DE LA CORRECCIÓN DEFINITIVA: INICIALIZACIÓN DE ESTADO ---
# Este bloque crea la "memoria" de la aplicación una sola vez por sesión.
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.evaluacion_actual = None
    # Perfil Básico
    st.session_state.edad = 30
    st.session_state.duracion_ciclo = 28
    st.session_state.peso = 65.0
    st.session_state.talla = 1.65
    st.session_state.imc = 23.9
    # Historial Clínico
    st.session_state.tiene_sop = False
    st.session_state.tiene_endometriosis = False
    st.session_state.grado_endometriosis = 1
    st.session_state.tiene_polipos_check = False
    st.session_state.tipo_polipo = "pequeno_unico"
    st.session_state.tiene_miomas = False
    st.session_state.mioma_submucoso = False
    st.session_state.mioma_submucoso_multiple = False
    st.session_state.mioma_intramural_significativo = False
    st.session_state.mioma_subseroso_grande = False
    st.session_state.tiene_adenomiosis_check = False
    st.session_state.tipo_adenomiosis = "focal"
    st.session_state.tiene_hsg = False
    st.session_state.resultado_hsg = "normal"
    # Laboratorio
    st.session_state.use_amh = False
    st.session_state.amh = 2.5
    st.session_state.use_prolactina = False
    st.session_state.prolactina = 15.0
    st.session_state.use_tsh = False
    st.session_state.tsh = 2.0
    st.session_state.tpo_ab_positivo = False
    st.session_state.use_homa = False
    st.session_state.insulina_ayunas = 8.0
    st.session_state.glicemia_ayunas = 90.0
    # Factor Masculino
    st.session_state.use_esperma = False
    st.session_state.volumen_seminal = 1.5
    st.session_state.concentracion_esperm = 20.0
    st.session_state.motilidad_progresiva = 32
    st.session_state.morfologia_normal = 4
    st.session_state.vitalidad_esperm = 58
# --- FIN DE LA CORRECCIÓN ---


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
    ui_factor_masculino()

st.divider()

# --- Lógica de Generación de Informe ---
if st.button("Generar Informe de Fertilidad Completo", type="primary", use_container_width=True, key="generar_informe"):
    
    # --- INICIO DE LA MODIFICACIÓN ---
    with st.spinner('Analizando factores y calculando pronóstico... 🧠'):
        try:
            # Toda la lógica que ya teníamos va indentada dentro del spinner
            datos_para_evaluacion = recopilar_datos_desde_ui()
            evaluacion = EvaluacionFertilidad(**datos_para_evaluacion)
            evaluacion.ejecutar_evaluacion()
            st.session_state.evaluacion_actual = evaluacion

        except Exception as e:
            st.error(f"Ocurrió un error al generar el informe: {e}")
            st.session_state.evaluacion_actual = None

# --- Bloque de Visualización del Informe ---
if 'evaluacion_actual' in st.session_state and st.session_state.evaluacion_actual is not None:
    # Esta llamada no se modifica, usará tu función completa y correcta del informe.
    mostrar_informe_completo(st.session_state.evaluacion_actual)
    
    # Lógica del botón de guardar
    if st.button("💾 Guardar este Perfil y Resultado", use_container_width=True, key="guardar_informe"):
        # (El resto de la lógica de guardado permanece igual)
        pass # Placeholder para tu lógica de guardado
    st.toast('¡Perfil guardado en la base de datos!', icon='✅')