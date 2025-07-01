import streamlit as st
from datetime import datetime

# --- Importaciones de nuestros módulos ---
from calculadora_fertilidad import EvaluacionFertilidad
from ui_components import ui_perfil_basico, ui_historial_clinico, ui_laboratorio, ui_factor_masculino, mostrar_informe_completo
from db_manager import crear_conexion, insertar_registro
from utils import recopilar_datos_desde_ui

# --- Configuración de la Página ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("Calculadora Profesional de Fertilidad 👶")
st.write("Herramienta de evaluación multifactorial para el pronóstico de fertilidad de pareja.")

# --- Estructura de Pestañas con la UI refactorizada ---
st.header("📝 Por favor, completa los siguientes pasos:")
tabs = st.tabs([" PASO 1: Perfil Básico ", " PASO 2: Historial Clínico ", " PASO 3: Laboratorio ", " PASO 4: Factor Masculino "])
with tabs[0]:
    ui_perfil_basico()
with tabs[1]:
    ui_historial_clinico()
with tabs[2]:
    ui_laboratorio()
with tabs[3]:
    ui_factor_masculino()

st.divider()

# --- Lógica de Generación de Informe ---
# UN ÚNICO BOTÓN PARA GENERAR EL INFORME
if st.button("Generar Informe de Fertilidad Completo", type="primary", use_container_width=True, key="generar_informe"):
    try:
        # Usamos la función de ayuda para recopilar datos de la UI
        datos_para_evaluacion = recopilar_datos_desde_ui()
        
        # Creamos y ejecutamos la evaluación
        evaluacion = EvaluacionFertilidad(**datos_para_evaluacion)
        evaluacion.ejecutar_evaluacion()
        
        # Guardamos el objeto de evaluación completo en el estado de la sesión
        st.session_state.evaluacion_actual = evaluacion

    except Exception as e:
        st.error(f"Ocurrió un error al generar el informe: {e}")
        st.session_state.evaluacion_actual = None # Limpiamos en caso de error

st.divider()

# --- Bloque de Visualización del Informe ---
# Este bloque solo se ejecuta si existe un informe válido en el estado de la sesión.
if 'evaluacion_actual' in st.session_state and st.session_state.evaluacion_actual is not None:
    evaluacion = st.session_state.evaluacion_actual

    # La función que dibuja toda la sección de resultados
    mostrar_informe_completo(evaluacion)

    # El botón de guardar solo aparece junto con el informe
    if st.button("💾 Guardar este Perfil y Resultado", use_container_width=True, key="guardar_informe"):
        DB_FILE = "fertilidad.db"
        conn = crear_conexion(DB_FILE)
        if conn:
            # Aquí necesitaríamos la función 'preparar_registro_db' de un paso anterior
            # Por ahora, asumimos que existe o la creamos en 'db_manager.py'
            from db_manager import preparar_registro_db # Asegúrate que esta función exista
            registro = preparar_registro_db(evaluacion)
            registro_id = insertar_registro(conn, registro)
            conn.close()

            if registro_id:
                st.success(f"¡Éxito! Perfil guardado con ID: {registro_id}")
                # Limpiamos el estado para empezar de nuevo
                del st.session_state.evaluacion_actual
            else:
                st.error("Error al guardar el perfil.")