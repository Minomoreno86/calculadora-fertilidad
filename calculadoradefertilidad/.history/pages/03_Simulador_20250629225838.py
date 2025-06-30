# pages/03_Simulador.py
import streamlit as st
import pandas as pd
from db_manager import crear_conexion, leer_todos_los_registros
from calculadora_fertilidad import EvaluacionFertilidad

# --- Configuración de la Página ---
st.set_page_config(page_title="Simulador de Escenarios", page_icon="🧪", layout="wide")
st.title("🧪 Simulador de Escenarios: ¿Qué Pasa Si...?")
st.write(
    "Selecciona uno de tus perfiles guardados y experimenta cómo cambiar ciertos factores "
    "podría impactar tu pronóstico de fertilidad."
)

# --- Cargar Perfiles Guardados ---
DB_FILE = "fertilidad.db"
conn = crear_conexion(DB_FILE)
if conn is not None:
    df_registros = leer_todos_los_registros(conn)
    conn.close()
else:
    st.error("No se pudo conectar a la base de datos.")
    st.stop() # Detiene la ejecución si no hay BBDD

if df_registros.empty:
    st.warning("No hay perfiles guardados para simular. Por favor, guarda al menos un informe desde la Calculadora.")
    st.stop()

# --- Selector de Perfil ---
# Creamos una lista de opciones para el selectbox, mostrando ID y fecha
opciones_registros = [f"ID {row['id']} - {row['timestamp']}" for index, row in df_registros.iterrows()]
registro_seleccionado_str = st.selectbox(
    "Selecciona el perfil que quieres usar como base para la simulación:",
    opciones_registros
)

if registro_seleccionado_str:
    # Obtenemos el ID del string seleccionado
    registro_id = int(registro_seleccionado_str.split(" ")[1])
    
    # Buscamos el registro completo en el DataFrame
    perfil_base = df_registros[df_registros['id'] == registro_id].iloc[0]

    st.divider()
    
    # --- Interfaz de Simulación en Dos Columnas ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔵 Perfil Original")
        # Mostramos los datos originales importantes
        st.metric(label="Pronóstico Original Guardado", value=f"{perfil_base['pronostico_final']:.1f}%")
        st.write(f"**IMC Original:** {perfil_base['imc']:.2f}")
        st.write(f"**Morfología Espermática Original:** {perfil_base['morfologia_normal']:.0f}%")
        
    with col2:
        st.subheader("🟢 Perfil Simulado")
        
        # --- Controles de Simulación (Sliders) ---
        # Creamos sliders cuyo valor inicial es el del perfil base
        imc_simulado = st.slider(
            "Simula un nuevo IMC:", 
            min_value=18.0, 
            max_value=40.0, 
            value=perfil_base['imc'],
            step=0.1
        )
        
        morfologia_simulada = st.slider(
            "Simula una nueva Morfología Espermática Normal (%):",
            min_value=0,
            max_value=100,
            value=int(perfil_base['morfologia_normal']),
            step=1
        )

    # --- Lógica de Recálculo ---
    # Creamos un nuevo diccionario con los datos del perfil base
    datos_simulados = perfil_base.to_dict()
    
    # Sobrescribimos los valores con los de los sliders
    datos_simulados['imc'] = imc_simulado
    datos_simulados['morfologia_normal'] = float(morfologia_simulada)
    
    # Convertimos los 0/1 de la BBDD a True/False para la clase
    datos_simulados['tiene_sop'] = bool(datos_simulados['tiene_sop'])
    datos_simulados['tiene_miomas'] = bool(datos_simulados['tiene_miomas'])
    # ... (y así para todos los campos booleanos)
    
    # Creamos una nueva instancia del cerebro con los datos simulados
    evaluacion_simulada = EvaluacionFertilidad(
        edad=datos_simulados['edad'],
        duracion_ciclo=datos_simulados['duracion_ciclo'],
        imc=datos_simulados['imc'],
        tiene_sop=bool(datos_simulados['tiene_sop']),
        grado_endometriosis=datos_simulados['grado_endometriosis'],
        tiene_miomas=bool(datos_simulados['tiene_miomas']),
        mioma_submucoso=bool(datos_simulados['mioma_submucoso']),
        mioma_intramural_significativo=bool(datos_simulados['mioma_intramural_significativo']),
        mioma_subseroso_grande=bool(datos_simulados['mioma_subseroso_grande']),
        amh=datos_simulados['amh'],
        prolactina=datos_simulados['prolactina'],
        tsh=datos_simulados['tsh'],
        tpo_ab_positivo=bool(datos_simulados['tpo_ab_positivo']),
        insulina_ayunas=datos_simulados['insulina_ayunas'],
        glicemia_ayunas=datos_simulados['glicemia_ayunas'],
        concentracion_esperm=datos_simulados['concentracion_esperm'],
        motilidad_progresiva=datos_simulados['motilidad_progresiva'],
        morfologia_normal=datos_simulados['morfologia_normal'],
        vitalidad_esperm=datos_simulados['vitalidad_esperm']
        # Nota: no pasamos todos los campos para simplificar, pero en una versión final lo haríamos
    )
    
    evaluacion_simulada.ejecutar_evaluacion()
    pronostico_simulado_num = float(evaluacion_simulada.probabilidad_ajustada_final.replace('%', ''))

    # Volvemos a la columna 2 para mostrar el resultado simulado
    with col2:
        st.metric(
            label="Nuevo Pronóstico Simulado", 
            value=f"{pronostico_simulado_num:.1f}%",
            delta=f"{pronostico_simulado_num - perfil_base['pronostico_final']:.1f}% vs. Original"
        )