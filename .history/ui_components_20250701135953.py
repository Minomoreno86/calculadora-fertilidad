# ui_components.py
import streamlit as st
import plotly.express as px
import pandas as pd  # <-- LA IMPORTACIÓN QUE FALTABA

def ui_perfil_basico():
    """Dibuja la interfaz de usuario para el Perfil Básico con validación y UX mejorada."""
    st.markdown("#### Paso 1 de 4: Perfil Básico")

    # --- Edad con validación inmediata y contextual ---
    edad_usuario = st.number_input(
        "Tu edad",
        min_value=18, max_value=55, key="edad",
        help="La edad es el factor más determinante en la fertilidad."
    )
    if 35 <= edad_usuario <= 37:
        st.info("💡 A partir de los 35, se recomienda no demorar la consulta si no se logra el embarazo en 6 meses.")
    elif edad_usuario > 37:
        st.warning("⚠️ Por encima de 37 años, el potencial reproductivo disminuye de forma acelerada.")

    # --- Duración del ciclo con feedback instantáneo ---
    duracion_usuario = st.number_input(
        "Duración promedio de tu ciclo menstrual",
        min_value=15, max_value=90, key="duracion_ciclo",
        help="Un ciclo regular y ovulatorio suele durar entre 21 y 35 días."
    )
    if not 21 <= duracion_usuario <= 35:
        st.warning(f"Un ciclo de {duracion_usuario} días se considera irregular y merece estudio.")
    else:
        st.success(f"Un ciclo de {duracion_usuario} días se considera dentro del rango normal. ¡Bien!")

    # --- Cálculo de IMC ---
    st.markdown("**Cálculo Automático de IMC**")
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=65.0, format="%.1f")
    talla = st.number_input("Talla (m)", min_value=1.0, max_value=2.5, value=1.65, format="%.2f")

    if talla > 0:
        imc_calculado = peso / (talla ** 2)
        st.session_state.imc = imc_calculado
        if imc_calculado < 18.5:
            st.error(f"**IMC: {imc_calculado:.1f} (Bajo Peso).** Esto puede afectar la ovulación.")
        elif 18.5 <= imc_calculado < 25:
            st.success(f"**IMC: {imc_calculado:.1f} (Peso Normal).** ¡Excelente!")
        else: # IMC >= 25
            st.warning(f"**IMC: {imc_calculado:.1f} (Sobrepeso/Obesidad).** Esto puede afectar la calidad ovocitaria y la respuesta a tratamientos.")
    else:
        st.session_state.imc = 0.0

def ui_historial_clinico():
    """
    Dibuja la interfaz de usuario para el Historial Clínico con UX mejorada.
    """
    st.markdown("#### Paso 2 de 4: Historial Clínico y Anatómico")
    st.write("Selecciona solo las condiciones que han sido diagnosticadas por un médico.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        # --- SOP (Síndrome de Ovario Poliquístico) ---
        tiene_sop = st.toggle("Diagnóstico de SOP", key="tiene_sop")
        if tiene_sop:
            st.info("💡 El SOP puede afectar la regularidad de la ovulación.")

        # --- Endometriosis ---
        tiene_endometriosis = st.toggle("Diagnóstico de Endometriosis", key="tiene_endometriosis")
        if tiene_endometriosis:
            st.info("💡 La localización y grado de la endometriosis son importantes.")
            st.selectbox("Grado de Endometriosis (1-4)", [1, 2, 3, 4], key="grado_endometriosis")

        # --- Pólipos ---
        # La key debe coincidir con el parámetro esperado por la clase: 'tipo_polipo'
        tiene_polipos = st.toggle("Diagnóstico de Pólipos Endometriales", key="tipo_polipo")
        if tiene_polipos:
            st.info("💡 Su resección suele mejorar el pronóstico de implantación.")

    with col2:
        # --- Miomatosis Uterina ---
        tiene_miomas = st.toggle("Diagnóstico de Miomatosis (Fibromas)", key="tiene_miomas")
        if tiene_miomas:
            st.info("💡 No todos los miomas afectan la fertilidad. Su localización es clave.")
            # La clase espera 'mioma_submucoso', etc.
            st.checkbox("¿Son SUBMUCOSOS (dentro de la cavidad)?", key="mioma_submucoso")
            st.checkbox("¿Son INTRAMURALES y deforman cavidad o >4cm?", key="mioma_intramural_significativo")

        # --- Factor Tubárico (HSG) ---
        tiene_hsg = st.toggle("Tienes resultado de Histerosalpingografía (HSG)", key="tiene_hsg")
        if tiene_hsg:
            st.info("💡 La HSG evalúa si las trompas de Falopio están abiertas.")
            # La clase espera 'resultado_hsg'
            st.selectbox(
                "Resultado de la HSG",
                options=["normal", "unilateral", "bilateral", "defecto_uterino"],
                key="resultado_hsg",
                    format_func=lambda x: {
                    "normal": "Normal (Ambas trompas permeables)",
                    "unilateral": "Obstrucción Unilateral",
                    "bilateral": "Obstrucción Bilateral",
                    "defecto_uterino": "Defecto en la cavidad uterina"
                }.get(x) if x else "Selecciona un resultado" # <--- ESTA ES LA LÍNEA CORREGIDA
                # --- FIN DE LA CORRECCIÓN ---
            )
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