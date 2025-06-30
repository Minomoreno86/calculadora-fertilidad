# app.py (Versión 2 - Interactiva y Completa)

# ===================================================================
# PARTE 1: IMPORTACIONES Y CONFIGURACIÓN INICIAL
# ===================================================================
import streamlit as st

# Importamos nuestro "cerebro" y nuestros "textos"
# Asegúrate de que los archivos 'calculadora_fertilidad.py' y 'textos_clinicos.py'
# están en la misma carpeta que este archivo 'app.py'.
from calculadora_fertilidad import EvaluacionFertilidad
from textos_clinicos import RECOMENDACIONES

# --- Configuración de la Página Web ---
# Esto debe ser lo primero que Streamlit ejecuta
st.set_page_config(
    page_title="Calculadora de Fertilidad Pro",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===================================================================
# PARTE 2: TÍTULO Y DESCRIPCIÓN DE LA APLICACIÓN
# ===================================================================

st.title("Calculadora Profesional de Fertilidad 👶")
st.write(
    "Esta herramienta utiliza un modelo de evaluación basado en factores clínicos "
    "para ofrecer un pronóstico de fertilidad personalizado. Fue desarrollada con el conocimiento experto de un especialista en ginecología y fertilidad."
)


# ===================================================================
# PARTE 3: FORMULARIO DE ENTRADA DE DATOS EN LA BARRA LATERAL
# ===================================================================

# Usamos st.sidebar para que todos los controles aparezcan en la barra lateral
st.sidebar.header("Por favor, introduce tus datos:")

# Usamos un formulario (st.form) para agrupar todas las entradas. 
# Esto nos permite tener un solo botón de envío y evita que la app se recargue con cada cambio.
with st.sidebar.form("input_form"):
    
    st.subheader("Datos Femeninos Básicos")
    
    # Widget para la Edad: un campo numérico.
    edad = st.number_input(
        label="Edad de la paciente", 
        min_value=18, 
        max_value=55, 
        value=30, # Valor por defecto que aparece al cargar la página
        help="Introduce tu edad actual en años."
    )

    # Widget para el SOP: un menú desplegable (selectbox).
    # Streamlit devuelve el valor de la opción seleccionada ('No' o 'Sí')
    sop_opcion = st.selectbox(
        label="¿Tienes diagnóstico de SOP?",
        options=["No", "Sí"],
        index=0, # Por defecto, la opción 'No' (índice 0) está seleccionada
        help="Síndrome de Ovario Poliquístico."
    )
    # Convertimos la opción de texto a un valor booleano (True/False) que nuestra clase entiende
    tiene_sop = True if sop_opcion == "Sí" else False

    # Widget para la Duración del Ciclo
    duracion_ciclo = st.number_input(
        label="Duración promedio de tu ciclo (días)",
        min_value=20,
        max_value=90,
        value=28,
        help="Número de días desde el primer día de una regla hasta el día antes de la siguiente."
    )

    # El botón que enviará todos los datos del formulario a la vez.
    # La variable 'submitted' será True solo cuando se haga clic en el botón.
    submitted = st.form_submit_button("Calcular Pronóstico")


# ===================================================================
# PARTE 4: LÓGICA Y VISUALIZACIÓN DE RESULTADOS
# ===================================================================

# Este bloque de código solo se ejecutará si el botón del formulario ha sido presionado.
if submitted:
    # Mostramos un mensaje de espera mientras se realizan los cálculos.
    with st.spinner("Analizando todos los factores..."):
        
        # Creamos la instancia de nuestro motor lógico.
        # Por ahora, solo pasamos los 3 datos que hemos recolectado en la interfaz.
        # Nuestra clase está preparada para manejar los demás como 'None' o valores por defecto.
        evaluacion = EvaluacionFertilidad(
            edad=edad,
            tiene_sop=tiene_sop,
            duracion_ciclo=duracion_ciclo
        )
        
        # Le damos la orden de ejecutar todos los cálculos internos.
        evaluacion.ejecutar_evaluacion()

    # Una vez terminan los cálculos, mostramos el informe en la página principal.
    st.header("📋 Tu Informe de Fertilidad Personalizado")

    # Usamos st.metric para mostrar el resultado principal de forma destacada.
    st.metric(
        label="Pronóstico Ajustado de Embarazo para este Ciclo",
        value=evaluacion.probabilidad_ajustada_final,
        help="Este es un pronóstico estadístico basado en los datos proporcionados y no garantiza un resultado."
    )
    
    # Creamos dos columnas para organizar mejor la información del informe.
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Análisis de Factores")
        st.info(f"**Potencial por Edad:** {evaluacion.diagnostico_potencial_edad}")
        if tiene_sop:
            st.info(f"**SOP:** {evaluacion.severidad_sop}")
        # A medida que añadamos más inputs, llenaremos esta sección con más análisis.

    with col2:
        st.subheader("Plan de Acción Sugerido")
        # Mostramos las recomendaciones si la lista no está vacía
        if evaluacion.recomendaciones_lista:
            # Usamos set() para eliminar recomendaciones duplicadas si las hubiera
            recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
            for rec in recomendaciones_unicas:
                st.warning(f"💡 {rec}")
        else:
            st.success("Basado en los datos proporcionados, no hay recomendaciones específicas de acción. ¡Buen pronóstico!")

else:
    # Este es el mensaje que se muestra en la página principal antes de que el usuario envíe el formulario.
    st.info("⬅️ Por favor, completa tus datos en la barra lateral y haz clic en 'Calcular Pronóstico' para generar tu informe.")