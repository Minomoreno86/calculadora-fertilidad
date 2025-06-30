# app.py

import streamlit as st
from calculadora_fertilidad import EvaluacionFertilidad
# El archivo de textos no lo usamos aquí directamente, pero es necesario para que 'calculadora_fertilidad' funcione.

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
# PARTE 3: FORMULARIO DE ENTRADA DE DATOS COMPLETO
# ===================================================================
with st.sidebar.form("full_input_form"):
    st.header("Por favor, introduce todos los datos disponibles:")

    # --- Expander para Datos Femeninos Básicos ---
    with st.expander("1. Datos Básicos Femeninos", expanded=True):
        edad = st.number_input("Edad", 18, 55, 30)
        duracion_ciclo = st.number_input("Duración promedio del ciclo (días)", 20, 90, 28)
        imc = st.number_input("Índice de Masa Corporal (IMC)", 15.0, 50.0, 22.5, format="%.2f")
        tiene_sop = (st.radio("¿Diagnóstico de SOP?", ["No", "Sí"]) == "Sí")

    # --- Expander para Factores Uterinos y Anatómicos ---
    with st.expander("2. Factores Uterinos y Anatómicos"):
        # Endometriosis
        tiene_endo = (st.radio("¿Diagnóstico de Endometriosis?", ["No", "Sí"]) == "Sí")
        grado_endometriosis = st.selectbox("Grado de Endometriosis", [0, 1, 2, 3, 4], help="0 si no tiene") if tiene_endo else 0
        
        # Miomatosis (lógica guiada)
        tiene_miomas = (st.radio("¿Diagnóstico de Miomatosis Uterina?", ["No", "Sí"]) == "Sí")
        mioma_submucoso, mioma_submucoso_multiple, mioma_intramural_significativo, mioma_subseroso_grande = False, False, False, False
        if tiene_miomas:
            mioma_submucoso = (st.radio("¿Existen miomas SUBMUCOSOS?", ["No", "Sí"]) == "Sí")
            if mioma_submucoso:
                mioma_submucoso_multiple = (st.radio("¿Son múltiples los miomas submucosos?", ["No", "Sí"]) == "Sí")
            else:
                mioma_intramural_significativo = (st.radio("¿Hay miomas INTRAMURALES ≥ 4cm o que deformen cavidad?", ["No", "Sí"]) == "Sí")
                mioma_subseroso_grande = (st.radio("¿Hay miomas SUBSEROSOS > 6cm?", ["No", "Sí"]) == "Sí")
        
        # Adenomiosis
        tiene_adeno = (st.radio("¿Diagnóstico de Adenomiosis?", ["No", "Sí"]) == "Sí")
        tipo_adenomiosis = st.selectbox("Tipo de Adenomiosis", ["", "focal", "difusa_leve", "difusa_severa"]) if tiene_adeno else ""
        
        # Pólipos
        tiene_polipo = (st.radio("¿Diagnóstico de Pólipos Endometriales?", ["No", "Sí"]) == "Sí")
        tipo_polipo = st.selectbox("Tipo de Pólipo", ["", "pequeno_unico", "moderado_multiple", "grande"]) if tiene_polipo else ""
        
        # HSG
        tiene_hsg = (st.radio("¿Resultado de Histerosalpingografía (HSG)?", ["No", "Sí"]) == "Sí")
        resultado_hsg = st.selectbox("Resultado HSG", ["", "normal", "unilateral", "bilateral", "defecto_uterino"]) if tiene_hsg else ""

    # --- Expander para Perfil Endocrino y Metabólico ---
    with st.expander("3. Perfil Endocrino y Metabólico"):
        amh = st.number_input("Nivel de AMH (ng/mL)", 0.0, 20.0, 2.5, format="%.2f")
        prolactina = st.number_input("Nivel de Prolactina (ng/mL)", 0.0, 200.0, 15.0, format="%.2f")
        tsh = st.number_input("Nivel de TSH (µUI/mL)", 0.0, 10.0, 2.0, format="%.2f")
        tpo_ab_positivo = (st.radio("¿Anticuerpos TPO positivos?", ["No", "Sí"]) == "Sí") if tsh > 2.5 else False
        insulina_ayunas = st.number_input("Insulina en ayunas (μU/mL)", 0.0, 50.0, 8.0, format="%.2f")
        glicemia_ayunas = st.number_input("Glicemia en ayunas (mg/dL)", 50, 200, 90)

    # --- Expander para Factor Masculino ---
    with st.expander("4. Factor Masculino"):
        tiene_esperma = (st.radio("¿La pareja tiene un análisis de espermatograma?", ["No", "Sí"]) == "Sí")
        volumen_seminal, concentracion_esperm, motilidad_progresiva, morfologia_normal, vitalidad_esperm = None, None, None, None, None
        if tiene_esperma:
            volumen_seminal = st.number_input("Volumen (mL)", 0.0, 10.0, 2.5, format="%.2f")
            concentracion_esperm = st.number_input("Concentración (millones/mL)", 0.0, 200.0, 40.0, format="%.2f")
            motilidad_progresiva = st.number_input("Motilidad progresiva (%)", 0, 100, 45)
            morfologia_normal = st.number_input("Morfología normal (%)", 0, 100, 5)
            vitalidad_esperm = st.number_input("Vitalidad (%)", 0, 100, 75)

    # Botón de envío del formulario
    submitted = st.form_submit_button("Generar Informe de Fertilidad Completo")

# ===================================================================
# PARTE 4: LÓGICA Y VISUALIZACIÓN DE RESULTADOS
# ===================================================================
if submitted:
    with st.spinner("Realizando evaluación completa con el motor clínico..."):
        # Creamos la instancia con TODOS los datos del formulario
        evaluacion = EvaluacionFertilidad(
            edad=edad, duracion_ciclo=duracion_ciclo, imc=imc, amh=amh, prolactina=prolactina, tsh=tsh, 
            tpo_ab_positivo=tpo_ab_positivo, insulina_ayunas=insulina_ayunas, glicemia_ayunas=glicemia_ayunas,
            tiene_sop=tiene_sop, grado_endometriosis=grado_endometriosis,
            tiene_miomas=tiene_miomas, mioma_submucoso=mioma_submucoso, mioma_submucoso_multiple=mioma_submucoso_multiple,
            mioma_intramural_significativo=mioma_intramural_significativo, mioma_subseroso_grande=mioma_subseroso_grande,
            tipo_adenomiosis=tipo_adenomiosis, tipo_polipo=tipo_polipo, resultado_hsg=resultado_hsg,
            volumen_seminal=volumen_seminal, concentracion_esperm=concentracion_esperm, motilidad_progresiva=motilidad_progresiva,
            morfologia_normal=morfologia_normal, vitalidad_esperm=vitalidad_esperm
        )
        evaluacion.ejecutar_evaluacion()

    st.header("📋 Tu Informe de Fertilidad Personalizado")
    
    # Columna para el pronóstico principal
    st.subheader("1. Pronóstico de Concepción por Ciclo")
    st.metric(
        label="PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO",
        value=evaluacion.probabilidad_ajustada_final,
        delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%",
        delta_color="off"
    )

    # Columnas para el desglose
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

    # Sección de Recomendaciones
    if evaluacion.recomendaciones_lista:
        st.subheader("3. Plan de Acción y Recomendaciones Sugeridas")
        recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
        for rec in recomendaciones_unicas:
            st.warning(f"💡 {rec}")

else:
    st.info("⬅️ Por favor, completa todos los datos disponibles en la barra lateral y haz clic en 'Generar Informe' para ver tu evaluación completa.")