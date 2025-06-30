# ui_components.py
import streamlit as st
import plotly.express as px

def ui_perfil_basico():
    """Crea la UI para el Paso 1 y usa st.session_state para guardar los valores."""
    st.markdown("Introduce tus datos básicos. Estos se guardarán automáticamente mientras avanzas.")
    
    st.number_input("Edad", 18, 55, key="edad")
    st.number_input("Duración promedio del ciclo (días)", 20, 90, key="duracion_ciclo")
    
    st.write("**Cálculo del IMC**")
    peso = st.number_input("Peso (kg)", 30.0, 200.0, 65.0, format="%.1f")
    talla = st.number_input("Talla (m)", 1.0, 2.5, 1.65, format="%.2f")

    if talla > 0:
        imc_calculado = peso / (talla ** 2)
        st.info(f"IMC calculado: {imc_calculado:.2f} kg/m²")
        st.session_state.imc = imc_calculado
    else:
        st.session_state.imc = 0

def ui_historial_clinico():
    """Crea la UI para el Paso 2 y usa st.session_state."""
    st.markdown("Información sobre diagnósticos ginecológicos previos.")

    st.radio("¿Diagnóstico de SOP?", ["No", "Sí"], key="sop_radio")
    
    st.radio("¿Diagnóstico de Endometriosis?", ["No", "Sí"], key="endo_radio")
    if st.session_state.endo_radio == 'Sí':
        st.selectbox("Grado de Endometriosis", [1, 2, 3, 4], key="grado_endometriosis")

    st.radio("¿Diagnóstico de Miomatosis?", ["No", "Sí"], key="miomas_radio")
    if st.session_state.miomas_radio == 'Sí':
        st.radio("¿Miomas SUBMUCOSOS?", ["No", "Sí"], key="mioma_submucoso_radio")
        if st.session_state.mioma_submucoso_radio == 'Sí':
            st.radio("¿Son múltiples?", ["No", "Sí"], key="mioma_submucoso_multiple_radio")
        else:
            # Estas opciones solo aparecen si la respuesta a miomas es SÍ y a submucosos es NO
            st.radio("¿Miomas INTRAMURALES ≥ 4cm o que deformen cavidad?", ["No", "Sí"], key="mioma_intramural_radio")
            st.radio("¿Miomas SUBSEROSOS > 6cm?", ["No", "Sí"], key="mioma_subseroso_radio")

    st.radio("¿Diagnóstico de Adenomiosis?", ["No", "Sí"], key="adeno_radio")
    if st.session_state.adeno_radio == 'Sí':
        st.selectbox("Tipo de Adenomiosis", ["focal", "difusa_leve", "difusa_severa"], key="tipo_adenomiosis")
    
    st.radio("¿Diagnóstico de Pólipos?", ["No", "Sí"], key="polipo_radio")
    if st.session_state.polipo_radio == 'Sí':
        st.selectbox("Tipo de Pólipo", ["pequeno_unico", "moderado_multiple", "grande"], key="tipo_polipo")
    
    st.radio("¿Resultado de HSG disponible?", ["No", "Sí"], key="hsg_radio")
    if st.session_state.hsg_radio == 'Sí':
        st.selectbox("Resultado HSG", ["normal", "unilateral", "bilateral", "defecto_uterino"], key="resultado_hsg")

def mostrar_informe_completo(evaluacion):
    """Dibuja el informe completo usando expanders para una mejor organización."""
    # (El código de esta función permanece sin cambios)
    st.header("📋 Tu Informe de Fertilidad Personalizado")
    st.subheader("1. Pronóstico de Concepción por Ciclo")
    st.metric(label="PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")
    st.subheader("2. Análisis Detallado de Factores")
    with st.expander("🔬 Ver desglose de factores evaluados", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("Factores Gineco-Anatómicos")
            st.write(f"* **IMC:** {evaluacion.comentario_imc or 'No reportado'}")
            st.write(f"* **SOP:** {evaluacion.severidad_sop or 'No reportado'}")
            st.write(f"* **Endometriosis:** {evaluacion.comentario_endometriosis or 'No reportada'}")
            st.write(f"* **Miomatosis:** {evaluacion.comentario_miomas or 'No reportada'}")
            st.write(f"* **Adenomiosis:** {evaluacion.comentario_adenomiosis or 'No reportada'}")
            st.write(f"* **Pólipos:** {evaluacion.comentario_polipo or 'No reportados'}")
            st.write(f"* **HSG:** {evaluacion.comentario_hsg or 'No reportada'}")
        with col2:
            st.info("Factores Endocrino-Metabólicos")
            st.write(f"* **Reserva Ovárica (AMH):** {evaluacion.diagnostico_reserva or 'No reportada'}")
            st.write(f"* **Prolactina:** {evaluacion.comentario_prolactina or 'No reportada'}")
            st.write(f"* **Función Tiroidea (TSH):** {evaluacion.comentario_tsh or 'No reportada'}")
            if evaluacion.homa_calculado:
                st.write(f"* **Resistencia a Insulina (HOMA {evaluacion.homa_calculado:.2f}):** {evaluacion.comentario_homa}")
            else:
                st.write("* **Resistencia a Insulina (HOMA):** Datos no proporcionados")
        with col3:
            st.info("Factor Masculino")
            st.write(f"* **Espermatograma:** {evaluacion.diagnostico_masculino_detallado or 'No reportado'}")

    if evaluacion.recomendaciones_lista:
        with st.expander("💡 Ver plan de acción y recomendaciones sugeridas"):
            recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
            for rec in recomendaciones_unicas:
                st.warning(f"• {rec}")
            
    with st.expander("📊 Ver comparativa visual del pronóstico"):
        prob_basal = evaluacion.probabilidad_base_edad_num
        try:
            prob_final = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
            df_probs = {'Tipo de Pronóstico': ['Probabilidad Basal (solo por edad)', 'Pronóstico Ajustado (todos los factores)'], 'Probabilidad (%)': [prob_basal, prob_final]}
            fig = px.bar(df_probs, x='Tipo de Pronóstico', y='Probabilidad (%)', text_auto='.1f', title="Comparativa de Probabilidad de Concepción por Ciclo", color='Tipo de Pronóstico', color_discrete_map={'Probabilidad Basal (solo por edad)': 'royalblue', 'Pronóstico Ajustado (todos los factores)': 'lightcoral'})
            fig.update_layout(yaxis_title="Probabilidad de Embarazo (%)", xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        except (ValueError, TypeError):
            st.error("No se pudo generar el gráfico debido a un resultado de pronóstico no numérico.")