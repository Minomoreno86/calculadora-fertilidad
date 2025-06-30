# pages/02_Historial.py
import streamlit as st
import pandas as pd
from db_manager import crear_conexion, leer_todos_los_registros

# Título de la página
st.set_page_config(page_title="Historial de Evaluaciones", page_icon="📈")
st.title("📈 Historial de Evaluaciones Guardadas")
st.write("Aquí puedes ver todos los perfiles y resultados que has guardado.")

# Conexión a la base de datos
DB_FILE = "fertilidad.db"
conn = crear_conexion(DB_FILE)

if conn is not None:
    # Leer los datos usando nuestra nueva función
    df_registros = leer_todos_los_registros(conn)
    conn.close()
    
    if not df_registros.empty:
        # st.dataframe muestra la tabla de forma interactiva
        st.dataframe(df_registros)
    else:
        st.info("Aún no hay registros guardados. Ve a la calculadora, genera un informe y guárdalo.")
else:
    st.error("No se pudo conectar a la base de datos.")