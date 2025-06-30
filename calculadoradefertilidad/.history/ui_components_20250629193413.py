# ui_components.py
import streamlit as st
import plotly.graph_objects as go

def inicializar_session_state():
    """Define los valores iniciales para todos los campos en la memoria de la sesión."""
    # Este diccionario contiene todas las claves y sus valores por defecto.
    defaults = {
        'edad': 30, 'duracion_ciclo': 28, 'imc_peso': 65.0, 'imc_talla': 1.65,
        'tiene_sop': "No", 'tiene_endo': "No", 'grado_endometriosis': 1,
        'tiene_miomas': "No", 'mioma_submucoso': "No", 'mioma_submucoso_multiple': "No",
        'mioma_intramural_significativo': "No", 'mioma_subseroso_grande': "No",
        'tiene_adeno': "No", 'tipo_adenomiosis': "focal", 'tiene_polipo': "No",
        'tipo_polipo': "pequeno_unico", 'tiene_hsg': "No", 'resultado_hsg': "normal",
        'amh': 2.5, 'prolactina': 15.0, 'tsh': 2.0, 'tpo_ab_positivo': "No",
        'insulina_ayunas': 8.0, 'glicemia_ayunas': 90,
        'tiene_esperma': "No", 'volumen_seminal': 2.5, 'concentracion_esperm': 40.0,
        'motilidad_progresiva': 45, 'morfologia_normal': 5, 'vitalidad_esperm': 75
    }
    # Solo inicializa las claves si no existen ya en la sesión.
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def mostrar_formulario_completo():
    """Dibuja el formulario completo en la barra lateral y usa st.session_state para la persistencia de datos."""
    st.sidebar.header("Datos de la Pareja")

    st.sidebar.subheader("1. Perfil Básico Femenino")
    st.sidebar.number_input("Edad", 18, 55, key="edad")
    st.sidebar.number_input("Duración promedio del ciclo (días)", 20, 90, key="duracion_ciclo")
    st.sidebar.write("**Cálculo del IMC**")
    st.sidebar.number_input("Peso (kg)", 30.0, 200.0, key="imc_peso", format="%.1f")
    st.sidebar.number_input("Talla (m)", 1.0, 2.5, key="imc_talla", format="%.2f", help="Introduce tu talla en metros, por ejemplo: 1.65")
    if st.session_state.imc_talla > 0:
        homa_calculado_realtime = st.session_state.imc_peso / (st.session_state.imc_talla ** 2)
        st.sidebar.info(f"IMC calculado: {homa_calculado_realtime:.2f} kg/m²")

    st.sidebar.subheader("2. Historial Clínico y Diagnósticos")
    st.sidebar.radio("¿Diagnóstico de SOP?", ["No", "Sí"], key="tiene_sop")
    st.sidebar.radio("¿Diagnóstico de Endometriosis?", ["No", "Sí"], key="tiene_endo")
    if st.session_state.tiene_endo == "Sí":
        st.sidebar.selectbox("Grado de Endometriosis", [1, 2, 3, 4], key="grado_endometriosis")
    
    st.sidebar.radio("¿Diagnóstico de Miomatosis?", ["No", "Sí"], key="tiene_miomas")
    if st.session_state.tiene_miomas == "Sí":
        st.sidebar.radio("¿Miomas SUBMUCOSOS?", ["No", "Sí"], key="mioma_submucoso")
        if st.session_state.mioma_submucoso == "Sí":
            st.sidebar.radio("¿Son múltiples?", ["No", "Sí"], key="mioma_submucoso_multiple")
        else:
            st.sidebar.radio("¿Miomas INTRAMURALES ≥ 4cm o que deformen cavidad?", ["No", "Sí"], key="mioma_intramural_significativo")
            st.sidebar.radio("¿Miomas SUBSEROSOS > 6cm?", ["No", "Sí"], key="mioma_subseroso_grande")

    st.sidebar.radio("¿Diagnóstico de Adenomiosis?", ["No", "Sí"], key="tiene_adeno")
    if st.session_state.tiene_adeno == "Sí":
        st.sidebar.selectbox("Tipo de Adenomiosis", ["focal", "difusa_leve", "difusa_severa"], key="tipo_adenomiosis")
    
    st.sidebar.radio("¿Diagnóstico de Pólipos?", ["No", "Sí"], key="tiene_polipo")
    if st.session_state.tiene_polipo == "Sí":
        st.sidebar.selectbox("Tipo de Pólipo", ["pequeno_unico", "moderado_multiple", "grande"], key="tipo_polipo")
    
    st.sidebar.radio("¿Resultado de HSG?", ["No", "Sí"], key="tiene_hsg")
    if st.session_state.tiene_hsg == "Sí":
        st.sidebar.selectbox("Resultado HSG", ["normal", "unilateral", "bilateral", "defecto_uterino"], key="hsg_type")

    st.sidebar.subheader("3. Perfil de Laboratorio")
    with st.sidebar.expander("Expandir para Perfil Endocrino y Metabólico"):
        st.number_input("Nivel de AMH (ng/mL)", 0.0, 20.0, format="%.2f", key="amh")
        st.number_input("Nivel de Prolactina (ng/mL)", 0.0, 200.0, format="%.2f", key="prolactina")
        st.number_input("Nivel de TSH (µUI/mL)", 0.0, 10.0, format="%.2f", key="tsh")
        if st.session_state.tsh > 2.5:
            st.radio("¿Anticuerpos TPO positivos?", ["No", "Sí"], key="tpo_ab_positivo")
        st.number_input("Insulina en ayunas (μU/mL)", 1.0, 50.0, format="%.2f", key="insulina_ayunas")
        st.number_input("Glicemia en ayunas (mg/dL)", 50, 200, key="glicemia_ayunas")

    st.sidebar.subheader("4. Factor Masculino")
    st.sidebar.radio("¿Análisis de espermatograma disponible?", ["No", "Sí"], key="tiene_esperma")
    if st.session_state.tiene_esperma == "Sí":
        with st.sidebar.expander("Expandir para Detalle del Espermatograma", expanded=True):
            st.number_input("Volumen (mL)", 0.0, 10.0, format="%.2f", key="volumen_seminal")
            st.number_input("Concentración (millones/mL)", 0.0, 200.0, format="%.2f", key="concentracion_esperm")
            st.number_input("Motilidad progresiva (%)", 0, 100, key="motilidad_progresiva")
            st.number_input("Morfología normal (%)", 0, 100, key="morfologia_normal")
            st.number_input("Vitalidad (%)", 0, 100, key="vitalidad_esperm")

    st.sidebar.write("---")
    submit_button = st.sidebar.button("Generar Informe de Fertilidad Completo")
    return submit_button

