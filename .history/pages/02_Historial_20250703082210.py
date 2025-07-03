# pages/02_Historial.py
import streamlit as st
import pandas as pd
import plotly.express as px
from db_manager import crear_conexion, leer_todos_los_registros, eliminar_registro_por_id, eliminar_todos_los_registros
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import aplicar_tema_personalizado
aplicar_tema_personalizado()
# --- Configuración de la Página ---
st.set_page_config(page_title="Historial de Evaluaciones", page_icon="📈", layout="wide")
st.title("📈 Historial de Evaluaciones Guardadas")
st.write("Aquí puedes ver y gestionar todos los perfiles y resultados que has guardado.")

# --- Conexión y Lectura de Datos ---
DB_FILE = "fertilidad.db"
conn = crear_conexion(DB_FILE)

if conn is not None:
    df_registros = leer_todos_los_registros(conn)
    
    if not df_registros.empty:
        # --- Procesamiento de Datos ---
        df_registros['timestamp'] = pd.to_datetime(df_registros['timestamp'])
        df_registros = df_registros.sort_values(by='timestamp')

        st.divider()
        
        # --- Gráfico de Evolución ---
        st.subheader("📊 Evolución del Pronóstico")
        fig = px.line(
            df_registros,
            x='timestamp',
            y='pronostico_final',
            title='Evolución del Pronóstico de Fertilidad a lo Largo del Tiempo',
            markers=True,
            labels={'timestamp': 'Fecha de Registro', 'pronostico_final': 'Pronóstico de Embarazo (%)'}
        )
        fig.update_traces(line=dict(color='royalblue', width=3))
        fig.update_layout(yaxis_title="Pronóstico de Embarazo (%)")
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- Tabla de Datos Crudos ---
        with st.expander("Ver todos los datos guardados en formato de tabla"):
            st.dataframe(df_registros)

        st.divider()
        from db_manager import leer_todos_los_riesgos

st.subheader("⚠️ Historial de Evaluaciones de Riesgo de Aborto")
conn = crear_conexion(DB_FILE)
if conn is not None:
    df_riesgos = leer_todos_los_riesgos(conn)

    if not df_riesgos.empty:
        df_riesgos['timestamp'] = pd.to_datetime(df_riesgos['timestamp'])
        df_riesgos = df_riesgos.sort_values(by='timestamp')

        st.divider()

        # --- Gráfico de Evolución de Riesgo de Aborto ---
        st.subheader("📉 Evolución del Riesgo de Aborto")
        fig = px.line(
            df_riesgos,
            x='timestamp',
            y='riesgo_final',
            title='Evolución del Riesgo de Aborto a lo Largo del Tiempo',
            markers=True,
            labels={'timestamp': 'Fecha de Registro', 'riesgo_final': 'Riesgo Estimado (%)'}
        )
        fig.update_traces(line=dict(color='red', width=3))
        fig.update_layout(yaxis_title="Riesgo Estimado de Aborto (%)")
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- Tabla de Datos Crudos de Riesgo de Aborto ---
        with st.expander("Ver todos los riesgos guardados en formato de tabla"):
            st.dataframe(df_riesgos)

    else:
        st.info("No hay evaluaciones de riesgo de aborto registradas.")

    conn.close()

    # --- Sección de Gestión de Datos ---
    st.subheader("🗑️ Gestionar Historial")
    col1, col2 = st.columns(2)
    
    with col1:
        # --- Borrado Individual ---
        st.markdown("##### Borrar un registro específico")
        lista_ids = df_registros['id'].tolist()
        id_a_borrar = st.selectbox("Selecciona el ID del registro a eliminar:", lista_ids)
        
        if st.button("Eliminar Registro Seleccionado"):
            eliminar_registro_por_id(conn, id_a_borrar)
            st.success(f"Registro con ID {id_a_borrar} eliminado.")
            st.info("La página se recargará para reflejar los cambios.")
            conn.close() 
            st.rerun()

    with col2:
        # --- Borrado Total ---
        st.markdown("##### Borrar todo el historial")
        if st.button("🚨 Eliminar TODO el Historial", type="primary", help="Esta acción no se puede deshacer."):
            eliminar_todos_los_registros(conn)
            st.success("Todo el historial ha sido eliminado.")
            st.info("La página se recargará para reflejar los cambios.")
            conn.close()
            st.rerun()
else:
    st.info("Aún no hay registros guardados. Ve a la página 'Calculadora' para generar y guardar un informe.")
    
# Nos aseguramos de cerrar la conexión si no se ha hecho ya dentro de un if
if conn:
    conn.close()
else:
    st.error("No se pudo conectar a la base de datos.")