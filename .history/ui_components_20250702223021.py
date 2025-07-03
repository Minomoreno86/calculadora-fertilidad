import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from recomendaciones_reproduccion import obtener_recomendaciones


# --- IMPORTACIÓN CLAVE QUE RESUELVE EL ERROR ---
from utils import create_sharable_image
import urllib.parse
def aplicar_tema_personalizado():
    tema = st.session_state.get('tema', 'light')

    if tema == 'light':
        css = """
        <style>
        .stApp {
            background-color: #f9f9f9;
            color: #000000;
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
        """
    elif tema == 'dark':
        css = """
        <style>
        .stApp {
            background-color: #1E2A47;
            color: #FFFFFF;
        }
        div.stButton > button:first-child {
            background-color: #FECB52;
            color: black;
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
        """
    elif tema == 'blue':
        css = """
        <style>
        .stApp {
            background-color: #E6F0FA;
            color: #003366;
        }
        div.stButton > button:first-child {
            background-color: #007ACC;
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
        """
    elif tema == 'pink':
        css = """
        <style>
        .stApp {
            background-color: #FFE6F0;
            color: #660033;
        }
        div.stButton > button:first-child {
            background-color: #FF66B2;
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
        """
    else:
        css = ""  # Seguridad por defecto si el tema no está definido.

    st.markdown(css, unsafe_allow_html=True)

# --- FUNCIONES DE LA INTERFAZ DE USUARIO (PASOS) ---
def ui_perfil_basico():
    """Dibuja la interfaz para el Perfil Básico con validación y UX mejorada."""
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
        "Duración promedio de tu ciclo menstrual (días)",
        min_value=15, max_value=90, key="duracion_ciclo",
        help="Un ciclo regular y ovulatorio suele durar entre 21 y 35 días."
    )
    if duracion_usuario > 0 and not 21 <= duracion_usuario <= 35:
        st.warning(f"Un ciclo de {duracion_usuario} días se considera irregular y merece estudio.")
    elif 21 <= duracion_usuario <= 35:
        st.success(f"Un ciclo de {duracion_usuario} días está dentro del rango normal. ¡Bien!")

    # --- Cálculo de IMC con feedback instantáneo ---
    st.markdown("**Cálculo Automático de IMC**")
    peso = st.number_input("Peso (kg)", min_value=30.0, format="%.1f", key="peso")
    talla = st.number_input("Talla (m)", min_value=1.0, format="%.2f", key="talla")
    if talla > 0:
        imc_calculado = round(peso / (talla ** 2), 2)
        st.session_state.imc = imc_calculado
        
        if imc_calculado < 18.5:
            st.error(f"**IMC: {imc_calculado:.1f} (Bajo Peso).** Esto puede afectar la ovulación.")
        elif 18.5 <= imc_calculado < 25:
            st.success(f"**IMC: {imc_calculado:.1f} (Peso Normal).** ¡Excelente!")
        else: # IMC >= 25
            st.warning(f"**IMC: {imc_calculado:.1f} (Sobrepeso/Obesidad).** Esto puede afectar la calidad ovocitaria.")


