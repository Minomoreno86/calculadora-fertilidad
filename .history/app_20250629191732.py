# app.py

import streamlit as st
from calculadora_fertilidad import EvaluacionFertilidad
# NUEVO: Importamos las funciones de la interfaz de usuario
from ui_components import mostrar_formulario_completo, mostrar_informe_completo

# --- Configuración y Título ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("Calculadora Profesional de Fertilidad 👶")
st.write("Herramienta de evaluación multifactorial para el pronóstico de fertilidad de pareja.")

# --- Renderizar el Formulario y Recolectar Todos los Datos ---
# Llamamos a una única función que se encarga de toda la complejidad de la UI
user_inputs = mostrar_formulario_completo()

# --- Lógica Principal: Calcular y Mostrar el Informe ---
if user_inputs['submit_button']:
    try:
        # El spinner se muestra mientras se ejecutan los cálculos
        with st.spinner("Realizando evaluación completa con el motor clínico..."):
            
            # Creamos la instancia de nuestro "cerebro" pasando todos los datos
            # recolectados por el formulario. El operador ** desempaqueta el diccionario.
            evaluacion = EvaluacionFertilidad(**user_inputs)
            
            # Ejecutamos todos los cálculos
            evaluacion.ejecutar_evaluacion()

        # Llamamos a la función que se encarga de dibujar todo el informe
        mostrar_informe_completo(evaluacion)
    
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado al generar el informe: {e}")
        st.error("Por favor, verifique que todos los campos numéricos han sido introducidos correctamente.")
else:
    # Mensaje inicial antes de que el usuario haga clic en el botón
    st.info("⬅️ Por favor, completa tu perfil en la barra lateral y presiona 'Generar Informe' para ver tu evaluación.")