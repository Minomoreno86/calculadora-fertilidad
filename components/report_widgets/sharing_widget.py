# Contenido para: components/report_widgets/sharing_widget.py

import streamlit as st
import urllib.parse
from utils import create_sharable_image

def render_sharing_buttons(evaluacion):
    """
    Muestra la sección para descargar la imagen de resumen y los
    botones para compartir en redes sociales.
    """
    st.subheader("🚀 ¡Comparte tu resultado!")
    st.write("Ayuda a que más personas conozcan su pronóstico de fertilidad.")

    # 1. Botón para descargar la imagen de resumen
    image_data = create_sharable_image(evaluacion)
    st.download_button(
        label="📥 Descargar Imagen de Resumen",
        data=image_data,
        file_name="mi_pronostico_fertilidad.png",
        mime="image/png",
        use_container_width=True
    )
    
    # 2. Botones para compartir en redes sociales
    # NOTA: Reemplaza la URL de la app con la tuya cuando la despliegues
    url_app = "https://tu-app-de-fertilidad.streamlit.app/" 
    mensaje_whatsapp = f"¡Mi pronóstico de fertilidad es {evaluacion.probabilidad_ajustada_final} ({evaluacion.pronostico_categoria})! 🍼 Calculado con FertiliCalc Pro. Pruébalo en: {url_app}"
    url_whatsapp = f"https://api.whatsapp.com/send?text={urllib.parse.quote(mensaje_whatsapp)}"
    url_facebook = f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(url_app)}"

    st.write("O comparte directamente en:")
    col1, col2, _ = st.columns([1, 1, 5]) # Columnas para alinear los iconos
    
    with col1:
        st.markdown(f'<a href="{url_whatsapp}" target="_blank"><img src="https://img.icons8.com/color/48/000000/whatsapp--v1.png" alt="WhatsApp"></a>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<a href="{url_facebook}" target="_blank"><img src="https://img.icons8.com/color/48/000000/facebook-new.png" alt="Facebook"></a>', unsafe_allow_html=True)