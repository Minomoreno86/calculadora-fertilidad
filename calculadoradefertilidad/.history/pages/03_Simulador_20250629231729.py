# pages/03_Simulador.py
import streamlit as st
import pandas as pd
import numpy as np
from db_manager import crear_conexion, leer_todos_los_registros
from calculadora_fertilidad import EvaluacionFertilidad
from config import SIMULATABLE_VARIABLES # <-- Importamos nuestra nueva configuración

st.set_page_config(page_title="Simulador de Escenarios", page_icon="🧪", layout="wide")
st.title("🧪 Simulador de Escenarios: ¿Qué Pasa Si...?")
st.write("Selecciona un perfil guardado. El simulador mostrará los factores que ya tenías. Usa el menú desplegable para añadir o quitar otros factores que quieras simular.")

DB_FILE = "fertilidad.db"
conn = crear_conexion(DB_FILE)
if conn is not None:
    df_registros = leer_todos_los_registros(conn)
    conn.close()
else:
    st.error("No se pudo conectar a la base de datos."); st.stop()

if df_registros.empty:
    st.warning("No hay perfiles guardados para simular."); st.stop()

df_registros = df_registros.replace({np.nan: None})
opciones_registros = [f"ID {row['id']} - {row['timestamp']}" for index, row in df_registros.iterrows()]

# --- Selector de Perfil y Estado de la Simulación ---
if 'registro_id_seleccionado' not in st.session_state:
    st.session_state.registro_id_seleccionado = None

registro_seleccionado_str = st.selectbox("Selecciona tu perfil base:", opciones_registros)
registro_id = int(registro_seleccionado_str.split(" ")[1])

# Si el usuario cambia de perfil, reseteamos las variables de simulación
if st.session_state.registro_id_seleccionado != registro_id:
    st.session_state.registro_id_seleccionado = registro_id
    st.session_state.variables_a_simular = [] # Reset

perfil_base = df_registros[df_registros['id'] == registro_id].iloc[0]

# --- Determinamos las variables a mostrar inicialmente ---
variables_iniciales = [var for var, info in SIMULATABLE_VARIABLES.items() if perfil_base.get(var) is not None]
if not st.session_state.variables_a_simular:
    st.session_state.variables_a_simular = variables_iniciales

st.divider()

# --- Widget para que el usuario elija qué simular ---
st.markdown("### Selecciona los Factores a Simular")
variables_elegidas = st.multiselect(
    "Puedes añadir o quitar variables de la simulación:",
    options=list(SIMULATABLE_VARIABLES.keys()),
    default=st.session_state.variables_a_simular,
    format_func=lambda var: SIMULATABLE_VARIABLES[var]['label']
)
st.session_state.variables_a_simular = variables_elegidas

st.divider()

# --- Interfaz de Simulación Dinámica ---
col1, col2 = st.columns(2)
datos_simulados = perfil_base.to_dict()

with col1:
    st.subheader("🔵 Perfil Original")
    st.metric(label="Pronóstico Original Guardado", value=f"{perfil_base['pronostico_final']:.1f}%")
    st.markdown("##### Valores Originales:")
    for var_name in st.session_state.variables_a_simular:
        info = SIMULATABLE_VARIABLES[var_name]
        original_value = perfil_base.get(var_name)
        display_value = f"{original_value:{info['format']}}" if original_value is not None else "No Proporcionado"
        st.write(f"**{info['label']}:** {display_value}")

with col2:
    st.subheader("🟢 Perfil Simulado")
    st.markdown("##### Mueve los sliders para ver el impacto:")
    # --- Generación dinámica de sliders ---
    for var_name in st.session_state.variables_a_simular:
        info = SIMULATABLE_VARIABLES[var_name]
        original_value = perfil_base.get(var_name)
        # Usamos un valor por defecto razonable si el original es None
        default_value = original_value if original_value is not None else info['min'] + (info['max'] - info['min']) / 2
        
        simulated_value = st.slider(
            info['label'], 
            min_value=info['min'], 
            max_value=info['max'],
            value=default_value,
            step=info['step']
        )
        # Actualizamos el diccionario de datos simulados con el valor del slider
        datos_simulados[var_name] = simulated_value

# --- Lógica de Recálculo ---
datos_simulados.pop('id', None); datos_simulados.pop('timestamp', None); datos_simulados.pop('pronostico_final', None)
evaluacion_simulada = EvaluacionFertilidad(**datos_simulados)
evaluacion_simulada.ejecutar_evaluacion()
pronostico_simulado_num = float(evaluacion_simulada.probabilidad_ajustada_final.replace('%', ''))

with col2:
    st.metric(
        label="Nuevo Pronóstico Simulado", 
        value=f"{pronostico_simulado_num:.1f}%",
        delta=f"{pronostico_simulado_num - perfil_base['pronostico_final']:.1f}% vs. Original"
    )