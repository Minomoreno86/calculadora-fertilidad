# app.py

# Importamos la librería de Streamlit y le damos el alias 'st' (una convención estándar)
import streamlit as st

# Con st.title() creamos el título principal de la página
st.title("Calculadora Profesional de Fertilidad")

# Con st.header() creamos un encabezado de segundo nivel
st.header("Bienvenida a la Herramienta de Evaluación de Pareja")

# Con st.write() podemos escribir texto normal, como si fuera un print()
st.write(
    "Esta aplicación utiliza un modelo de evaluación basado en factores clínicos "
    "para ofrecer un pronóstico de fertilidad personalizado. "
    "Estamos trabajando para añadir todos los campos interactivos."
)

st.success("¡Nuestra primera aplicación web está funcionando!")