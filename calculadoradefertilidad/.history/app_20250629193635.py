# app.py

import streamlit as st
# Es buena práctica poner las importaciones de librerías externas primero
import plotly.express as px
# Luego las importaciones de nuestros propios módulos
from calculadora_fertilidad import EvaluacionFertilidad
from ui_components import mostrar_formulario_completo, mostrar_informe_completo

# --- Configuración y Título ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("Calculadora Profesional de Fertilidad 👶")
st.write("Herramienta de evaluación multifactorial para el pronóstico de fertilidad de pareja.")

# --- Renderizar el Formulario y Recolectar Todos los Datos ---
user_inputs = mostrar_formulario_completo()

# --- Lógica Principal: Calcular y Mostrar el Informe ---

# CORRECCIÓN DEL BUG:
# 1. Sacamos el estado del botón del diccionario a una variable propia.
submit_button_pressed = user_inputs.pop('submit_button')

# 2. Ahora, el diccionario 'user_inputs' está limpio y solo contiene datos clínicos.
#    El bloque `if` ahora usa nuestra nueva variable.
if submit_button_pressed:
    try:
        with st.spinner("Realizando evaluación completa con el motor clínico..."):
            
            # 3. Ahora podemos pasar el diccionario limpio (**user_inputs) a la clase sin peligro.
            evaluacion = EvaluacionFertilidad(**user_inputs)
            
            evaluacion.ejecutar_evaluacion()

        mostrar_informe_completo(evaluacion)
    
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado al generar el informe: {e}")
        st.error("Por favor, verifique que todos los campos numéricos han sido introducidos correctamente.")
else:
    st.info("⬅️ Por favor, completa tu perfil en la barra lateral y presiona 'Generar Informe' para ver tu evaluación.")