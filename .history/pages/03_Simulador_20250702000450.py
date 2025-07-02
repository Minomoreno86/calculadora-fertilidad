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
st.session_state['tema'] = perfil_base.get('tema', 'light')
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
   st.subheader("🔮 Nuevo Pronóstico Simulado")
   st.metric(
    label="Nuevo Pronóstico Simulado", 
    value=pronostico_simulado_str,
    delta=f"{pronostico_simulado_num - perfil_base['pronostico_final']:.1f}% vs. Original"
)

# --- COMPARACIÓN GRÁFICA DEL PRONÓSTICO ORIGINAL VS. SIMULADO CON ETIQUETAS ---
st.divider()
st.subheader("📊 Comparación Visual del Pronóstico")

import plotly.graph_objects as go

# Datos a comparar
pronostico_original = perfil_base['pronostico_final']
pronostico_simulado = pronostico_simulado_num

# Crear gráfico de barras con etiquetas
fig = go.Figure(data=[
    go.Bar(
        name='Pronóstico Original',
        x=['Pronóstico'],
        y=[pronostico_original],
        marker_color='royalblue',
        text=[f"{pronostico_original:.1f}%"],
        textposition='outside'
    ),
    go.Bar(
        name='Pronóstico Simulado',
        x=['Pronóstico'],
        y=[pronostico_simulado],
        marker_color='seagreen',
        text=[f"{pronostico_simulado:.1f}%"],
        textposition='outside'
    )
])

fig.update_layout(
    barmode='group',
    yaxis_title="Probabilidad de Embarazo (%)",
    title="Comparación de Pronóstico Original vs. Simulado",
    height=400,
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig, use_container_width=True)

# --- RECOMENDACIONES CLÍNICAS ACTUALIZADAS ---
st.divider()
st.subheader("💡 Recomendaciones Clínicas para el Escenario Simulado")

if evaluacion_simulada.recomendaciones_lista:
    recomendaciones_unicas = list(set(evaluacion_simulada.recomendaciones_lista))
    for rec in recomendaciones_unicas:
        st.warning(f"• {rec}")
else:
    st.success("No hay recomendaciones clínicas específicas para este escenario simulado.")

# --- GUARDAR ESCENARIO SIMULADO COMO NUEVO PERFIL ---
st.divider()
st.subheader("💾 Guardar Escenario Simulado")

if st.button("Guardar este Escenario Simulado como Nuevo Perfil"):
    from db_manager import crear_conexion, insertar_registro
    from datetime import datetime

    DB_FILE = "fertilidad.db"
    conn = crear_conexion(DB_FILE)

    if conn is not None:
        try:
            pronostico_num = float(evaluacion_simulada.probabilidad_ajustada_final.replace('%', ''))
        except:
            pronostico_num = 0.0

        # Preparamos el registro para guardar
        registro_simulado = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datos_simulados.get('edad', perfil_base['edad']),
            datos_simulados.get('duracion_ciclo', perfil_base['duracion_ciclo']),
            datos_simulados.get('imc', perfil_base['imc']),
            1 if datos_simulados.get('tiene_sop', perfil_base['tiene_sop']) else 0,
            datos_simulados.get('grado_endometriosis', perfil_base['grado_endometriosis']),
            1 if datos_simulados.get('tiene_miomas', perfil_base['tiene_miomas']) else 0,
            1 if datos_simulados.get('mioma_submucoso', perfil_base['mioma_submucoso']) else 0,
            1 if datos_simulados.get('mioma_submucoso_multiple', perfil_base['mioma_submucoso_multiple']) else 0,
            1 if datos_simulados.get('mioma_intramural_significativo', perfil_base['mioma_intramural_significativo']) else 0,
            1 if datos_simulados.get('mioma_subseroso_grande', perfil_base['mioma_subseroso_grande']) else 0,
            datos_simulados.get('tipo_adenomiosis', perfil_base['tipo_adenomiosis']),
            datos_simulados.get('tipo_polipo', perfil_base['tipo_polipo']),
            datos_simulados.get('resultado_hsg', perfil_base['resultado_hsg']),
            datos_simulados.get('amh', perfil_base['amh']),
            datos_simulados.get('prolactina', perfil_base['prolactina']),
            datos_simulados.get('tsh', perfil_base['tsh']),
            1 if datos_simulados.get('tpo_ab_positivo', perfil_base['tpo_ab_positivo']) else 0,
            datos_simulados.get('insulina_ayunas', perfil_base['insulina_ayunas']),
            datos_simulados.get('glicemia_ayunas', perfil_base['glicemia_ayunas']),
            datos_simulados.get('volumen_seminal', perfil_base['volumen_seminal']),
            datos_simulados.get('concentracion_esperm', perfil_base['concentracion_esperm']),
            datos_simulados.get('motilidad_progresiva', perfil_base['motilidad_progresiva']),
            datos_simulados.get('morfologia_normal', perfil_base['morfologia_normal']),
            datos_simulados.get('vitalidad_esperm', perfil_base['vitalidad_esperm']),
            pronostico_num
        )

        registro_id = insertar_registro(conn, registro_simulado)
        conn.close()

        if registro_id:
            st.success(f"✅ Escenario simulado guardado exitosamente con ID: {registro_id}")
        else:
            st.error("❌ Ocurrió un error al guardar el escenario simulado.")
    else:
        st.error("❌ No se pudo conectar a la base de datos para guardar el escenario simulado.")