def ui_historial_clinico():
    """
    Dibuja la interfaz de usuario para el Historial Clínico con UX mejorada y opciones completas.
    Incluye selectbox como el resto de los controles para OTB y HSG.
    """
    import streamlit as st

    st.markdown("#### Paso 2 de 4: Historial Clínico y Anatómico")
    st.write("Selecciona solo las condiciones que han sido diagnosticadas por un médico.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        # --- SOP ---
        tiene_sop = st.toggle("Diagnóstico de SOP", key="tiene_sop")
        if tiene_sop:
            st.info("💡 El SOP puede afectar la regularidad de la ovulación.")

        # --- Endometriosis ---
        tiene_endometriosis = st.toggle("Diagnóstico de Endometriosis", key="tiene_endometriosis")
        if tiene_endometriosis:
            st.info("💡 La localización y grado de la endometriosis son importantes.")
            st.selectbox("Grado de Endometriosis (1-4)", [1, 2, 3, 4], key="grado_endometriosis")

        # --- Pólipos ---
        tiene_polipos = st.toggle("Diagnóstico de Pólipos Endometriales", key="tiene_polipos_check")
        if tiene_polipos:
            st.info("💡 Su tamaño y número pueden influir en la implantación.")
            st.selectbox(
                "Describe los pólipos",
                options=["pequeno_unico", "moderado_multiple", "grande"],
                key="tipo_polipo",
                format_func=lambda x: {"pequeno_unico": "Pequeño y único", "moderado_multiple": "Moderado o múltiple", "grande": "Grande (>1.5cm)"}.get(x, x)
            )

    with col2:
        # --- Miomas ---
        tiene_miomas = st.toggle("Diagnóstico de Miomatosis (Fibromas)", key="tiene_miomas")
        if tiene_miomas:
            st.info("💡 La localización y tamaño de los miomas es crucial.")
            st.checkbox("¿Son SUBMUCOSOS (dentro de la cavidad)?", key="mioma_submucoso")
            st.checkbox("¿Son SUBMUCOSOS y MÚLTIPLES?", key="mioma_submucoso_multiple")
            st.checkbox("¿Son INTRAMURALES y deforman cavidad o >4cm?", key="mioma_intramural_significativo")
            st.checkbox("¿Son SUBSEROSOS y miden >6cm?", key="mioma_subseroso_grande")

        # --- Adenomiosis ---
        tiene_adenomiosis = st.toggle("Diagnóstico de Adenomiosis", key="tiene_adenomiosis_check")
        if tiene_adenomiosis:
            st.info("💡 La adenomiosis ocurre cuando el tejido endometrial crece en la pared muscular del útero.")
            st.selectbox("Tipo de Adenomiosis", options=["focal", "difusa"], key="tipo_adenomiosis", format_func=lambda x: x.capitalize())

    st.divider()

    # --- Ligadura de Trompas (OTB) con selectbox ---
    tiene_otb = st.selectbox(
        "¿La paciente tiene OTB (ligadura de trompas)?",
        options=["No", "Sí"],
        key="tiene_otb"
    )

    # --- Resultado de HSG con selectbox ---
    tiene_hsg = st.toggle("¿Tiene resultado de Histerosalpingografía (HSG)?", key="tiene_hsg")
    if tiene_hsg:
        st.info("💡 La HSG evalúa si las trompas de Falopio están abiertas.")
        st.selectbox(
            "Resultado de la HSG",
            options=["normal", "unilateral", "bilateral", "defecto_uterino"],
            key="resultado_hsg",
            format_func=lambda x: {
                "normal": "Normal (Ambas trompas permeables)",
                "unilateral": "Obstrucción Unilateral",
                "bilateral": "Obstrucción Bilateral",
                "defecto_uterino": "Defecto en la cavidad uterina"
            }.get(x, "Selecciona un resultado")
        )

    
def ui_laboratorio():
    """
    Dibuja la interfaz para el Perfil de Laboratorio con UX mejorada y validación inmediata.
    """
    st.markdown("#### Paso 3 de 4: Perfil de Laboratorio (Opcional)")
    st.write("Si tienes resultados de análisis, puedes introducirlos aquí para un pronóstico más preciso.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        # --- Hormona Antimülleriana (AMH) ---
        use_amh = st.toggle("Introducir Nivel de AMH", key="use_amh")
        if use_amh:
            amh_level = st.number_input("Nivel de AMH (ng/mL)", min_value=0.0, max_value=20.0, format="%.2f", key="amh")
            if amh_level < 1.0:
                st.warning("⚠️ AMH baja, sugiere una reserva ovárica disminuida.")
            elif amh_level > 3.0:
                st.info("💡 AMH alta, puede ser sugestivo de SOP.")
            else:
                st.success("✅ Nivel de AMH en un rango adecuado.")

        # --- Prolactina ---
        use_prolactina = st.toggle("Introducir Nivel de Prolactina", key="use_prolactina")
        if use_prolactina:
            prolactina_level = st.number_input("Nivel de Prolactina (ng/mL)", min_value=0.0, max_value=200.0, format="%.1f", key="prolactina")
            if prolactina_level >= 25:
                st.warning("⚠️ Nivel de Prolactina elevado (Hiperprolactinemia).")
            else:
                st.success("✅ Nivel de Prolactina normal.")

    with col2:
        # --- Función Tiroidea (TSH) ---
        use_tsh = st.toggle("Introducir Función Tiroidea (TSH)", key="use_tsh")
        if use_tsh:
            tsh_level = st.number_input("Nivel de TSH (µUI/mL)", min_value=0.0, max_value=10.0, format="%.2f", key="tsh")
            if tsh_level > 2.5:
                st.warning("⚠️ TSH por encima del nivel óptimo para fertilidad (>2.5).")
                # Esta sub-opción solo aparece si es relevante
                st.toggle("¿Anticuerpos TPO positivos?", key="tpo_ab_positivo")
            else:
                st.success("✅ Nivel de TSH óptimo.")

        # --- Resistencia a la Insulina (HOMA) ---
        use_homa = st.toggle("Introducir Índice HOMA (Insulina/Glicemia)", key="use_homa")
        if use_homa:
            insulina = st.number_input("Insulina en ayunas (μU/mL)", min_value=1.0, max_value=50.0, format="%.2f", key="insulina_ayunas")
            glicemia = st.number_input("Glicemia en ayunas (mg/dL)", min_value=50.0, max_value=200.0, format="%.1f", key="glicemia_ayunas")

            # Validamos y calculamos el índice HOMA en tiempo real
            if insulina > 1 and glicemia > 50:
                homa_calculado = (insulina * glicemia) / 405
                if homa_calculado >= 3.5:
                    st.warning(f"**Índice HOMA: {homa_calculado:.2f}**. Sugiere Resistencia a la Insulina.")
                else:
                    st.success(f"**Índice HOMA: {homa_calculado:.2f}**. Normal.")
def ui_factor_masculino():
    """
    Dibuja la interfaz para el Factor Masculino con UX mejorada y validación inmediata.
    """
    st.markdown("#### Paso 4 de 4: Factor Masculino (Opcional)")
    st.write("Si se dispone de un espermatograma, introduce aquí los resultados.")
    st.divider()

    use_esperma = st.toggle("Incluir análisis de espermatograma", key="use_esperma")
    if use_esperma:
        col1, col2 = st.columns(2)
        
        with col1:
            # --- Volumen Seminal ---
            volumen = st.number_input("Volumen (mL)", min_value=0.0, max_value=10.0, format="%.2f", key="volumen_seminal")
            if volumen < 1.4:
                st.warning("⚠️ Volumen por debajo del límite de referencia (>1.4 mL).")
            else:
                st.success("✅ Volumen normal.")

            # --- Concentración Espermática ---
            concentracion = st.number_input("Concentración (millones/mL)", min_value=0.0, max_value=200.0, format="%.1f", key="concentracion_esperm")
            if concentracion < 16:
                st.warning("⚠️ Concentración por debajo del límite de referencia (>16 M/mL).")
            else:
                st.success("✅ Concentración normal.")

            # --- Morfología Normal ---
            morfologia = st.number_input("Morfología normal (%)", min_value=0, max_value=100, key="morfologia_normal")
            if morfologia < 4:
                st.warning("⚠️ Morfología por debajo del límite de referencia (>4%).")
            else:
                st.success("✅ Morfología normal.")

        with col2:
            # --- Motilidad Progresiva ---
            motilidad = st.number_input("Motilidad progresiva (%)", min_value=0, max_value=100, key="motilidad_progresiva")
            if motilidad < 32:
                st.warning("⚠️ Motilidad progresiva por debajo del límite de referencia (>30%).")
            else:
                st.success("✅ Motilidad progresiva normal.")

            # --- Vitalidad Espermática ---
            vitalidad = st.number_input("Vitalidad (%)", min_value=0, max_value=100, key="vitalidad_esperm")
            if vitalidad < 58:
                st.warning("⚠️ Vitalidad por debajo del límite de referencia (>54%).")
            else:
                st.success("✅ Vitalidad normal.")
# --- FUNCIONES DE VISUALIZACIÓN DEL INFORME ---

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

    # Extraemos los datos relevantes desde la evaluación actual
    datos_reproduccion = {
    'edad': evaluacion.edad,
    'tiene_sop': evaluacion.tiene_sop,
    'trompas_permeables': st.session_state.get('trompas_permeables', True),
    'factor_tubario': evaluacion.factor_tubario,
    
    'recanalizacion_trompas': st.session_state.get('recanalizacion_trompas', False),
    'baja_reserva': evaluacion.baja_reserva,
    'fallo_ovario': evaluacion.fallo_ovario,
    'concentracion': evaluacion.concentracion_esperm,
    'motilidad': evaluacion.motilidad_progresiva
}

    recomendaciones_repro, tecnica_sugerida = obtener_recomendaciones(datos_reproduccion)

    for recomendacion in recomendaciones_repro:
        st.success(recomendacion)

    if tecnica_sugerida:
        st.info(f"👉 Técnica prioritaria sugerida: **{tecnica_sugerida}**")

    st.caption("📚 Estas recomendaciones son orientativas y deben ser validadas con consulta médica especializada.")
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