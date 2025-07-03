import streamlit as st

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