def mostrar_grafico_gauge(prob_final):
    """Genera y muestra un gráfico de medidor (gauge)."""
    color = "green"
    if prob_final < 10: color = "red"
    elif prob_final < 20: color = "orange"
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = prob_final,
        title = {'text': "Pronóstico de Concepción (%)"},
        gauge = {'axis': {'range': [None, 35]}, 'bar': {'color': color},
                 'steps' : [{'range': [0, 10], 'color': "rgba(255, 0, 0, 0.2)"}, {'range': [10, 20], 'color': "rgba(255, 165, 0, 0.2)"}]}
    ))
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=60, b=10))
    st.plotly_chart(fig, use_container_width=True)

def mostrar_informe_completo(evaluacion):
    """Dibuja el informe completo en la página principal."""
    st.header("📋 Tu Informe de Fertilidad Personalizado")
    prob_final_num = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
    mostrar_grafico_gauge(prob_final_num)
    
    with st.expander("Ver Resumen de Pronóstico y Factores"):
        st.metric(label="PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")
        st.subheader("Análisis Detallado de Factores")
        col1, col2, col3 = st.columns(3)
        # ... (código para mostrar el detalle de factores)
    
    if evaluacion.recomendaciones_lista:
        st.subheader("Plan de Acción y Recomendaciones Sugeridas")
        recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
        for rec in recomendaciones_unicas:
            st.warning(f"💡 {rec}")