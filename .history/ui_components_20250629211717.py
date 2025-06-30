# ui_components.py
import streamlit as st

def ui_perfil_basico():
    """Crea la UI para el Paso 1 y usa st.session_state para guardar los valores."""
    st.markdown("Introduce tus datos básicos. Estos se guardarán automáticamente mientras avanzas.")
    
    # Cada widget ahora tiene un 'key' que lo vincula directamente a st.session_state
    st.number_input("Edad", 18, 55, key="edad")
    st.number_input("Duración promedio del ciclo (días)", 20, 90, key="duracion_ciclo")
    
    st.write("**Cálculo del IMC**")
    peso = st.number_input("Peso (kg)", 30.0, 200.0, 65.0, format="%.1f")
    talla = st.number_input("Talla (m)", 1.0, 2.5, 1.65, format="%.2f")

    if talla > 0:
        imc_calculado = peso / (talla ** 2)
        st.info(f"IMC calculado: {imc_calculado:.2f} kg/m²")
        # Guardamos el resultado del cálculo también en el estado de la sesión
        st.session_state.imc = imc_calculado
    else:
        st.session_state.imc = 0