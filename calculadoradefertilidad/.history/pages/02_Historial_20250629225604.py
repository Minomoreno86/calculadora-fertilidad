# pages/02_Historial.py
import streamlit as st
import pandas as pd
import plotly.express as px
from db_manager import crear_conexion, leer_todos_los_registros

# --- Configuración de la Página ---
st.set_page_config(page_title="Historial de Evaluaciones", page_icon="📈", layout="wide")
st.title("📈 Historial de Evaluaciones Guardadas")
st.write("Aquí puedes ver todos los perfiles y resultados que has guardado y su evolución en el tiempo.")

# --- Conexión y Lectura de Datos ---
DB_FILE = "fertilidad.db"
conn = crear_conexion(DB_FILE)

if conn is not None:
    df_registros = leer_todos_los_registros(conn)
    conn.close()
    
    if not df_registros.empty:
        # --- NUEVO: Procesamiento de Datos ---
        # 1. Convertir la columna de texto a un formato de fecha y hora real
        df_registros['timestamp'] = pd.to_datetime(df_registros['timestamp'])
        
        # 2. Ordenar el dataframe por fecha para que el gráfico tenga sentido
        df_registros = df_registros.sort_values(by='timestamp')

        st.divider()
        
        # --- NUEVO: Gráfico de Evolución ---
        st.subheader("📊 Evolución del Pronóstico")
        
        fig = px.line(
            df_registros,
            x='timestamp',
            y='pronostico_final',
            title='Evolución del Pronóstico de Fertilidad a lo Largo del Tiempo',
            markers=True,  # Añade puntos en cada registro para mayor claridad
            labels={'timestamp': 'Fecha de Registro', 'pronostico_final': 'Pronóstico de Embarazo (%)'}
        )
        
        fig.update_traces(line=dict(color='royalblue', width=3))
        fig.update_layout(yaxis_title="Pronóstico de Embarazo (%)")
        
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # La tabla de datos ahora está dentro de un expander para no ocupar tanto espacio
        with st.expander("Ver todos los datos guardados en formato de tabla"):
            st.dataframe(df_registros)
            
    else:
        st.info("Aún no hay registros guardados. Ve a la página 'Calculadora', genera un informe y guárdalo.")
else:
    st.error("No se pudo conectar a la base de datos.")