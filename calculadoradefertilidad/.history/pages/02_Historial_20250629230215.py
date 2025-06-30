import streamlit as st; import pandas as pd; import plotly.express as px
from db_manager import crear_conexion, leer_todos_los_registros, eliminar_registro_por_id, eliminar_todos_los_registros

st.set_page_config(page_title="Historial de Evaluaciones", page_icon="📈", layout="wide")
st.title("📈 Historial de Evaluaciones Guardadas")
st.write("Aquí puedes ver y gestionar todos los perfiles y resultados que has guardado.")

DB_FILE = "fertilidad.db"; conn = crear_conexion(DB_FILE)
if conn is not None:
    df_registros = leer_todos_los_registros(conn)
    if not df_registros.empty:
        df_registros['timestamp'] = pd.to_datetime(df_registros['timestamp'])
        df_registros = df_registros.sort_values(by='timestamp')
        st.divider(); st.subheader("📊 Evolución del Pronóstico")
        fig = px.line(df_registros, x='timestamp', y='pronostico_final', title='Evolución del Pronóstico de Fertilidad a lo Largo del Tiempo', markers=True, labels={'timestamp': 'Fecha de Registro', 'pronostico_final': 'Pronóstico de Embarazo (%)'})
        fig.update_traces(line=dict(color='royalblue', width=3)); fig.update_layout(yaxis_title="Pronóstico de Embarazo (%)"); st.plotly_chart(fig, use_container_width=True)
        st.divider();
        with st.expander("Ver todos los datos guardados en formato de tabla"): st.dataframe(df_registros)
        st.divider(); st.subheader("🗑️ Gestionar Historial")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Borrar un registro específico")
            lista_ids = df_registros['id'].tolist(); id_a_borrar = st.selectbox("Selecciona el ID del registro a eliminar:", lista_ids)
            if st.button("Eliminar Registro Seleccionado"):
                eliminar_registro_por_id(conn, id_a_borrar); st.success(f"Registro con ID {id_a_borrar} eliminado."); conn.close(); st.rerun()
        with col2:
            st.markdown("##### Borrar todo el historial")
            if st.button("🚨 Eliminar TODO el Historial", type="primary"):
                eliminar_todos_los_registros(conn); st.success("Todo el historial ha sido eliminado."); conn.close(); st.rerun()
    else:
        st.info("Aún no hay registros guardados. Ve a la página 'Calculadora' para generar y guardar un informe.")
    if conn: conn.close()
else: st.error("No se pudo conectar a la base de datos.")