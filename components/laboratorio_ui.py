   
import streamlit as st
   
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