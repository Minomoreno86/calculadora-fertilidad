# pages/03_Simulador.py
import streamlit as st
import pandas as pd
from db_manager import crear_conexion, leer_todos_los_registros
from calculadora_fertilidad import EvaluacionFertilidad

# ... (El código hasta la Lógica de Recálculo permanece sin cambios) ...
st.set_page_config(page_title="Simulador de Escenarios", page_icon="🧪", layout="wide")
st.title("🧪 Simulador de Escenarios: ¿Qué Pasa Si...?")
st.write(
    "Selecciona uno de tus perfiles guardados y experimenta cómo cambiar ciertos factores "
    "modificables podría impactar tu pronóstico de fertilidad."
)
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

opciones_registros = [f"ID {row['id']} - {row['timestamp']}" for index, row in df_registros.iterrows()]
registro_seleccionado_str = st.selectbox(
    "Selecciona el perfil que quieres usar como base para la simulación:",
    opciones_registros
)

if registro_seleccionado_str:
    registro_id = int(registro_seleccionado_str.split(" ")[1])
    perfil_base = df_registros[df_registros['id'] == registro_id].iloc[0]
    st.divider()
    col1, col2 = st.columns([0.8, 1.2])
    with col1:
        st.subheader("🔵 Perfil Original")
        st.metric(label="Pronóstico Original Guardado", value=f"{perfil_base['pronostico_final']:.1f}%")
        imc_original = perfil_base.get('imc')
        tsh_original = perfil_base.get('tsh')
        prolactina_original = perfil_base.get('prolactina')
        conc_original = perfil_base.get('concentracion_esperm')
        morf_original = perfil_base.get('morfologia_normal')
        st.write(f"**IMC Original:** {f'{imc_original:.2f}' if imc_original is not None else 'No Proporcionado'}")
        st.write(f"**TSH Original:** {f'{tsh_original:.2f}' if tsh_original is not None else 'No Proporcionado'}")
        st.write(f"**Prolactina Original:** {f'{prolactina_original:.1f}' if prolactina_original is not None else 'No Proporcionado'}")
        st.write(f"**Concentración Espermática Original:** {f'{conc_original:.1f} M/mL' if conc_original is not None else 'No Proporcionado'}")
        st.write(f"**Morfología Espermática Original:** {f'{morf_original:.0f}%' if morf_original is not None else 'No Proporcionado'}")
    with col2:
        st.subheader("🟢 Perfil Simulado")
        imc_simulado = st.slider("Simula un nuevo IMC:", 18.0, 40.0, imc_original if imc_original is not None else 22.5, 0.1)
        tsh_simulado = st.slider("Simula una nueva TSH (ideal < 2.5):", 0.5, 10.0, tsh_original if tsh_original is not None else 2.0, 0.1)
        prolactina_simulada = st.slider("Simula una nueva Prolactina (ideal < 25):", 0.0, 50.0, prolactina_original if prolactina_original is not None else 15.0, 0.5)
        conc_esperm_simulada = st.slider("Simula una nueva Concentración Espermática (M/mL):", 0.0, 200.0, conc_original if conc_original is not None else 40.0, 1.0)
        morfologia_simulada = st.slider("Simula una nueva Morfología Normal (%):", 0, 100, int(morf_original) if morf_original is not None else 4, 1)

    # --- Lógica de Recálculo (SECCIÓN CORREGIDA) ---
    datos_simulados = perfil_base.to_dict()
    datos_simulados['imc'] = imc_simulado
    datos_simulados['tsh'] = tsh_simulado
    datos_simulados['prolactina'] = prolactina_simulada
    datos_simulados['concentracion_esperm'] = conc_esperm_simulada
    datos_simulados['morfologia_normal'] = float(morfologia_simulada)
    
    # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
    # Eliminamos las claves del diccionario que no son parte del "contrato" de EvaluacionFertilidad
    datos_simulados.pop('id', None)
    datos_simulados.pop('timestamp', None)
    datos_simulados.pop('pronostico_final', None) # El pronóstico tampoco es un input

    # Ahora, el diccionario "datos_simulados" está limpio y solo contiene los argumentos que la clase espera.
    evaluacion_simulada = EvaluacionFertilidad(**datos_simulados)
    
    evaluacion_simulada.ejecutar_evaluacion()
    pronostico_simulado_num = float(evaluacion_simulada.probabilidad_ajustada_final.replace('%', ''))

    with col2:
        st.metric(
            label="Nuevo Pronóstico Simulado", 
            value=f"{pronostico_simulado_num:.1f}%",
            delta=f"{pronostico_simulado_num - perfil_base['pronostico_final']:.1f}% vs. Original"
        )