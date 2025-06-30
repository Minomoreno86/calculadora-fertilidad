# pages/03_Simulador.py
import streamlit as st
import pandas as pd
import numpy as np
from db_manager import crear_conexion, leer_todos_los_registros
from calculadora_fertilidad import EvaluacionFertilidad
from config import SIMULATABLE_VARIABLES

st.set_page_config(page_title="Simulador de Escenarios", page_icon="🧪", layout="wide")
st.title("🧪 Simulador de Escenarios: ¿Qué Pasa Si...?")
st.write(
    "Selecciona un perfil guardado y experimenta cómo cambiar ciertos factores podría impactar tu pronóstico de fertilidad."
)

# --- 1. Carga de Datos ---
DB_FILE = "fertilidad.db"
conn = crear_conexion(DB_FILE)
if conn is not None:
    df_registros = leer_todos_los_registros(conn)
    conn.close()
else:
    st.error("No se pudo conectar a la base de datos.")
    st.stop()

if df_registros.empty:
    st.warning("No hay perfiles guardados para simular. Por favor, guarda al menos un informe desde la Calculadora.")
    st.stop()

df_registros = df_registros.replace({np.nan: None})
opciones_registros = [f"ID {row['id']} - {row['timestamp']}" for index, row in df_registros.iterrows()]

# --- 2. Selección de Perfil ---
registro_seleccionado_str = st.selectbox("Selecciona tu perfil base:", opciones_registros, key="profile_selector")
registro_id = int(registro_seleccionado_str.split(" ")[1])
perfil_base = df_registros[df_registros['id'] == registro_id].iloc[0]

# --- 3. Selección de Variables a Simular ---
st.divider()
st.markdown("### Selecciona los Factores a Simular")

# Determinamos las variables que tienen un valor en el perfil cargado
variables_con_datos = [var for var in SIMULATABLE_VARIABLES if perfil_base.get(var) not in [None, 0, False]]
variables_elegidas = st.multiselect(
    "Puedes añadir o quitar variables de la simulación:",
    options=list(SIMULATABLE_VARIABLES.keys()),
    default=variables_con_datos,
    format_func=lambda var: SIMULATABLE_VARIABLES[var]['label']
)

st.divider()

# --- 4. Interfaz de Simulación ---
col1, col2 = st.columns(2)
datos_simulados = perfil_base.to_dict()

with col1:
    st.subheader("🔵 Perfil Original")
    st.metric(label="Pronóstico Original Guardado", value=f"{perfil_base['pronostico_final']:.1f}%")
    st.markdown("##### Valores Originales:")
    # Mostramos solo las variables que se están simulando
    for var_name in sorted(variables_elegidas):
        info = SIMULATABLE_VARIABLES[var_name]
        original_value = perfil_base.get(var_name)
        
        # Lógica de visualización
        if info['type'] == 'boolean':
            display_value = "Sí" if original_value else "No"
        else:
            if original_value is not None:
                display_value = (info['format_spec'] % original_value) + info.get('unit', '')
            else:
                display_value = "No Proporcionado"
        st.write(f"**{info['label']}:** {display_value}")

with col2:
    st.subheader("🟢 Perfil Simulado")
    st.markdown("##### Mueve los controles para ver el impacto:")
    
    # Generamos los widgets de simulación dinámicamente
    for var_name in sorted(variables_elegidas):
        info = SIMULATABLE_VARIABLES[var_name]
        original_value = perfil_base.get(var_name)
        
        # Preparamos un valor por defecto numérico y seguro para el widget
        if original_value is not None:
            # Aseguramos que el valor sea del tipo correcto (float o int)
            default_value = float(original_value) if '.' in str(original_value) else int(original_value)
        else:
            # Si no hay valor, usamos un punto medio del rango del slider como default
            default_value = info['min'] + (info['max'] - info['min']) / 2

        if info['type'] == 'slider':
            simulated_value = st.slider(
                info['label'], min_value=info['min'], max_value=info['max'],
                value=default_value, step=info['step'], key=f"sim_{var_name}"
            )
            datos_simulados[var_name] = simulated_value
        elif info['type'] == 'boolean':
            simulated_value = st.toggle(
                info['label'], value=bool(original_value), key=f"sim_{var_name}"
            )
            datos_simulados[var_name] = simulated_value

# --- 5. Lógica de Recálculo ---
if not datos_simulados.get('tiene_miomas'):
    datos_simulados['mioma_submucoso'] = False; datos_simulados['mioma_intramural_significativo'] = False; datos_simulados['mioma_subseroso_grande'] = False

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