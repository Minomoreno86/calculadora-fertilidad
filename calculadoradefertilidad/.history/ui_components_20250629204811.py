# ui_components.py
import streamlit as st
import plotly.express as px

# ===================================================================
# PARTE 1: SUB-FUNCIONES MODULARES PARA EL FORMULARIO
# La estructura modular se mantiene porque es una buena práctica.
# ===================================================================

def _mostrar_datos_basicos(inputs):
    """Muestra la sección de perfil básico femenino."""
    st.subheader("1. Perfil Básico Femenino")
    inputs['edad'] = st.number_input("Edad", 18, 55, 30)
    inputs['duracion_ciclo'] = st.number_input("Duración promedio del ciclo (días)", 20, 90, 28)
    
    st.write("**Cálculo del IMC**")
    peso = st.number_input("Peso (kg)", 30.0, 200.0, 65.0, format="%.1f")
    talla = st.number_input("Talla (m)", 1.0, 2.5, 1.65, format="%.2f", help="Introduce tu talla en metros, por ejemplo: 1.65")

    if talla > 0:
        imc_calculado = peso / (talla ** 2)
        st.info(f"IMC calculado: {imc_calculado:.2f} kg/m²")
        inputs['imc'] = imc_calculado
    else:
        inputs['imc'] = 0

def _mostrar_historial_clinico(inputs):
    """Muestra la sección de historial clínico con lógica 'if' para interactividad."""
    st.subheader("2. Historial Clínico y Diagnósticos")
    inputs['tiene_sop'] = (st.radio("¿Diagnóstico de SOP?", ["No", "Sí"], key="sop") == "Sí")
    
    tiene_endo = (st.radio("¿Diagnóstico de Endometriosis?", ["No", "Sí"], key="endo") == "Sí")
    # LÓGICA 'if' RESTAURADA: El widget solo se crea si la condición es True
    if tiene_endo:
        inputs['grado_endometriosis'] = st.selectbox("Grado de Endometriosis", [1, 2, 3, 4], key="endo_grade")
    else:
        inputs['grado_endometriosis'] = 0 # Aseguramos que la clave exista siempre

    inputs['tiene_miomas'] = (st.radio("¿Diagnóstico de Miomatosis?", ["No", "Sí"], key="miomas") == "Sí")
    # LÓGICA 'if' RESTAURADA
    if inputs['tiene_miomas']:
        inputs['mioma_submucoso'] = (st.radio("¿Miomas SUBMUCOSOS?", ["No", "Sí"], key="subm") == "Sí")
        if inputs['mioma_submucoso']:
            inputs['mioma_submucoso_multiple'] = (st.radio("¿Son múltiples?", ["No", "Sí"], key="subm_mult") == "Sí")
            inputs['mioma_intramural_significativo'], inputs['mioma_subseroso_grande'] = False, False
        else:
            inputs['mioma_intramural_significativo'] = (st.radio("¿Miomas INTRAMURALES ≥ 4cm o que deformen cavidad?", ["No", "Sí"], key="intra") == "Sí")
            inputs['mioma_subseroso_grande'] = (st.radio("¿Miomas SUBSEROSOS > 6cm?", ["No", "Sí"], key="subs") == "Sí")
            inputs['mioma_submucoso_multiple'] = False
    else:
        inputs['mioma_submucoso'], inputs['mioma_submucoso_multiple'], inputs['mioma_intramural_significativo'], inputs['mioma_subseroso_grande'] = False, False, False, False

    tiene_adeno = (st.radio("¿Diagnóstico de Adenomiosis?", ["No", "Sí"], key="adeno") == "Sí")
    if tiene_adeno:
        inputs['tipo_adenomiosis'] = st.selectbox("Tipo de Adenomiosis", ["focal", "difusa_leve", "difusa_severa"], key="adeno_type")
    else:
        inputs['tipo_adenomiosis'] = ""
    
    tiene_polipo = (st.radio("¿Diagnóstico de Pólipos?", ["No", "Sí"], key="polipo") == "Sí")
    if tiene_polipo:
        inputs['tipo_polipo'] = st.selectbox("Tipo de Pólipo", ["pequeno_unico", "moderado_multiple", "grande"], key="polipo_type")
    else:
        inputs['tipo_polipo'] = ""
    
    tiene_hsg = (st.radio("¿Resultado de HSG disponible?", ["No", "Sí"], key="hsg") == "Sí")
    if tiene_hsg:
        inputs['resultado_hsg'] = st.selectbox("Resultado HSG", ["normal", "unilateral", "bilateral", "defecto_uterino"], key="hsg_type")
    else:
        inputs['resultado_hsg'] = ""

def _mostrar_laboratorio(inputs):
    """Muestra la sección de pruebas de laboratorio."""
    st.subheader("3. Perfil de Laboratorio")
    with st.expander("Expandir para Perfil Endocrino y Metabólico"):
        inputs['amh'] = st.number_input("Nivel de AMH (ng/mL)", 0.0, 20.0, 2.5, format="%.2f")
        inputs['prolactina'] = st.number_input("Nivel de Prolactina (ng/mL)", 0.0, 200.0, 15.0, format="%.2f")
        tsh = st.number_input("Nivel de TSH (µUI/mL)", 0.0, 10.0, 2.0, format="%.2f")
        inputs['tsh'] = tsh
        if tsh > 2.5: # El widget TPO solo aparece si TSH es relevante
            inputs['tpo_ab_positivo'] = (st.radio("¿Anticuerpos TPO positivos?", ["No", "Sí"], key="tpo") == "Sí")
        else:
            inputs['tpo_ab_positivo'] = False
        inputs['insulina_ayunas'] = st.number_input("Insulina en ayunas (μU/mL)", 1.0, 50.0, 8.0, format="%.2f")
        inputs['glicemia_ayunas'] = st.number_input("Glicemia en ayunas (mg/dL)", 50, 200, 90)

