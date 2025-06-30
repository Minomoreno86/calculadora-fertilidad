# app.py

import streamlit as st
from calculadora_fertilidad import EvaluacionFertilidad

# --- Configuración de la Página Web ---
st.set_page_config(
    page_title="Calculadora de Fertilidad Pro",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Título y Descripción ---
st.title("Calculadora Profesional de Fertilidad 👶")
st.write(
    "Esta herramienta, creada con el conocimiento de un especialista, evalúa el pronóstico de fertilidad de una pareja "
    "basado en un modelo multifactorial completo."
)

# ===================================================================
# PARTE 3: ENTRADA DE DATOS (REESTRUCTURADA PARA MEJOR UX)
# ===================================================================

st.sidebar.header("Por favor, introduce tus datos:")

# --- Controles Principales (Fuera del formulario para interactividad instantánea) ---
st.sidebar.subheader("1. Diagnósticos Previos")
tiene_sop = (st.sidebar.radio("¿Diagnóstico de SOP?", ["No", "Sí"]) == "Sí")
tiene_endo = (st.sidebar.radio("¿Diagnóstico de Endometriosis?", ["No", "Sí"]) == "Sí")
tiene_miomas = (st.sidebar.radio("¿Diagnóstico de Miomatosis Uterina?", ["No", "Sí"]) == "Sí")
tiene_adeno = (st.sidebar.radio("¿Diagnóstico de Adenomiosis?", ["No", "Sí"]) == "Sí")
tiene_polipo = (st.sidebar.radio("¿Diagnóstico de Pólipos Endometriales?", ["No", "Sí"]) == "Sí")
tiene_hsg = (st.sidebar.radio("¿Resultado de Histerosalpingografía (HSG)?", ["No", "Sí"]) == "Sí")
tiene_esperma = (st.sidebar.radio("¿La pareja tiene un análisis de espermatograma?", ["No", "Sí"]) == "Sí")


# --- Formulario para el resto de los datos ---
with st.sidebar.form("data_input_form"):
    
    # --- Datos que siempre son visibles ---
    st.subheader("2. Datos y Mediciones")
    with st.expander("Datos Básicos Femeninos", expanded=True):
        edad = st.number_input("Edad", 18, 55, 30)
        duracion_ciclo = st.number_input("Duración promedio del ciclo (días)", 20, 90, 28)
        imc = st.number_input("Índice de Masa Corporal (IMC)", 15.0, 50.0, 22.5, format="%.2f")

    # --- Secciones condicionales que ahora aparecerán al instante ---
    if tiene_endo:
        with st.expander("Detalle de Endometriosis", expanded=True):
            grado_endometriosis = st.selectbox("Grado de Endometriosis", [1, 2, 3, 4])
    else:
        grado_endometriosis = 0

    if tiene_miomas:
        with st.expander("Detalle de Miomatosis", expanded=True):
            mioma_submucoso = (st.radio("¿Existen miomas SUBMUCOSOS?", ["No", "Sí"]) == "Sí")
            if mioma_submucoso:
                mioma_submucoso_multiple = (st.radio("¿Son múltiples los miomas submucosos?", ["No", "Sí"]) == "Sí")
                mioma_intramural_significativo, mioma_subseroso_grande = False, False
            else:
                mioma_intramural_significativo = (st.radio("¿Hay miomas INTRAMURALES ≥ 4cm o que deformen cavidad?", ["No", "Sí"]) == "Sí")
                mioma_subseroso_grande = (st.radio("¿Hay miomas SUBSEROSOS > 6cm?", ["No", "Sí"]) == "Sí")
                mioma_submucoso_multiple = False
    else:
        mioma_submucoso, mioma_submucoso_multiple, mioma_intramural_significativo, mioma_subseroso_grande = False, False, False, False

    if tiene_adeno:
        with st.expander("Detalle de Adenomiosis", expanded=True):
            tipo_adenomiosis = st.selectbox("Tipo de Adenomiosis", ["focal", "difusa_leve", "difusa_severa"])
    else:
        tipo_adenomiosis = ""

    if tiene_polipo:
        with st.expander("Detalle de Pólipos", expanded=True):
            tipo_polipo = st.selectbox("Tipo de Pólipo", ["pequeno_unico", "moderado_multiple", "grande"])
    else:
        tipo_polipo = ""
    
    if tiene_hsg:
        with st.expander("Detalle de HSG", expanded=True):
            resultado_hsg = st.selectbox("Resultado HSG", ["normal", "unilateral", "bilateral", "defecto_uterino"])
    else:
        resultado_hsg = ""
        
    with st.expander("Perfil Endocrino y Metabólico"):
        amh = st.number_input("Nivel de AMH (ng/mL)", 0.0, 20.0, 2.5, format="%.2f")
        prolactina = st.number_input("Nivel de Prolactina (ng/mL)", 0.0, 200.0, 15.0, format="%.2f")
        tsh = st.number_input("Nivel de TSH (µUI/mL)", 0.0, 10.0, 2.0, format="%.2f")
        tpo_ab_positivo = (st.radio("¿Anticuerpos TPO positivos?", ["No", "Sí"]) == "Sí") if tsh > 2.5 else False
        insulina_ayunas = st.number_input("Insulina en ayunas (μU/mL)", 0.0, 50.0, 8.0, format="%.2f")
        glicemia_ayunas = st.number_input("Glicemia en ayunas (mg/dL)", 50, 200, 90)

    if tiene_esperma:
        with st.expander("Detalle del Espermatograma", expanded=True):
            volumen_seminal = st.number_input("Volumen (mL)", 0.0, 10.0, 2.5, format="%.2f")
            concentracion_esperm = st.number_input("Concentración (millones/mL)", 0.0, 200.0, 40.0, format="%.2f")
            motilidad_progresiva = st.number_input("Motilidad progresiva (%)", 0, 100, 45)
            morfologia_normal = st.number_input("Morfología normal (%)", 0, 100, 5)
            vitalidad_esperm = st.number_input("Vitalidad (%)", 0, 100, 75)
    else:
        volumen_seminal, concentracion_esperm, motilidad_progresiva, morfologia_normal, vitalidad_esperm = None, None, None, None, None

    # Botón de envío del formulario
    submitted = st.form_submit_button("Generar Informe de Fertilidad Completo")

# ===================================================================
# PARTE 4: LÓGICA Y VISUALIZACIÓN DE RESULTADOS
# ===================================================================
if submitted:
    with st.spinner("Realizando evaluación completa con el motor clínico..."):
        miomas_dict = {
            'tiene_miomas': tiene_miomas, 'mioma_submucoso': mioma_submucoso, 
            'mioma_submucoso_multiple': mioma_submucoso_multiple,
            'mioma_intramural_significativo': mioma_intramural_significativo, 
            'mioma_subseroso_grande': mioma_subseroso_grande
        }
        evaluacion = EvaluacionFertilidad(
            edad=edad, duracion_ciclo=duracion_ciclo, imc=imc, amh=amh, prolactina=prolactina, tsh=tsh, 
            tpo_ab_positivo=tpo_ab_positivo, insulina_ayunas=insulina_ayunas, glicemia_ayunas=glicemia_ayunas,
            tiene_sop=tiene_sop, grado_endometriosis=grado_endometriosis,
            tipo_adenomiosis=tipo_adenomiosis, tipo_polipo=tipo_polipo, resultado_hsg=resultado_hsg,
            volumen_seminal=volumen_seminal, concentracion_esperm=concentracion_esperm, motilidad_progresiva=motilidad_progresiva,
            morfologia_normal=morfologia_normal, vitalidad_esperm=vitalidad_esperm,
            **miomas_dict
        )
        evaluacion.ejecutar_evaluacion()

    st.header("📋 Tu Informe de Fertilidad Personalizado")
    # ... (El código para mostrar el informe es el mismo de la lección anterior)
    st.subheader("1. Pronóstico de Concepción por Ciclo")
    st.metric(label="PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")
    st.subheader("2. Análisis Detallado de Factores")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Factores Gineco-Anatómicos"); st.write(f"* **IMC:** {evaluacion.comentario_imc}"); st.write(f"* **SOP:** {evaluacion.severidad_sop}"); st.write(f"* **Endometriosis:** {evaluacion.comentario_endometriosis or 'No reportada'}"); st.write(f"* **Miomatosis:** {evaluacion.comentario_miomas or 'No reportada'}"); st.write(f"* **Adenomiosis:** {evaluacion.comentario_adenomiosis or 'No reportada'}"); st.write(f"* **Pólipos:** {evaluacion.comentario_polipo or 'No reportados'}"); st.write(f"* **HSG:** {evaluacion.comentario_hsg or 'No reportada'}")
    with col2:
        st.info("Factores Endocrino-Metabólicos"); st.write(f"* **Reserva Ovárica (AMH):** {evaluacion.diagnostico_reserva}"); st.write(f"* **Prolactina:** {evaluacion.comentario_prolactina or 'No reportada'}"); st.write(f"* **Función Tiroidea (TSH):** {evaluacion.comentario_tsh or 'No reportada'}"); 
        if evaluacion.homa_calculado: st.write(f"* **Resistencia a Insulina (HOMA {evaluacion.homa_calculado:.2f}):** {evaluacion.comentario_homa}")
        else: st.write("* **Resistencia a Insulina (HOMA):** Datos no proporcionados")
    with col3:
        st.info("Factor Masculino"); st.write(f"* **Espermatograma:** {evaluacion.diagnostico_masculino_detallado}")
    if evaluacion.recomendaciones_lista:
        st.subheader("3. Plan de Acción y Recomendaciones Sugeridas")
        recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
        for rec in recomendaciones_unicas: st.warning(f"💡 {rec}")

else:
    st.info("⬅️ Por favor, responde a las preguntas iniciales y completa los datos en el formulario para generar tu informe.")