# En: pages/02_Historial.py

import streamlit as st
import pandas as pd
import plotly.express as px
from db_manager import (
    crear_conexion, 
    leer_todos_los_registros, 
    leer_todos_los_riesgos,
    eliminar_registro_por_id, 
    eliminar_todos_los_registros
)
# ✅ CORRECCIÓN: Importamos desde 'utils'
from utils import aplicar_tema_personalizado

# --- Configuración de la Página ---
st.set_page_config(page_title="Historial de Evaluaciones", page_icon="📈", layout="wide")
# aplicamos el tema al principio si existe en el estado de la sesión
# if 'tema' in st.session_state:
#     aplicar_tema_personalizado()

st.title("📈 Historial de Evaluaciones Guardadas")
st.write("Aquí puedes ver y gestionar todos los perfiles y resultados que has guardado.")

# --- ✅ MEJORA: Gestión centralizada de la conexión a la BD ---
DB_FILE = "fertilidad.db"
conn = crear_conexion(DB_FILE)

def mostrar_pagina_historial(db_connection):
    """Función principal para renderizar toda la página del historial."""
    
    # --- Sección de Pronóstico de Fertilidad ---
    st.header("📊 Evolución del Pronóstico de Fertilidad")
    df_registros = leer_todos_los_registros(db_connection)
    
    if not df_registros.empty:
        df_registros['timestamp'] = pd.to_datetime(df_registros['timestamp']).dt.date
        df_registros = df_registros.sort_values(by='timestamp')
        
        fig_pronostico = px.line(
            df_registros, x='timestamp', y='pronostico_final',
            title='Pronóstico a lo Largo del Tiempo', markers=True,
            labels={'timestamp': 'Fecha', 'pronostico_final': 'Pronóstico (%)'}
        )
        st.plotly_chart(fig_pronostico, use_container_width=True)
        with st.expander("Ver datos de pronóstico"):
            st.dataframe(df_registros)
    else:
        st.info("No hay evaluaciones de pronóstico guardadas.")

    st.divider()

    # --- Sección de Riesgo de Aborto ---
    st.header("📉 Evolución del Riesgo de Aborto")
    df_riesgos = leer_todos_los_riesgos(db_connection)

    if not df_riesgos.empty:
        df_riesgos['timestamp'] = pd.to_datetime(df_riesgos['timestamp']).dt.date
        df_riesgos = df_riesgos.sort_values(by='timestamp')

        fig_riesgo = px.line(
            df_riesgos, x='timestamp', y='riesgo_final',
            title='Riesgo de Aborto a lo Largo del Tiempo', markers=True,
            labels={'timestamp': 'Fecha', 'riesgo_final': 'Riesgo Estimado (%)'}
        )
        fig_riesgo.update_traces(line=dict(color='red'))
        st.plotly_chart(fig_riesgo, use_container_width=True)
        with st.expander("Ver datos de riesgo"):
            st.dataframe(df_riesgos)
    else:
        st.info("No hay evaluaciones de riesgo de aborto registradas.")

    st.divider()
    
    # --- Sección de Gestión de Datos (solo si hay registros) ---
    if not df_registros.empty:
        st.header("🗑️ Gestionar Historial")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Borrar un registro específico")
            # Creamos etiquetas amigables para el selectbox
            opciones = [f"ID: {row['id']} - Fecha: {row['timestamp']}" for index, row in df_registros.iterrows()]
            seleccion = st.selectbox("Selecciona el registro a eliminar:", opciones)
            
            if st.button("Eliminar Registro Seleccionado"):
                id_a_borrar = int(seleccion.split(" ")[1])
                eliminar_registro_por_id(db_connection, id_a_borrar)
                st.success(f"Registro con ID {id_a_borrar} eliminado.")
                st.rerun()

        with col2:
            st.markdown("##### Borrar todo el historial")
            if st.button("🚨 Eliminar TODO el Historial", type="primary", help="Esta acción no se puede deshacer."):
                eliminar_todos_los_registros(db_connection)
                st.success("Todo el historial ha sido eliminado.")
                st.rerun()

# --- Lógica Principal ---
if conn is not None:
    try:
        mostrar_pagina_historial(conn)
    finally:
        # Nos aseguramos de cerrar la conexión sin importar lo que pase
        conn.close()
else:
    st.error("No se pudo conectar a la base de datos.")
