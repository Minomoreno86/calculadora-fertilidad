
import streamlit as st

def recopilar_datos_desde_ui():
    """
    Lee el st.session_state de la interfaz de usuario, lo traduce a un formato
    limpio y devuelve un diccionario listo para la clase EvaluacionFertilidad.
    Este es el "traductor" oficial entre el Frontend y el Backend.
    """
    datos = {}

    # --- Perfil Básico ---
    datos['edad'] = st.session_state.get('edad', 30)
    datos['duracion_ciclo'] = st.session_state.get('duracion_ciclo', 28)
    datos['imc'] = st.session_state.get('imc', 22.0)

    # --- Historial Clínico ---
    datos['tiene_sop'] = st.session_state.get('tiene_sop', False)

    if st.session_state.get('tiene_endometriosis', False):
        datos['grado_endometriosis'] = st.session_state.get('grado_endometriosis', 1)
    else:
        # Si el toggle está apagado, nos aseguramos de que el valor sea 0.
        datos['grado_endometriosis'] = 0

    if st.session_state.get('tiene_polipos_check', False):
        datos['tipo_polipo'] = st.session_state.get('tipo_polipo', 'pequeno_unico')
    else:
        datos['tipo_polipo'] = "" # Un string vacío si no hay pólipos

    datos['tiene_miomas'] = st.session_state.get('tiene_miomas', False)
    # Solo añadimos los detalles si el toggle principal está activo
    if datos['tiene_miomas']:
        datos['mioma_submucoso'] = st.session_state.get('mioma_submucoso', False)
        datos['mioma_submucoso_multiple'] = st.session_state.get('mioma_submucoso_multiple', False)
        datos['mioma_intramural_significativo'] = st.session_state.get('mioma_intramural_significativo', False)
        datos['mioma_subseroso_grande'] = st.session_state.get('mioma_subseroso_grande', False)

    if st.session_state.get('tiene_adenomiosis_check', False):
        datos['tipo_adenomiosis'] = st.session_state.get('tipo_adenomiosis', 'focal')
    else:
        datos['tipo_adenomiosis'] = ""

    if st.session_state.get('tiene_hsg', False):
        datos['resultado_hsg'] = st.session_state.get('resultado_hsg', 'normal')
    else:
        datos['resultado_hsg'] = None # None si no hay datos

    # --- Laboratorio ---
    datos['amh'] = st.session_state.get('amh') if st.session_state.get('use_amh') else None
    datos['prolactina'] = st.session_state.get('prolactina') if st.session_state.get('use_prolactina') else None
    datos['tsh'] = st.session_state.get('tsh') if st.session_state.get('use_tsh') else None
    datos['tpo_ab_positivo'] = st.session_state.get('tpo_ab_positivo', False) if st.session_state.get('use_tsh') else False
    datos['insulina_ayunas'] = st.session_state.get('insulina_ayunas') if st.session_state.get('use_homa') else None
    datos['glicemia_ayunas'] = st.session_state.get('glicemia_ayunas') if st.session_state.get('use_homa') else None

    # --- Factor Masculino ---
    if st.session_state.get('use_esperma', False):
        datos['volumen_seminal'] = st.session_state.get('volumen_seminal')
        datos['concentracion_esperm'] = st.session_state.get('concentracion_esperm')
        datos['motilidad_progresiva'] = st.session_state.get('motilidad_progresiva', 32)
        datos['morfologia_normal'] = st.session_state.get('morfologia_normal')
        datos['vitalidad_esperm'] = st.session_state.get('vitalidad_esperm', 58)

    return datos