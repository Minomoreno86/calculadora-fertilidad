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
    st.stop()

if df_registros.empty:
    st.warning("No hay perfiles guardados para simular. Por favor, guarda al menos un informe desde la Calculadora.")
    st.stop()

# --- Selector de Perfil ---
opciones_registros = [f"ID {row['id']} - {row['timestamp']}" for index, row in df_registros.iterrows()]
registro_seleccionado_str = st.selectbox(
    "Selecciona el perfil que quieres usar como base para la simulación:",
    opciones_registros
)

if registro_seleccionado_str:
    registro_id = int(registro_seleccionado_str.split(" ")[1])
    perfil_base = df_registros[df_registros['id'] == registro_id].iloc[0]

    st.divider()
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔵 Perfil Original")
        st.metric(label="Pronóstico Original Guardado", value=f"{perfil_base['pronostico_final']:.1f}%")
        
        # --- VISUALIZACIÓN DEFENSIVA ---
        # Verificamos si el valor no es None antes de formatearlo
        imc_original = perfil_base.get('imc')
        morf_original = perfil_base.get('morfologia_normal')

        imc_display = f"{imc_original:.2f}" if imc_original is not None else "No proporcionado"
        morf_display = f"{morf_original:.0f}%" if morf_original is not None else "No proporcionado"
        
        st.write(f"**IMC Original:** {imc_display}")
        st.write(f"**Morfología Espermática Original:** {morf_display}")
        
    with col2:
        st.subheader("🟢 Perfil Simulado")
        
        # --- INICIALIZACIÓN DEFENSIVA DE SLIDERS ---
        # Si el valor original es None, le damos un valor por defecto razonable al slider
        imc_simulado = st.slider(
            "Simula un nuevo IMC:", 
            min_value=18.0, 
            max_value=40.0, 
            value=imc_original if imc_original is not None else 22.5,
            step=0.1
        )
        
        morfologia_simulada = st.slider(
            "Simula una nueva Morfología Espermática Normal (%):",
            min_value=0,
            max_value=100,
            value=int(morf_original) if morf_original is not None else 4,
            step=1
        )

    # --- Lógica de Recálculo ---
    datos_simulados = perfil_base.to_dict()
    datos_simulados['imc'] = imc_simulado
    datos_simulados['morfologia_normal'] = float(morfologia_simulada)
    
    # Aseguramos que los campos que no se simulan pero pueden ser None, se pasen correctamente
    # Usamos .get() para evitar errores si una columna no existiera
    evaluacion_simulada = EvaluacionFertilidad(
        edad=datos_simulados.get('edad'),
        duracion_ciclo=datos_simulados.get('duracion_ciclo'),
        imc=datos_simulados.get('imc'),
        tiene_sop=bool(datos_simulados.get('tiene_sop')),
        grado_endometriosis=datos_simulados.get('grado_endometriosis'),
        tiene_miomas=bool(datos_simulados.get('tiene_miomas')),
        mioma_submucoso=bool(datos_simulados.get('mioma_submucoso')),
        mioma_intramural_significativo=bool(datos_simulados.get('mioma_intramural_significativo')),
        mioma_subseroso_grande=bool(datos_simulados.get('mioma_subseroso_grande')),
        amh=datos_simulados.get('amh'),
        prolactina=datos_simulados.get('prolactina'),
        tsh=datos_simulados.get('tsh'),
        tpo_ab_positivo=bool(datos_simulados.get('tpo_ab_positivo')),
        insulina_ayunas=datos_simulados.get('insulina_ayunas'),
        glicemia_ayunas=datos_simulados.get('glicemia_ayunas'),
        concentracion_esperm=datos_simulados.get('concentracion_esperm'),
        motilidad_progresiva=datos_simulados.get('motilidad_progresiva'),
        morfologia_normal=datos_simulados.get('morfologia_normal'),
        vitalidad_esperm=datos_simulados.get('vitalidad_esperm')
    )
    
    evaluacion_simulada.ejecutar_evaluacion()
    pronostico_simulado_num = float(evaluacion_simulada.probabilidad_ajustada_final.replace('%', ''))

    with col2:
        st.metric(
            label="Nuevo Pronóstico Simulado", 
            value=f"{pronostico_simulado_num:.1f}%",
            delta=f"{pronostico_simulado_num - perfil_base['pronostico_final']:.1f}% vs. Original"
        )