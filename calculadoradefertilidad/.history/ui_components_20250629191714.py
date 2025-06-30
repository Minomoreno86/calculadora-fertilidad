# ui_components.py
import streamlit as st
import plotly.express as px

def mostrar_formulario_completo():
    """
    Dibuja el formulario completo en la barra lateral y devuelve todos los datos ingresados.
    """
    st.sidebar.header("Datos de la Pareja")
    
    # DICCIONARIO PARA GUARDAR TODOS LOS INPUTS
    inputs = {}

    # --- Sección 1: Datos Femeninos Básicos ---
    st.sidebar.subheader("1. Perfil Básico Femenino")
    inputs['edad'] = st.sidebar.number_input("Edad", 18, 55, 30)
    inputs['duracion_ciclo'] = st.sidebar.number_input("Duración promedio del ciclo (días)", 20, 90, 28)
    inputs['imc'] = st.sidebar.number_input("Índice de Masa Corporal (IMC)", 15.0, 50.0, 22.5, format="%.2f")

    # --- Sección 2: Historial Clínico y Diagnósticos ---
    st.sidebar.subheader("2. Historial Clínico y Diagnósticos")
    inputs['tiene_sop'] = (st.sidebar.radio("¿Diagnóstico de SOP?", ["No", "Sí"], key="sop") == "Sí")
    
    tiene_endo = (st.sidebar.radio("¿Diagnóstico de Endometriosis?", ["No", "Sí"], key="endo") == "Sí")
    inputs['grado_endometriosis'] = st.sidebar.selectbox("Grado de Endometriosis", [1, 2, 3, 4], key="endo_grade") if tiene_endo else 0

    # Lógica guiada para Miomas
    inputs['tiene_miomas'] = (st.sidebar.radio("¿Diagnóstico de Miomatosis?", ["No", "Sí"], key="miomas") == "Sí")
    if inputs['tiene_miomas']:
        inputs['mioma_submucoso'] = (st.sidebar.radio("¿Miomas SUBMUCOSOS?", ["No", "Sí"], key="subm") == "Sí")
        if inputs['mioma_submucoso']:
            inputs['mioma_submucoso_multiple'] = (st.sidebar.radio("¿Son múltiples?", ["No", "Sí"], key="subm_mult") == "Sí")
            inputs['mioma_intramural_significativo'], inputs['mioma_subseroso_grande'] = False, False
        else:
            inputs['mioma_intramural_significativo'] = (st.sidebar.radio("¿Miomas INTRAMURALES ≥ 4cm o que deformen cavidad?", ["No", "Sí"], key="intra") == "Sí")
            inputs['mioma_subseroso_grande'] = (st.sidebar.radio("¿Miomas SUBSEROSOS > 6cm?", ["No", "Sí"], key="subs") == "Sí")
            inputs['mioma_submucoso_multiple'] = False
    else:
        inputs['mioma_submucoso'], inputs['mioma_submucoso_multiple'], inputs['mioma_intramural_significativo'], inputs['mioma_subseroso_grande'] = False, False, False, False

    tiene_adeno = (st.sidebar.radio("¿Diagnóstico de Adenomiosis?", ["No", "Sí"], key="adeno") == "Sí")
    inputs['tipo_adenomiosis'] = st.sidebar.selectbox("Tipo de Adenomiosis", ["focal", "difusa_leve", "difusa_severa"], key="adeno_type") if tiene_adeno else ""
    
    tiene_polipo = (st.sidebar.radio("¿Diagnóstico de Pólipos?", ["No", "Sí"], key="polipo") == "Sí")
    inputs['tipo_polipo'] = st.sidebar.selectbox("Tipo de Pólipo", ["pequeno_unico", "moderado_multiple", "grande"], key="polipo_type") if tiene_polipo else ""
    
    tiene_hsg = (st.sidebar.radio("¿Resultado de HSG?", ["No", "Sí"], key="hsg") == "Sí")
    inputs['resultado_hsg'] = st.sidebar.selectbox("Resultado HSG", ["normal", "unilateral", "bilateral", "defecto_uterino"], key="hsg_type") if tiene_hsg else ""

    # --- Sección 3: Pruebas de Laboratorio ---
    st.sidebar.subheader("3. Perfil de Laboratorio")
    with st.sidebar.expander("Expandir para Perfil Endocrino y Metabólico"):
        inputs['amh'] = st.number_input("Nivel de AMH (ng/mL)", 0.0, 20.0, 2.5, format="%.2f")
        inputs['prolactina'] = st.number_input("Nivel de Prolactina (ng/mL)", 0.0, 200.0, 15.0, format="%.2f")
        tsh = st.number_input("Nivel de TSH (µUI/mL)", 0.0, 10.0, 2.0, format="%.2f")
        inputs['tsh'] = tsh
        inputs['tpo_ab_positivo'] = (st.radio("¿Anticuerpos TPO positivos?", ["No", "Sí"], key="tpo") == "Sí") if tsh > 2.5 else False
        inputs['insulina_ayunas'] = st.number_input("Insulina en ayunas (μU/mL)", 1.0, 50.0, 8.0, format="%.2f")
        inputs['glicemia_ayunas'] = st.number_input("Glicemia en ayunas (mg/dL)", 50, 200, 90)

    # --- Sección 4: Factor Masculino ---
    st.sidebar.subheader("4. Factor Masculino")
    tiene_esperma = (st.sidebar.radio("¿Análisis de espermatograma disponible?", ["No", "Sí"], key="esperma") == "Sí")
    if tiene_esperma:
        with st.sidebar.expander("Expandir para Detalle del Espermatograma", expanded=True):
            inputs['volumen_seminal'] = st.number_input("Volumen (mL)", 0.0, 10.0, 2.5, format="%.2f")
            inputs['concentracion_esperm'] = st.number_input("Concentración (millones/mL)", 0.0, 200.0, 40.0, format="%.2f")
            inputs['motilidad_progresiva'] = st.number_input("Motilidad progresiva (%)", 0, 100, 45)
            inputs['morfologia_normal'] = st.number_input("Morfología normal (%)", 0, 100, 5)
            inputs['vitalidad_esperm'] = st.number_input("Vitalidad (%)", 0, 100, 75)
    else:
        keys = ['volumen_seminal', 'concentracion_esperm', 'motilidad_progresiva', 'morfologia_normal', 'vitalidad_esperm']
        for key in keys:
            inputs[key] = None

    # --- Botón de Cálculo ---
    st.sidebar.write("---")
    inputs['submit_button'] = st.sidebar.button("Generar Informe de Fertilidad Completo")
    
    return inputs

