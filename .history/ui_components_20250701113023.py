# ui_components.py
import streamlit as st
import plotly.express as px
import pandas as pd  # <-- LA IMPORTACIÓN QUE FALTABA

def ui_perfil_basico():
    """Dibuja la interfaz de usuario para el Paso 1: Perfil Básico con validación y feedback mejorado."""
    st.markdown("#### Paso 1 de 4: Perfil Básico")

    # --- Edad con validación ---
    edad_usuario = st.number_input("Edad", min_value=18, max_value=55, key="edad", help="La edad es el factor más determinante.")
    if edad_usuario > 45:
        st.warning("⚠️ A partir de los 45 años, la probabilidad de concepción natural es muy baja.")

    # --- Duración del ciclo con validación ---
    duracion_usuario = st.number_input("Duración promedio del ciclo (días)", min_value=15, max_value=90, key="duracion_ciclo", help="Un ciclo regular dura entre 21 y 35 días.")
    if duracion_usuario < 21 or duracion_usuario > 35:
        st.warning("⚠️ Un ciclo fuera del rango normal (21-35 días) puede indicar irregularidades que deben ser evaluadas.")

    # --- Cálculo y feedback persuasivo del IMC ---
    st.write("**Cálculo Automático de IMC**")
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=65.0, format="%.1f")
    talla = st.number_input("Talla (m)", min_value=1.0, max_value=2.5, value=1.65, format="%.2f")

    if talla > 0:
        imc_calculado = peso / (talla ** 2)
        st.session_state.imc = imc_calculado

        # Lógica de feedback con colores y mensajes claros
        if imc_calculado < 18.5:
            st.error(f"**IMC: {imc_calculado:.1f} (Bajo Peso).** Esto puede afectar negativamente la fertilidad.")
        elif 18.5 <= imc_calculado < 25:
            st.success(f"**IMC: {imc_calculado:.1f} (Peso Normal).** ¡Excelente!")
        elif 25 <= imc_calculado < 30:
            st.warning(f"**IMC: {imc_calculado:.1f} (Sobrepeso).** Considera hablar con un profesional sobre un peso saludable.")
        else: # IMC >= 30
            st.error(f"**IMC: {imc_calculado:.1f} (Obesidad).** Esto impacta significativamente en la fertilidad y requiere atención.")
    else:
        st.session_state.imc = 0.0

    st.divider()

def ui_historial_clinico():
    """Dibuja la interfaz de usuario para el Paso 2: Historial Clínico."""
    st.markdown("#### Paso 2 de 4: Historial Clínico")
    st.radio("¿Diagnóstico de SOP?", ["No", "Sí"], key="sop_radio")
    
    st.radio("¿Diagnóstico de Endometriosis?", ["No", "Sí"], key="endo_radio")
    if st.session_state.get("endo_radio") == 'Sí':
        st.selectbox("Grado de Endometriosis", [1, 2, 3, 4], key="grado_endometriosis")
        
    st.radio("¿Diagnóstico de Miomatosis?", ["No", "Sí"], key="miomas_radio")
    if st.session_state.get("miomas_radio") == 'Sí':
        st.radio("¿Miomas SUBMUCOSOS?", ["No", "Sí"], key="mioma_submucoso_radio")
        if st.session_state.get("mioma_submucoso_radio") == 'Sí':
            st.radio("¿Son múltiples?", ["No", "Sí"], key="mioma_submucoso_multiple_radio")
        else:
            st.radio("¿Miomas INTRAMURALES ≥ 4cm o que deformen cavidad?", ["No", "Sí"], key="mioma_intramural_radio")
            st.radio("¿Miomas SUBSEROSOS > 6cm?", ["No", "Sí"], key="mioma_subseroso_radio")
            
    st.radio("¿Diagnóstico de Adenomiosis?", ["No", "Sí"], key="adeno_radio")
    if st.session_state.get("adeno_radio") == 'Sí':
        st.selectbox("Tipo de Adenomiosis", ["focal", "difusa_leve", "difusa_severa"], key="tipo_adenomiosis")
        
    st.radio("¿Diagnóstico de Pólipos?", ["No", "Sí"], key="polipo_radio")
    if st.session_state.get("polipo_radio") == 'Sí':
        st.selectbox("Tipo de Pólipo", ["pequeno_unico", "moderado_multiple", "grande"], key="tipo_polipo")
        
    st.radio("¿Resultado de HSG disponible?", ["No", "Sí"], key="hsg_radio")
    if st.session_state.get("hsg_radio") == 'Sí':
        st.selectbox("Resultado HSG", ["normal", "unilateral", "bilateral", "defecto_uterino"], key="resultado_hsg")
    st.divider()

