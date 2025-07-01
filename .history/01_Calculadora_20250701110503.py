# 01_Calculadora.py (Versión FINAL con Lógica de Fiabilidad CORREGIDA)

import streamlit as st
from datetime import datetime
from calculadora_fertilidad import EvaluacionFertilidad
from ui_components import ui_perfil_basico, ui_historial_clinico, ui_laboratorio, ui_factor_masculino, mostrar_informe_completo
from db_manager import crear_conexion, insertar_registro

# --- Configuración de la Página ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("Calculadora Profesional de Fertilidad 👶")
st.write("Herramienta de evaluación multifactorial para el pronóstico de fertilidad de pareja.")

# --- Inicialización del Session State (Tu bloque completo) ---
if 'step' not in st.session_state:
    st.session_state.step = 1
    # Paso 1
    st.session_state.edad = 30
    st.session_state.duracion_ciclo = 28
    st.session_state.imc = 0.0
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
    # Paso 3 (Opt-In por defecto)
    st.session_state.use_amh = False
    st.session_state.amh = 2.5
    st.session_state.use_prolactina = False
    st.session_state.prolactina = 15.0
    st.session_state.use_tsh = False
    st.session_state.tsh = 2.0
    st.session_state.tpo_radio = "No"
    st.session_state.use_homa = False
    st.session_state.insulina_ayunas = 8.0
    st.session_state.glicemia_ayunas = 90.0
    # Paso 4 (Opt-In por defecto)
    st.session_state.use_esperma = False
    st.session_state.volumen_seminal = 2.5
    st.session_state.concentracion_esperm = 40.0
    st.session_state.motilidad_progresiva = 45
    st.session_state.morfologia_normal = 5
    st.session_state.vitalidad_esperm = 75

# --- LÓGICA DE NAVEGACIÓN GUIADA Y FLEXIBLE ---
pasos_totales = 4
st.progress((st.session_state.step) / pasos_totales, text=f"Paso {st.session_state.step} de {pasos_totales}")

def siguiente_paso():
    if st.session_state.step < pasos_totales:
        st.session_state.step += 1

def anterior_paso():
    if st.session_state.step > 1:
        st.session_state.step -= 1

container = st.container(border=True)

# Mostrar la UI correspondiente al paso actual
if st.session_state.step == 1:
    with container:
        ui_perfil_basico()
elif st.session_state.step == 2:
    with container:
        ui_historial_clinico()
elif st.session_state.step == 3:
    with container:
        ui_laboratorio()
elif st.session_state.step == 4:
    with container:
        ui_factor_masculino()

# --- BOTONES DE NAVEGACIÓN ---
col1, col2 = st.columns([1, 1])
with col1:
    if st.session_state.step > 1:
        st.button("← Anterior", on_click=anterior_paso, use_container_width=True)
with col2:
    if st.session_state.step < pasos_totales:
        st.button("Siguiente →", on_click=siguiente_paso, type="primary", use_container_width=True)

st.divider()

# --- INDICADOR DE FIABILIDAD (LÓGICA CORREGIDA) ---
st.subheader("Fiabilidad del Pronóstico")

puntos_fiabilidad = 0
max_puntos = 4  # Un punto por cada sección

# 1. Perfil Básico siempre cuenta
puntos_fiabilidad += 1

# 2. Historial Clínico: Cuenta si se aporta el resultado de la HSG
if st.session_state.get('hsg_radio') == 'Sí':
    puntos_fiabilidad += 1

# 3. Laboratorio: Cuenta si se aporta cualquier resultado de laboratorio
if st.session_state.get('use_amh') or st.session_state.get('use_tsh') or st.session_state.get('use_homa'):
    puntos_fiabilidad += 1

# 4. Factor Masculino: Cuenta si se aporta el espermatograma
if st.session_state.get('use_esperma'):
    puntos_fiabilidad += 1

# Cálculo y visualización
fiabilidad = puntos_fiabilidad / max_puntos
st.progress(fiabilidad, text=f"Nivel de Precisión: {int(fiabilidad * 100)}%")
st.caption("Mientras más datos relevantes aportes, más preciso y personalizado será el pronóstico.")