def mostrar_informe_completo(evaluacion):
    """
    Dibuja el informe completo en la página principal a partir de un objeto de evaluación.
    """
    st.header("📋 Tu Informe de Fertilidad Personalizado")
    st.subheader("1. Pronóstico de Concepción por Ciclo")
    st.metric(label="PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")

    st.subheader("2. Análisis Detallado de Factores")
    col1, col2, col3 = st.columns(3)
    with col1: st.info("Factores Gineco-Anatómicos"); st.write(f"* **IMC:** {evaluacion.comentario_imc}"); st.write(f"* **SOP:** {evaluacion.severidad_sop}"); st.write(f"* **Endometriosis:** {evaluacion.comentario_endometriosis or 'No reportada'}"); st.write(f"* **Miomatosis:** {evaluacion.comentario_miomas or 'No reportada'}"); st.write(f"* **Adenomiosis:** {evaluacion.comentario_adenomiosis or 'No reportada'}"); st.write(f"* **Pólipos:** {evaluacion.comentario_polipo or 'No reportados'}"); st.write(f"* **HSG:** {evaluacion.comentario_hsg or 'No reportada'}")
    with col2: st.info("Factores Endocrino-Metabólicos"); st.write(f"* **Reserva Ovárica (AMH):** {evaluacion.diagnostico_reserva}"); st.write(f"* **Prolactina:** {evaluacion.comentario_prolactina or 'No reportada'}"); st.write(f"* **Función Tiroidea (TSH):** {evaluacion.comentario_tsh or 'No reportada'}"); 
    if evaluacion.homa_calculado: st.write(f"* **Resistencia a Insulina (HOMA {evaluacion.homa_calculado:.2f}):** {evaluacion.comentario_homa}")
    else: st.write("* **Resistencia a Insulina (HOMA):** Datos no proporcionados")
    with col3: st.info("Factor Masculino"); st.write(f"* **Espermatograma:** {evaluacion.diagnostico_masculino_detallado}")

    if evaluacion.recomendaciones_lista:
        st.subheader("3. Plan de Acción y Recomendaciones Sugeridas")
        recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
        for rec in recomendaciones_unicas: st.warning(f"💡 {rec}")