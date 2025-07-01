# pages/03_Simulador.py
# CÓDIGO COMPLETO Y SINCRONIZADO CON LA ÚLTIMA VERSIÓN DE LA CLASE

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

# --- 2. Selección de Perfil y Gestión de Estado ---
opciones_registros = [f"ID {row['id']} - {row['timestamp']}" for index, row in df_registros.iterrows()]

registro_seleccionado_str = st.selectbox("Selecciona tu perfil base:", opciones_registros, key="profile_selector")

if 'registro_id_seleccionado' not in st.session_state or st.session_state.registro_id_seleccionado != registro_seleccionado_str:
    st.session_state.registro_id_seleccionado = registro_seleccionado_str
    st.session_state.variables_a_simular = [] 

registro_id = int(registro_seleccionado_str.split(" ")[1])
perfil_base = df_registros[df_registros['id'] == registro_id].iloc[0]

# --- 3. Selección Dinámica de Variables a Simular ---
st.divider()
st.markdown("### Selecciona los Factores a Simular")

variables_con_datos = [var for var in SIMULATABLE_VARIABLES if perfil_base.get(var) not in [None, 0, False]]

if not st.session_state.get('variables_a_simular'):
    st.session_state.variables_a_simular = variables_con_datos

variables_elegidas = st.multiselect(
    "Puedes añadir o quitar variables de la simulación:",
    options=list(SIMULATABLE_VARIABLES.keys()),
    default=st.session_state.variables_a_simular,
    format_func=lambda var: SIMULATABLE_VARIABLES[var]['label']
)
st.session_state.variables_a_simular = variables_elegidas

st.divider()

# --- 4. Interfaz de Simulación ---
col1, col2 = st.columns(2)
datos_simulados = perfil_base.to_dict()

with col1:
    st.subheader("🔵 Perfil Original")
    st.metric(label="Pronóstico Original Guardado", value=f"{perfil_base['pronostico_final']:.1f}%")
    st.markdown("##### Valores Originales:")
    for var_name in sorted(st.session_state.variables_a_simular):
        info = SIMULATABLE_VARIABLES[var_name]
        original_value = perfil_base.get(var_name)
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
    
    for var_name in sorted(st.session_state.variables_a_simular):
        info = SIMULATABLE_VARIABLES[var_name]
        original_value = perfil_base.get(var_name)
        
        if original_value is not None:
            default_value = float(original_value) if isinstance(original_value, (float, int)) else info.get('min', 0.0)
        else:
            default_value = info.get('min', 0) + (info.get('max', 100) - info.get('min', 0)) / 2

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

# ####################################################################
# --- 5. Lógica de Recálculo (SECCIÓN CORREGIDA) ---
# ####################################################################

if not datos_simulados.get('tiene_miomas'):
    datos_simulados['mioma_submucoso'] = False
    datos_simulados['mioma_submucoso_multiple'] = False
    datos_simulados['mioma_intramural_significativo'] = False
    datos_simulados['mioma_subseroso_grande'] = False

datos_simulados.pop('id', None)
datos_simulados.pop('timestamp', None)
datos_simulados.pop('pronostico_final', None)

# 1. Creamos la instancia del modelo.
evaluacion_simulada = EvaluacionFertilidad(**datos_simulados)
# 2. Le pedimos al modelo que ejecute su lógica interna.
evaluacion_simulada.ejecutar_evaluacion()

# 3. Obtenemos los atributos correctos que el "contrato" de la clase nos ofrece.
pronostico_simulado_num = evaluacion_simulada.pronostico_numerico
# Para la visualización, usamos la propiedad que devuelve el string "XX.X%"
pronostico_simulado_str = evaluacion_simulada.probabilidad_ajustada_final

with col2:
    # 4. Usamos las variables correctas en st.metric
    st.metric(
        label="Nuevo Pronóstico Simulado", 
        value=pronostico_simulado_str,
        delta=f"{pronostico_simulado_num - perfil_base['pronostico_final']:.1f}% vs. Original"
    )
    # --- COMPARACIÓN GRÁFICA ENTRE PERFIL ORIGINAL Y SIMULADO ---
import plotly.graph_objects as go

st.divider()
st.subheader("📊 Comparación Visual de las Variables Simuladas")

# Creamos las listas para el gráfico
variables_labels = []
original_values = []
simulated_values = []

for var_name in sorted(st.session_state.variables_a_simular):
    info = SIMULATABLE_VARIABLES[var_name]
    label = info['label']
    original_value = perfil_base.get(var_name)
    simulated_value = datos_simulados.get(var_name)

    if info['type'] == 'boolean':
        # Convertimos a valores numéricos para graficar (Sí = 1, No = 0)
        original_val_numeric = 1 if original_value else 0
        simulated_val_numeric = 1 if simulated_value else 0
    else:
        original_val_numeric = float(original_value) if original_value is not None else 0.0
        simulated_val_numeric = float(simulated_value) if simulated_value is not None else 0.0

    variables_labels.append(label)
    original_values.append(original_val_numeric)
    simulated_values.append(simulated_val_numeric)

# Creamos el gráfico de barras con Plotly
fig = go.Figure(data=[
    go.Bar(name='Original', x=variables_labels, y=original_values, marker_color='royalblue'),
    go.Bar(name='Simulado', x=variables_labels, y=simulated_values, marker_color='seagreen')
])

fig.update_layout(
    barmode='group',
    xaxis_title="Variables Simuladas",
    yaxis_title="Valores",
    title="Comparación de Variables Originales vs. Simuladas",
    height=500
)

st.plotly_chart(fig, use_container_width=True)