def ui_laboratorio():
    """Dibuja la interfaz de usuario para el Paso 3: Laboratorio."""
    st.markdown("#### Paso 3 de 4: Perfil de Laboratorio")
    with st.expander("Expandir para introducir Perfil Endocrino y Metabólico"):
        st.checkbox("Incluir Nivel de AMH", key="use_amh", value=st.session_state.get("use_amh", False))
        st.number_input("Nivel de AMH (ng/mL)", min_value=0.0, max_value=20.0, format="%.2f", key="amh", disabled=not st.session_state.get("use_amh"))
        st.divider()
        
        st.checkbox("Incluir Nivel de Prolactina", key="use_prolactina", value=st.session_state.get("use_prolactina", False))
        st.number_input("Nivel de Prolactina (ng/mL)", min_value=0.0, max_value=200.0, format="%.2f", key="prolactina", disabled=not st.session_state.get("use_prolactina"))
        st.divider()
        
        st.checkbox("Incluir Función Tiroidea (TSH)", key="use_tsh", value=st.session_state.get("use_tsh", False))
        st.number_input("Nivel de TSH (µUI/mL)", min_value=0.0, max_value=10.0, format="%.2f", key="tsh", disabled=not st.session_state.get("use_tsh"))
        if st.session_state.get("use_tsh") and st.session_state.get("tsh", 0) > 2.5:
            st.radio("¿Anticuerpos TPO positivos?", ["No", "Sí"], key="tpo_radio", help="Este campo solo es relevante si TSH > 2.5")
        st.divider()
        
        st.checkbox("Incluir Índice HOMA (Resistencia a Insulina)", key="use_homa", value=st.session_state.get("use_homa", False))
        st.number_input("Insulina en ayunas (μU/mL)", min_value=1.0, max_value=50.0, format="%.2f", key="insulina_ayunas", disabled=not st.session_state.get("use_homa"))
        st.number_input("Glicemia en ayunas (mg/dL)", min_value=50.0, max_value=200.0, format="%.1f", key="glicemia_ayunas", disabled=not st.session_state.get("use_homa"))
    st.divider()

def ui_factor_masculino():
    """Dibuja la interfaz de usuario para el Paso 4: Factor Masculino."""
    st.markdown("#### Paso 4 de 4: Factor Masculino")
    st.checkbox("Incluir análisis de espermatograma", key="use_esperma", value=st.session_state.get("use_esperma", False))
    with st.expander("Expandir para introducir Detalle del Espermatograma"):
        is_disabled = not st.session_state.get("use_esperma")
        st.number_input("Volumen (mL)", min_value=0.0, max_value=10.0, format="%.2f", key="volumen_seminal", disabled=is_disabled)
        st.number_input("Concentración (millones/mL)", min_value=0.0, max_value=200.0, format="%.2f", key="concentracion_esperm", disabled=is_disabled)
        st.number_input("Motilidad progresiva (%)", min_value=0, max_value=100, key="motilidad_progresiva", disabled=is_disabled)
        st.number_input("Morfología normal (%)", min_value=0, max_value=100, key="morfologia_normal", disabled=is_disabled)
        st.number_input("Vitalidad (%)", min_value=0, max_value=100, key="vitalidad_esperm", disabled=is_disabled)
    st.divider()

