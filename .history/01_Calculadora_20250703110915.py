
import streamlit as st
from datetime import datetime

# --- ✅ PASO 1: CORREGIR LOS IMPORTS ---
from models import EvaluacionFertilidad
from engine import ejecutar_evaluacion_completa  # <-- Importar la nueva función
from components import ui_perfil_basico, ui_historial_clinico, ui_laboratorio, ui_factor_masculino, mostrar_informe_completo
from database import crear_conexion, insertar_registro, preparar_registro_db, desbloquear_logro, obtener_logros
from utils import recopilar_datos_desde_ui, aplicar_tema_personalizado

# --- Configuración de la Página ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("🎯 Calculadora Profesional de Fertilidad 👶")
st.markdown("## Evalúa tu pronóstico de fertilidad de manera moderna, visual y personalizada.")
# Selector de tema dinámico
st.selectbox(
    "🎨 Selecciona el tema de visualización:",
    ["light", "dark", "blue", "pink"],
    key="tema"
)
from utils import aplicar_tema_personalizado
aplicar_tema_personalizado()


# --- INICIO DE LA CORRECCIÓN DEFINITIVA: INICIALIZACIÓN DE ESTADO ---
# Este bloque crea la "memoria" de la aplicación una sola vez por sesión.
# Este bloque crea la "memoria" de la aplicación una sola vez por sesión.
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.evaluacion_actual = None

    # Perfil Básico
    if 'edad' not in st.session_state: st.session_state.edad = 30
    if 'duracion_ciclo' not in st.session_state: st.session_state.duracion_ciclo = 28
    if 'peso' not in st.session_state: st.session_state.peso = 65.0
    if 'talla' not in st.session_state: st.session_state.talla = 1.65
    if 'imc' not in st.session_state: st.session_state.imc = 23.9

    # Historial Clínico
    if 'tiene_sop' not in st.session_state: st.session_state.tiene_sop = False
    if 'tiene_endometriosis' not in st.session_state: st.session_state.tiene_endometriosis = False
    if 'grado_endometriosis' not in st.session_state: st.session_state.grado_endometriosis = 1
    if 'tiene_polipos_check' not in st.session_state: st.session_state.tiene_polipos_check = False
    if 'tipo_polipo' not in st.session_state: st.session_state.tipo_polipo = "pequeno_unico"
    if 'tiene_miomas' not in st.session_state: st.session_state.tiene_miomas = False
    if 'mioma_submucoso' not in st.session_state: st.session_state.mioma_submucoso = False
    if 'mioma_submucoso_multiple' not in st.session_state: st.session_state.mioma_submucoso_multiple = False
    if 'mioma_intramural_significativo' not in st.session_state: st.session_state.mioma_intramural_significativo = False
    if 'mioma_subseroso_grande' not in st.session_state: st.session_state.mioma_subseroso_grande = False
    if 'tiene_adenomiosis_check' not in st.session_state: st.session_state.tiene_adenomiosis_check = False
    if 'tipo_adenomiosis' not in st.session_state: st.session_state.tipo_adenomiosis = "focal"
    if 'tiene_otb' not in st.session_state: st.session_state.tiene_otb = False
    if 'tiene_hsg' not in st.session_state: st.session_state.tiene_hsg = False
    if 'resultado_hsg' not in st.session_state: st.session_state.resultado_hsg = "normal"
   

    # Laboratorio
    if 'use_amh' not in st.session_state: st.session_state.use_amh = False
    if 'amh' not in st.session_state: st.session_state.amh = 2.5
    if 'use_prolactina' not in st.session_state: st.session_state.use_prolactina = False
    if 'prolactina' not in st.session_state: st.session_state.prolactina = 15.0
    if 'use_tsh' not in st.session_state: st.session_state.use_tsh = False
    if 'tsh' not in st.session_state: st.session_state.tsh = 2.0
    if 'tpo_ab_positivo' not in st.session_state: st.session_state.tpo_ab_positivo = False
    if 'use_homa' not in st.session_state: st.session_state.use_homa = False
    if 'insulina_ayunas' not in st.session_state: st.session_state.insulina_ayunas = 8.0
    if 'glicemia_ayunas' not in st.session_state: st.session_state.glicemia_ayunas = 90.0

    # Factor Masculino
    if 'use_esperma' not in st.session_state: st.session_state.use_esperma = False
    if 'volumen_seminal' not in st.session_state: st.session_state.volumen_seminal = 1.5
    if 'concentracion_esperm' not in st.session_state: st.session_state.concentracion_esperm = 20.0
    if 'motilidad_progresiva' not in st.session_state: st.session_state.motilidad_progresiva = 32
    if 'morfologia_normal' not in st.session_state: st.session_state.morfologia_normal = 4
    if 'vitalidad_esperm' not in st.session_state: st.session_state.vitalidad_esperm = 58
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
    
    with st.spinner('Analizando factores y calculando pronóstico... 🧠'):
        try:
            datos_para_evaluacion = recopilar_datos_desde_ui()
            
            # --- ✅ PASO 2: CORREGIR LA LLAMADA A LA LÓGICA ---
            
            # 1. Se crea el objeto contenedor de datos
            evaluacion = EvaluacionFertilidad(**datos_para_evaluacion)
            
            # 2. Se le pasa el objeto al "motor" para que lo procese
            ejecutar_evaluacion_completa(evaluacion)
            
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
    if st.session_state.evaluacion_actual is not None:
        conn = crear_conexion("fertilidad.db")
        if conn is not None:
            try:
                registro_db = preparar_registro_db(st.session_state.evaluacion_actual)
                resultado = insertar_registro(conn, registro_db)
                
                if resultado:
                    desbloquear_logro(conn, "Primer Informe")
                    st.toast('¡Perfil guardado en la base de datos!', icon='✅')
                else:
                    st.error("No se pudo guardar el perfil en la base de datos.")
                
                conn.close()
            except Exception as e:
                st.error(f"Error al guardar: {e}")
                conn.close()
    else:
        st.warning("⚠️ Debes generar primero un informe antes de poder guardarlo.")
    st.divider()
st.subheader("🏅 Tus Logros")

conn = crear_conexion("fertilidad.db")
if conn is not None:
    df_logros = obtener_logros(conn)
    for index, row in df_logros.iterrows():
        if row['obtenido']:
            st.success(f"✅ {row['nombre']}: {row['descripcion']} (Obtenido el {row['timestamp']})")
        else:
            st.info(f"🔒 {row['nombre']}: {row['descripcion']}")
    conn.close()