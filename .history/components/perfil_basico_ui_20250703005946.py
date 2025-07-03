import streamlit as st

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
