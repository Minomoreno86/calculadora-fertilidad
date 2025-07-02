import streamlit as st
import plotly.express as px
import pandas as pd
import urllib.parse
from utils import create_sharable_image

# --- Tema Personalizado CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f9f9f9;
        background-image: url('https://images.unsplash.com/photo-1526256262350-7da7584cf5eb');
        background-size: cover;
        background-position: center;
    }
    div.stButton > button:first-child {
        background-color: #00CC96;
        color: white;
        height: 50px;
        width: 100%;
        border-radius: 10px;
        font-size: 18px;
    }
    .stProgress > div > div > div > div {
        border-radius: 10px;
        height: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- VISUALIZACIÓN DEL INFORME ---
def display_main_score(value):
    st.header("📊 Tu Pronóstico de un Vistazo")
    if value < 5:
        color = "#EF553B"
        performance_text = "Bajo"
    elif value < 15:
        color = "#FECB52"
        performance_text = "Moderado"
    else:
        color = "#00CC96"
        performance_text = "Bueno"

    st.markdown(f"""<style>.stProgress > div > div > div > div {{background-color: {color};}}</style>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])

    with col1:
        st.metric(label="Probabilidad", value=f"{value:.1f} %")

    with col2:
        st.progress(value / 25)

    st.markdown(f"### Resultado: {performance_text}")


def mostrar_informe_completo(evaluacion):
    st.header("📋 Tu Informe de Fertilidad Personalizado")
    display_main_score(evaluacion.pronostico_numerico)
    st.markdown("""<hr style='border:2px solid #00CC96; border-radius: 5px;'>""", unsafe_allow_html=True)

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

    st.markdown("""<hr style='border:2px solid #00CC96; border-radius: 5px;'>""", unsafe_allow_html=True)
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

    st.markdown("""<hr style='border:2px solid #00CC96; border-radius: 5px;'>""", unsafe_allow_html=True)
    st.subheader("¡Comparte tu resultado!")
    st.write("Descarga esta imagen de resumen para compartirla en tus redes sociales.")

    image_data = create_sharable_image(evaluacion)

    st.download_button(
        label="📥 Descargar Imagen para Compartir 🖼️",
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

    st.markdown("""<hr style='border:2px solid #00CC96; border-radius: 5px;'>""", unsafe_allow_html=True)
    st.subheader("3. Empodérate con Conocimiento")
    with st.expander("🔗 Recursos Educativos y Sociedades Científicas"):
        st.markdown("""
        La información es poder. Aquí tienes enlaces a las principales organizaciones de medicina reproductiva donde encontrarás guías, artículos y noticias de confianza.
        * **[American Society for Reproductive Medicine (ASRM)](https://www.asrm.org/)**: Principal sociedad en Estados Unidos.
        * **[European Society of Human Reproduction and Embryology (ESHRE)](https://www.eshre.eu/)**: Referente mundial y principal sociedad en Europa.
        * **[Red Latinoamericana de Reproducción Asistida (REDLARA)](https://redlara.com/)**: La red más importante de centros de fertilidad en Latinoamérica.
        """)
