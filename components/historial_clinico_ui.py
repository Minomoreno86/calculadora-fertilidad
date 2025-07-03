
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
     # --- Ligadura de Trompas (OTB) con selectbox ---
    tiene_otb = st.toggle("¿La paciente tiene OTB (ligadura de trompas)?", key="tiene_otb")


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