if fiabilidad <= 0.25:
    st.info("ℹ️ El pronóstico se basa solo en datos básicos. Para una evaluación más completa, considera añadir resultados de HSG, laboratorio y espermatograma.")
elif fiabilidad < 1.0:
     st.warning("⚠️ ¡Buen comienzo! Estás en camino a un pronóstico de alta precisión. Completa las secciones restantes para obtener la máxima fiabilidad.")
else:
     st.success("✅ ¡Excelente! Has proporcionado todos los datos clave para un pronóstico de máxima fiabilidad.")

# --- LÓGICA DE GENERACIÓN DE INFORME (SIEMPRE VISIBLE) ---
if st.button("Generar Informe de Fertilidad Completo", type="primary", use_container_width=True, key="generar_informe"):
    try:
        tiene_miomas_val = (st.session_state.get("miomas_radio", "No") == 'Sí')
        evaluacion = EvaluacionFertilidad(
            edad=st.session_state.get("edad", 30),
            duracion_ciclo=st.session_state.get("duracion_ciclo", 28),
            imc=st.session_state.get("imc", 0),
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
            glicemia_ayunas=st.session_state.get("glicemia_ayunas") if st.session_state.get("use_homa") else None,
            volumen_seminal=st.session_state.get("volumen_seminal") if st.session_state.get("use_esperma") else None,
            concentracion_esperm=st.session_state.get("concentracion_esperm") if st.session_state.get("use_esperma") else None,
            motilidad_progresiva=st.session_state.get("motilidad_progresiva") if st.session_state.get("use_esperma") else None,
            morfologia_normal=st.session_state.get("morfologia_normal") if st.session_state.get("use_esperma") else None,
            vitalidad_esperm=st.session_state.get("vitalidad_esperm") if st.session_state.get("use_esperma") else None
        )
        
        evaluacion.ejecutar_evaluacion()
        st.session_state.evaluacion_actual = evaluacion
        
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado al generar el informe: {e}")
        st.error("Detalle técnico: " + str(e))
        if 'evaluacion_actual' in st.session_state:
            del st.session_state.evaluacion_actual

# --- Lógica para mostrar y guardar el informe (Tu bloque completo) ---
if 'evaluacion_actual' in st.session_state:
    evaluacion = st.session_state.evaluacion_actual
    mostrar_informe_completo(evaluacion)
    
    st.divider()
    if st.button("💾 Guardar este Perfil y Resultado", use_container_width=True):
        DB_FILE = "fertilidad.db"
        conn = crear_conexion(DB_FILE)
        if conn is not None:
            try:
                pronostico_num = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
            except:
                pronostico_num = 0.0

            registro = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                evaluacion.edad, evaluacion.duracion_ciclo, evaluacion.imc,
                1 if evaluacion.tiene_sop else 0,
                evaluacion.grado_endometriosis,
                1 if evaluacion.tiene_miomas else 0,
                1 if evaluacion.mioma_submucoso else 0,
                1 if evaluacion.mioma_submucoso_multiple else 0,
                1 if evaluacion.mioma_intramural_significativo else 0,
                1 if evaluacion.mioma_subseroso_grande else 0,
                evaluacion.tipo_adenomiosis,
                evaluacion.tipo_polipo,
                evaluacion.resultado_hsg,
                evaluacion.amh,
                evaluacion.prolactina,
                evaluacion.tsh,
                1 if evaluacion.tpo_ab_positivo else 0,
                evaluacion.insulina_ayunas,
                evaluacion.glicemia_ayunas,
                evaluacion.volumen_seminal,
                evaluacion.concentracion_esperm,
                evaluacion.motilidad_progresiva,
                evaluacion.morfologia_normal,
                evaluacion.vitalidad_esperm,
                pronostico_num
            )
            
            registro_id = insertar_registro(conn, registro)
            conn.close()
            
            if registro_id:
                st.success(f"¡Éxito! Perfil guardado correctamente con el ID: {registro_id}")
                del st.session_state.evaluacion_actual
            else:
                st.error("Hubo un error al intentar guardar el perfil en la base de datos.")