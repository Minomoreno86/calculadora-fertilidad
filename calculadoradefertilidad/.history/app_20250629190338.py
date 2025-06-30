# app.py (Versión 6 - Profesional y Completa)

import streamlit as st
import plotly.express as px
from calculadora_fertilidad import EvaluacionFertilidad

# MEJORA 4: Optimizar el set_page_config
st.set_page_config(
    page_title="Calculadora de Fertilidad Pro",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:soporte@tuappfertilidad.com',
        'Report a bug': "mailto:bug@tuappfertilidad.com",
        'About': "# Calculadora de Fertilidad Profesional.\n¡Una app creada con conocimiento experto y la última tecnología!"
    }
)

# --- Título y Descripción ---
st.title("Calculadora Profesional de Fertilidad 👶")
st.write("Herramienta de evaluación multifactorial para el pronóstico de fertilidad de pareja, basada en guías clínicas y conocimiento experto.")

# ===================================================================
# PARTE 3: BARRA LATERAL INTERACTIVA
# ===================================================================
st.sidebar.header("Datos de la Pareja")

# --- Controles Principales ---
st.sidebar.subheader("1. Perfil Básico y Diagnósticos")
edad = st.sidebar.number_input("Edad", 18, 55, 30)
duracion_ciclo = st.sidebar.number_input("Duración promedio del ciclo (días)", 20, 90, 28)
imc = st.sidebar.number_input("Índice de Masa Corporal (IMC)", 15.0, 50.0, 22.5, format="%.2f")
tiene_sop = (st.sidebar.radio("¿Diagnóstico de SOP?", ["No", "Sí"], key="sop") == "Sí")

# --- Secciones Detalladas ---
with st.sidebar.expander("Expandir para Factores Anatómicos"):
    tiene_endo = (st.radio("¿Diagnóstico de Endometriosis?", ["No", "Sí"], key="endo") == "Sí")
    grado_endometriosis = st.selectbox("Grado de Endometriosis", [1, 2, 3, 4], key="endo_grade") if tiene_endo else 0
    
    st.write("---")
    tiene_miomas = (st.radio("¿Diagnóstico de Miomatosis Uterina?", ["No", "Sí"], key="miomas") == "Sí")
    if tiene_miomas:
        mioma_submucoso = (st.radio("¿Miomas SUBMUCOSOS?", ["No", "Sí"], key="subm") == "Sí")
        if mioma_submucoso:
            mioma_submucoso_multiple = (st.radio("¿Son múltiples?", ["No", "Sí"], key="subm_mult") == "Sí")
            mioma_intramural_significativo, mioma_subseroso_grande = False, False
        else:
            mioma_intramural_significativo = (st.radio("¿Miomas INTRAMURALES ≥ 4cm o que deformen cavidad?", ["No", "Sí"], key="intra") == "Sí")
            mioma_subseroso_grande = (st.radio("¿Miomas SUBSEROSOS > 6cm?", ["No", "Sí"], key="subs") == "Sí")
            mioma_submucoso_multiple = False
    else:
        mioma_submucoso, mioma_submucoso_multiple, mioma_intramural_significativo, mioma_subseroso_grande = False, False, False, False

    st.write("---")
    tiene_adeno = (st.radio("¿Diagnóstico de Adenomiosis?", ["No", "Sí"], key="adeno") == "Sí")
    tipo_adenomiosis = st.selectbox("Tipo de Adenomiosis", ["focal", "difusa_leve", "difusa_severa"], key="adeno_type") if tiene_adeno else ""

    st.write("---")
    tiene_polipo = (st.radio("¿Diagnóstico de Pólipos?", ["No", "Sí"], key="polipo") == "Sí")
    tipo_polipo = st.selectbox("Tipo de Pólipo", ["pequeno_unico", "moderado_multiple", "grande"], key="polipo_type") if tiene_polipo else ""

    st.write("---")
    tiene_hsg = (st.radio("¿Resultado de HSG?", ["No", "Sí"], key="hsg") == "Sí")
    resultado_hsg = st.selectbox("Resultado HSG", ["normal", "unilateral", "bilateral", "defecto_uterino"], key="hsg_type") if tiene_hsg else ""

with st.sidebar.expander("Expandir para Perfil Endocrino-Metabólico"):
    amh = st.number_input("Nivel de AMH (ng/mL)", 0.0, 20.0, 2.5, format="%.2f")
    prolactina = st.number_input("Nivel de Prolactina (ng/mL)", 0.0, 200.0, 15.0, format="%.2f")
    tsh = st.number_input("Nivel de TSH (µUI/mL)", 0.0, 10.0, 2.0, format="%.2f")
    tpo_ab_positivo = (st.radio("¿Anticuerpos TPO positivos?", ["No", "Sí"], key="tpo") == "Sí") if tsh > 2.5 else False
    st.write("---")
    st.write("**Cálculo del Índice HOMA**")
    insulina_ayunas = st.number_input("Insulina en ayunas (μU/mL)", 1.0, 50.0, 8.0, format="%.2f", key="insulina")
    glicemia_ayunas = st.number_input("Glicemia en ayunas (mg/dL)", 50, 200, 90, key="glicemia")
    
    # MEJORA 1: Calcular y mostrar HOMA en tiempo real
    homa_calculado_realtime = (insulina_ayunas * glicemia_ayunas) / 405
    st.sidebar.info(f"Índice HOMA calculado: {homa_calculado_realtime:.2f}")