def _mostrar_factor_masculino(inputs):
    """Muestra la sección de factor masculino."""
    st.subheader("4. Factor Masculino")
    tiene_esperma = (st.radio("¿Análisis de espermatograma disponible?", ["No", "Sí"], key="esperma") == "Sí")
    if tiene_esperma:
        with st.expander("Expandir para Detalle del Espermatograma", expanded=True):
            inputs['volumen_seminal'] = st.number_input("Volumen (mL)", 0.0, 10.0, 2.5, format="%.2f")
            inputs['concentracion_esperm'] = st.number_input("Concentración (millones/mL)", 0.0, 200.0, 40.0, format="%.2f")
            inputs['motilidad_progresiva'] = st.number_input("Motilidad progresiva (%)", 0, 100, 45)
            inputs['morfologia_normal'] = st.number_input("Morfología normal (%)", 0, 100, 5)
            inputs['vitalidad_esperm'] = st.number_input("Vitalidad (%)", 0, 100, 75)
    else:
        keys = ['volumen_seminal', 'concentracion_esperm', 'motilidad_progresiva', 'morfologia_normal', 'vitalidad_esperm']
        for key in keys:
            inputs[key] = None

# ===================================================================
# PARTE 2: FUNCIÓN PRINCIPAL DEL FORMULARIO (Orquestador)
# SIN st.form PARA PERMITIR INTERACTIVIDAD INMEDIATA
# ===================================================================

def mostrar_formulario_completo():
    """Dibuja el formulario completo en la barra lateral y devuelve los datos."""
    
    with st.sidebar:
        st.header("Datos de la Pareja")
        inputs = {}
        
        # Llamamos a nuestras sub-funciones modulares en orden
        _mostrar_datos_basicos(inputs)
        _mostrar_historial_clinico(inputs)
        _mostrar_laboratorio(inputs)
        _mostrar_factor_masculino(inputs)
        
        st.write("---")
        
        # Usamos un botón normal. Su estado será True solo en la re-ejecución inmediata después de hacer clic.
        submit_button = st.button(label="Generar Informe de Fertilidad Completo")

    inputs['submit_button'] = submit_button
    return inputs

# ===================================================================
# PARTE 3: FUNCIÓN PARA MOSTRAR EL INFORME (Sin Cambios)
# ===================================================================

def mostrar_informe_completo(evaluacion):
    # (El código de esta función permanece exactamente igual)
    # ...
    st.header("📋 Tu Informe de Fertilidad Personalizado")
    st.subheader("1. Pronóstico de Concepción por Ciclo")
    st.metric(label="PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")
    st.subheader("2. Análisis Detallado de Factores")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Factores Gineco-Anatómicos")
        st.write(f"* **IMC:** {evaluacion.comentario_imc}")
        st.write(f"* **SOP:** {evaluacion.severidad_sop}")
        st.write(f"* **Endometriosis:** {evaluacion.comentario_endometriosis or 'No reportada'}")
        st.write(f"* **Miomatosis:** {evaluacion.comentario_miomas or 'No reportada'}")
        st.write(f"* **Adenomiosis:** {evaluacion.comentario_adenomiosis or 'No reportada'}")
        st.write(f"* **Pólipos:** {evaluacion.comentario_polipo or 'No reportados'}")
        st.write(f"* **HSG:** {evaluacion.comentario_hsg or 'No reportada'}")
    with col2:
        st.info("Factores Endocrino-Metabólicos")
        st.write(f"* **Reserva Ovárica (AMH):** {evaluacion.diagnostico_reserva}")
        st.write(f"* **Prolactina:** {evaluacion.comentario_prolactina or 'No reportada'}")
        st.write(f"* **Función Tiroidea (TSH):** {evaluacion.comentario_tsh or 'No reportada'}")
        if evaluacion.homa_calculado:
            st.write(f"* **Resistencia a Insulina (HOMA {evaluacion.homa_calculado:.2f}):** {evaluacion.comentario_homa}")
        else:
            st.write("* **Resistencia a Insulina (HOMA):** Datos no proporcionados")
    with col3:
        st.info("Factor Masculino")
        st.write(f"* **Espermatograma:** {evaluacion.diagnostico_masculino_detallado}")
    if evaluacion.recomendaciones_lista:
        st.subheader("3. Plan de Acción y Recomendaciones Sugeridas")
        recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
        for rec in recomendaciones_unicas:
            st.warning(f"💡 {rec}")
    st.subheader("4. Comparativa Visual del Pronóstico")
    prob_basal = evaluacion.probabilidad_base_edad_num
    try:
        prob_final = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
        df_probs = {'Tipo de Pronóstico': ['Probabilidad Basal (solo por edad)', 'Pronóstico Ajustado (todos los factores)'], 'Probabilidad (%)': [prob_basal, prob_final]}
        fig = px.bar(df_probs, x='Tipo de Pronóstico', y='Probabilidad (%)', text_auto='.1f', title="Comparativa de Probabilidad de Concepción por Ciclo", color='Tipo de Pronóstico', color_discrete_map={'Probabilidad Basal (solo por edad)': 'royalblue', 'Pronóstico Ajustado (todos los factores)': 'lightcoral'})
        fig.update_layout(yaxis_title="Probabilidad de Embarazo (%)", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
    except (ValueError, TypeError):
        st.error("No se pudo generar el gráfico debido a un resultado de pronóstico no numérico.")