import streamlit as st

def render_main_score(evaluacion):
    st.header("📊 Tu Pronóstico de un Vistazo")
    value = evaluacion.pronostico_numerico
    if value < 5: color, performance_text = "#EF553B", "Bajo"
    elif value < 15: color, performance_text = "#FECB52", "Moderado"
    else: color, performance_text = "#00CC96", "Bueno"
    st.markdown(f"<style>.stProgress > div > div > div > div {{background-color: {color};}}</style>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label="Pronóstico por Ciclo", value=f"{value:.1f} %")
    with col2:
        st.progress(value / 25)
        st.write(f"**Evaluación:** Un pronóstico considerado **{performance_text}**.")