with st.sidebar.expander("Expandir para Factor Masculino"):
    tiene_esperma = (st.radio("¿Análisis de espermatograma disponible?", ["No", "Sí"], key="esperma") == "Sí")
    if tiene_esperma:
        volumen_seminal = st.number_input("Volumen (mL)", 0.0, 10.0, 2.5, format="%.2f")
        concentracion_esperm = st.number_input("Concentración (millones/mL)", 0.0, 200.0, 40.0, format="%.2f")
        motilidad_progresiva = st.number_input("Motilidad progresiva (%)", 0, 100, 45)
        morfologia_normal = st.number_input("Morfología normal (%)", 0, 100, 5)
        vitalidad_esperm = st.number_input("Vitalidad (%)", 0, 100, 75)
    else:
        volumen_seminal, concentracion_esperm, motilidad_progresiva, morfologia_normal, vitalidad_esperm = None, None, None, None, None


# MEJORA 2: Validación de campos críticos
campos_validados = True
if tiene_esperma and (concentracion_esperm == 0.0): # Azoospermia es un caso especial, no necesita otros valores.
    pass
elif tiene_esperma and (volumen_seminal is None or concentracion_esperm is None or motilidad_progresiva is None or morfologia_normal is None or vitalidad_esperm is None):
    st.sidebar.warning("Por favor, complete todos los campos del espermatograma.")
    campos_validados = False

st.sidebar.write("---")
submit_button = st.sidebar.button("Generar Informe de Fertilidad Completo", disabled=not campos_validados)

# ===================================================================
# PARTE 4: LÓGICA Y VISUALIZACIÓN DE RESULTADOS
# ===================================================================
if submit_button:
    # MEJORA 5: Manejo de errores más robusto
    try:
        with st.spinner("Realizando evaluación completa con el motor clínico..."):
            miomas_dict = {'tiene_miomas': tiene_miomas, 'mioma_submucoso': mioma_submucoso, 'mioma_submucoso_multiple': mioma_submucoso_multiple,'mioma_intramural_significativo': mioma_intramural_significativo, 'mioma_subseroso_grande': mioma_subseroso_grande}
            adenomiosis_dict = {'tipo_adenomiosis': tipo_adenomiosis}
            polipo_dict = {'tipo_polipo': tipo_polipo}
            hsg_dict = {'resultado_hsg': resultado_hsg}
            
            evaluacion = EvaluacionFertilidad(
                edad=edad, duracion_ciclo=duracion_ciclo, imc=imc, amh=amh, prolactina=prolactina, tsh=tsh, 
                tpo_ab_positivo=tpo_ab_positivo, insulina_ayunas=insulina_ayunas, glicemia_ayunas=glicemia_ayunas,
                tiene_sop=tiene_sop, grado_endometriosis=grado_endometriosis,
                volumen_seminal=volumen_seminal, concentracion_esperm=concentracion_esperm, motilidad_progresiva=motilidad_progresiva,
                morfologia_normal=morfologia_normal, vitalidad_esperm=vitalidad_esperm,
                **miomas_dict, **adenomiosis_dict, **polipo_dict, **hsg_dict
            )
            evaluacion.ejecutar_evaluacion()

        # MEJORA 3: Resumen de datos ingresados
        with st.expander("Verificar Resumen de Datos Ingresados"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Edad:** {edad}")
                st.write(f"**IMC:** {imc}")
                st.write(f"**SOP:** {'Sí' if tiene_sop else 'No'}")
                st.write(f"**Endometriosis:** Grado {grado_endometriosis if tiene_endo else 'No reportada'}")
            with col2:
                st.write(f"**AMH:** {amh if amh is not None else 'No reportado'}")
                st.write(f"**TSH:** {tsh if tsh is not None else 'No reportado'}")
                st.write(f"**Factor Masculino:** {'Sí' if tiene_esperma else 'No'}")

        st.header("📋 Tu Informe de Fertilidad Personalizado")
        st.subheader("1. Pronóstico de Concepción por Ciclo")
        st.metric(label="PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")

        st.subheader("2. Análisis Detallado de Factores")
        # ... (código del informe detallado)
        
        st.subheader("3. Plan de Acción y Recomendaciones")
        if evaluacion.recomendaciones_lista:
            recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
            for rec in recomendaciones_unicas:
                st.warning(f"💡 {rec}")
        else:
            st.success("Basado en los datos proporcionados, no se identificaron factores de riesgo que requieran una recomendación específica. ¡Excelente pronóstico!")

        # MEJORA 6: Visualización gráfica opcional
        st.subheader("4. Comparativa Visual del Pronóstico")
        prob_basal = evaluacion.probabilidad_base_edad_num
        prob_final = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
        
        df_probs = {'Tipo de Pronóstico': ['Probabilidad Basal (solo por edad)', 'Pronóstico Ajustado (todos los factores)'], 'Probabilidad (%)': [prob_basal, prob_final]}
        fig = px.bar(df_probs, x='Tipo de Pronóstico', y='Probabilidad (%)', text_auto='.1f', title="Comparativa de Probabilidad de Concepción por Ciclo", color='Tipo de Pronóstico', color_discrete_map={'Probabilidad Basal (solo por edad)': 'royalblue', 'Pronóstico Ajustado (todos los factores)': 'lightcoral'})
        fig.update_layout(yaxis_title="Probabilidad de Embarazo (%)", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Ha ocurrido un error al generar el informe: {e}")
        st.error("Por favor, verifique que todos los campos numéricos han sido introducidos correctamente.")

else:
    st.info("⬅️ Por favor, completa tu perfil en la barra lateral y presiona 'Generar Informe' para ver tu evaluación.")