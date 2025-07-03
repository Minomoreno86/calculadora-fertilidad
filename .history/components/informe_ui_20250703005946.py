import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from recomendaciones_reproduccion import obtener_recomendaciones


def display_main_score(value):
    """Muestra el resultado principal con un marcador y una barra de progreso de color dinámico."""
    st.header("📊 Tu Pronóstico de un Vistazo")
    if value < 5: color, performance_text = "#EF553B", "Bajo"
    elif value < 15: color, performance_text = "#FECB52", "Moderado"
    else: color, performance_text = "#00CC96", "Bueno"
        
    st.markdown(f"""<style>.stProgress > div > div > div > div {{background-color: {color};}}</style>""", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label="Pronóstico por Ciclo", value=f"{value:.1f} %")
    with col2:
        st.progress(value / 25)
        st.write(f"**Evaluación:** Un pronóstico considerado **{performance_text}**.")


def mostrar_informe_completo(evaluacion):
    # --- 1. Marcador Visual Principal ---
    display_main_score(evaluacion.pronostico_numerico)
    st.divider()

    # --- 2. Resumen del Pronóstico ---
    st.header("📋 Análisis Detallado del Informe")
    st.subheader(f"1. {evaluacion.pronostico_emoji} Tu Pronóstico General es: **{evaluacion.pronostico_categoria}**")

    if evaluacion.pronostico_categoria == "BUENO":
        st.success(evaluacion.pronostico_frase)
        st.balloons()

    elif evaluacion.pronostico_categoria == "MODERADO":
        st.warning(evaluacion.pronostico_frase)
    else:
        st.error(evaluacion.pronostico_frase)

    st.metric(label="PROBABILIDAD AJUSTADA DE CONCEPCIÓN POR CICLO", value=evaluacion.probabilidad_ajustada_final, delta=f"Basal por edad: {evaluacion.probabilidad_base_edad_num}%", delta_color="off")

    if evaluacion.benchmark_frase:
        st.info(f"💡 **Contexto Poblacional:** {evaluacion.benchmark_frase}")
    st.divider()

    # --- 3. Desglose Detallado de Factores ---
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

    # --- 4. Recomendaciones y Recursos ---
    if evaluacion.insights_clinicos:
        with st.expander("💎 Perlas de Sabiduría Clínica Personalizadas"):
            for insight in evaluacion.insights_clinicos:
                st.info(f"🧠 {insight}")

    if evaluacion.recomendaciones_lista:
        with st.expander("💡 Ver plan de acción y recomendaciones sugeridas"):
            recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
            for rec in recomendaciones_unicas:
                st.warning(f"• {rec}")

    with st.expander("🔗 Recursos Educativos y Sociedades Científicas"):
        st.markdown("""
        * **[American Society for Reproductive Medicine (ASRM)](https://www.asrm.org/)**
        * **[European Society of Human Reproduction and Embryology (ESHRE)](https://www.eshre.eu/)**
        * **[Red Latinoamericana de Reproducción Asistida (REDLARA)](https://redlara.com/)**
        """)

    st.divider()
    st.subheader("🔬 Recomendación de Técnicas de Reproducción Asistida")

  
    # (código para mostrar el informe que ya tenías)
    st.header("...")
    
    # El diccionario se crea aquí, cuando SÍ existe 'evaluacion'.
    datos_reproduccion = {
        'edad': evaluacion.edad,
        'tiene_otb': evaluacion.tiene_otb,
        'amh': evaluacion.amh,
        'concentracion_esperm': evaluacion.concentracion_esperm,
        'motilidad_progresiva': evaluacion.motilidad_progresiva,
        'resultado_hsg': evaluacion.resultado_hsg,
        'tiene_sop': evaluacion.tiene_sop
    }

    # Llamas a la función de recomendaciones con el diccionario recién creado.
    recomendaciones_repro, tecnica_sugerida = obtener_recomendaciones(datos_reproduccion)
    
    st.subheader("Tratamiento Sugerido")
    st.success(f"**Técnica Recomendada:** {tecnica_sugerida}")
    for rec in recomendaciones_repro:
        st.write(rec)
    # 🔥 --- 5. SECCIÓN PARA COMPARTIR (DEBE ESTAR AQUÍ DENTRO) ---
    st.divider()
    st.subheader("¡Comparte tu resultado!")
    st.write("Descarga esta imagen de resumen para compartirla en tus redes sociales.")

    image_data = create_sharable_image(evaluacion)

    st.download_button(
        label="📥 Descargar Imagen",
        data=image_data,
        file_name="mi_pronostico_fertilidad.png",
        mime="image/png",
        use_container_width=True
    )

    st.markdown("---")
    st.subheader("Compartir en redes sociales")

    mensaje_whatsapp = f"¡Mi pronóstico de fertilidad es {evaluacion.probabilidad_ajustada_final} ({evaluacion.pronostico_categoria})! 🍼 Calculado con FertiliCalc Pro. Haz tu test en: https://tuappfertilidad.com"
    url_whatsapp = f"https://api.whatsapp.com/send?text={urllib.parse.quote(mensaje_whatsapp)}"
    url_facebook = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote('https://tuappfertilidad.com')}"

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <a href="{url_whatsapp}" target="_blank">
                <img src="https://img.icons8.com/color/96/000000/whatsapp--v1.png" style="margin-right:10px;"/>
            </a>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <a href="{url_facebook}" target="_blank">
                <img src="https://img.icons8.com/color/96/000000/facebook-new.png" style="margin-right:10px;"/>
            </a>
        """, unsafe_allow_html=True)

    st.info("💡 ¡Comparte para que más personas conozcan su probabilidad de embarazo!")