def mostrar_informe_completo(evaluacion):
    """Dibuja el informe completo y dinámico en la página."""
    st.header("📋 Tu Informe de Fertilidad Personalizado")
    st.subheader(f"1. {evaluacion.pronostico_emoji} Tu Pronóstico General es: **{evaluacion.pronostico_categoria}**")
    
    if evaluacion.pronostico_categoria == "BUENO":
        st.success(evaluacion.pronostico_frase)
    elif evaluacion.pronostico_categoria == "MODERADO":
        st.warning(evaluacion.pronostico_frase)
    else:
        st.error(evaluacion.pronostico_frase)

    st.metric(label="PROBABILIDAD AJUSTADA DE CONCEPCIÓN POR CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")
    
    if evaluacion.benchmark_frase:
        st.info(f"💡 **Contexto Poblacional:** {evaluacion.benchmark_frase}")
        
    st.divider()
    
    st.subheader("2. Análisis Detallado y Recomendaciones")
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
            if evaluacion.homa_calculado is not None:
                st.write(f"* **Resistencia a Insulina (HOMA {evaluacion.homa_calculado:.2f}):** {evaluacion.comentario_homa}")
            else:
                st.write("* **Resistencia a Insulina (HOMA):** Datos no proporcionados")
        with col3:
            st.info("Factor Masculino")
            st.write(f"* **Espermatograma:** {evaluacion.diagnostico_masculino_detallado or 'No reportado'}")

    if evaluacion.insights_clinicos:
        st.subheader("💎 Perlas de Sabiduría Clínica Personalizadas")
        st.write("Basado en los datos que proporcionaste, aquí tienes información clave extraída de la evidencia científica:")
        for insight in evaluacion.insights_clinicos:
            st.info(f"🧠 {insight}")

    if evaluacion.recomendaciones_lista:
        with st.expander("💡 Ver plan de acción y recomendaciones sugeridas"):
            recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
            for rec in recomendaciones_unicas:
                st.warning(f"• {rec}")

    with st.expander("📊 Ver comparativa visual del pronóstico"):
        prob_basal = evaluacion.probabilidad_base_edad_num
        try:
            prob_final = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
            df_probs = pd.DataFrame({
                'Tipo de Pronóstico': ['Probabilidad Basal (solo por edad)', 'Pronóstico Ajustado (todos los factores)'],
                'Probabilidad (%)': [prob_basal, prob_final]
            })
            fig = px.bar(df_probs, x='Tipo de Pronóstico', y='Probabilidad (%)', text_auto='.1f', title="Comparativa de Probabilidad de Concepción por Ciclo", color='Tipo de Pronóstico', color_discrete_map={'Probabilidad Basal (solo por edad)': 'royalblue', 'Pronóstico Ajustado (todos los factores)': 'lightcoral'})
            fig.update_layout(yaxis_title="Probabilidad de Embarazo (%)", xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        except (ValueError, TypeError):
            st.error("No se pudo generar el gráfico debido a un resultado de pronóstico no numérico.")

    st.divider()
    st.subheader("3. Empodérate con Conocimiento")
    with st.expander("🔗 Recursos Educativos y Sociedades Científicas"):
        st.markdown("""
        La información es poder. Aquí tienes enlaces a las principales organizaciones de medicina reproductiva donde encontrarás guías, artículos y noticias de confianza.
        * **[American Society for Reproductive Medicine (ASRM)](https://www.asrm.org/)**: Principal sociedad en Estados Unidos.
        * **[European Society of Human Reproduction and Embryology (ESHRE)](https://www.eshre.eu/)**: Referente mundial y principal sociedad en Europa.
        * **[Red Latinoamericana de Reproducción Asistida (REDLARA)](https://redlara.com/)**: La red más importante de centros de fertilidad en Latinoamérica.
        """)