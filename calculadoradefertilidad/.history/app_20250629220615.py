# app.py
import streamlit as st
from calculadora_fertilidad import EvaluacionFertilidad
from ui_components import ui_perfil_basico, ui_historial_clinico, ui_laboratorio, ui_factor_masculino, mostrar_informe_completo
# --- AÑADIMOS IMPORTACIONES DE DB ---
from db_manager import crear_conexion, insertar_registro
from datetime import datetime

# --- Configuración y Título (sin cambios) ---
# ...

# --- Inicialización del Session State (sin cambios) ---
# ...

# --- Estructura de Pestañas (sin cambios) ---
# ...

# --- Botón de Envío y Lógica Principal (MODIFICADO) ---
st.divider()
if st.button("Generar Informe de Fertilidad Completo", type="primary", use_container_width=True):
    try:
        # (La creación del objeto 'evaluacion' no cambia)
        evaluacion = EvaluacionFertilidad(
            # ... (todos los parámetros)
        )
        evaluacion.ejecutar_evaluacion()
        
        # Guardamos el objeto de evaluación en el estado de la sesión para poder acceder a él después
        st.session_state.evaluacion_actual = evaluacion
        
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado al generar el informe: {e}")
        st.error("Detalle técnico: " + str(e))

# --- Lógica para mostrar y guardar el informe ---
# Este bloque ahora está fuera del if del botón, para que el informe permanezca visible.
if 'evaluacion_actual' in st.session_state:
    evaluacion = st.session_state.evaluacion_actual
    mostrar_informe_completo(evaluacion)
    
    st.divider()
    # Creamos un nuevo botón para guardar, que solo aparece si hay un informe
    if st.button("💾 Guardar este Perfil y Resultado", use_container_width=True):
        DB_FILE = "fertilidad.db"
        conn = crear_conexion(DB_FILE)
        if conn is not None:
            # Preparamos los datos para la inserción
            # Convertimos booleanos a 1/0 para SQLite
            try:
                pronostico_num = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
            except:
                pronostico_num = 0.0

            registro = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                evaluacion.edad,
                evaluacion.duracion_ciclo,
                evaluacion.imc,
                1 if evaluacion.tiene_sop else 0,
                evaluacion.grado_endometriosis,
                1 if evaluacion.tiene_miomas else 0,
                1 if evaluacion.mioma_submucoso else 0,
                1 if evaluacion.mioma_intramural_significativo else 0,
                1 if evaluacion.mioma_subseroso_grande else 0,
                evaluacion.amh,
                evaluacion.prolactina,
                evaluacion.tsh,
                1 if evaluacion.tpo_ab_positivo else 0,
                evaluacion.insulina_ayunas,
                evaluacion.glicemia_ayunas,
                evaluacion.concentracion_esperm,
                evaluacion.motilidad_progresiva,
                evaluacion.morfologia_normal,
                evaluacion.vitalidad_esperm,
                pronostico_num
            )
            
            registro_id = insertar_registro(conn, registro)
            conn.close()
            
            if registro_id:
                st.success(f"¡Éxito! Perfil guardado correctamente en la base de datos con el ID: {registro_id}")
            else:
                st.error("Hubo un error al intentar guardar el perfil en la base de datos.")