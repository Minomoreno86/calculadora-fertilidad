# app.py
import streamlit as st
from calculadora_fertilidad import EvaluacionFertilidad
from ui_components import mostrar_formulario_completo, mostrar_informe_completo, inicializar_session_state

# --- Configuración y Título ---
st.set_page_config(page_title="Calculadora de Fertilidad Pro", page_icon="👶", layout="wide")
st.title("Calculadora Profesional de Fertilidad 👶")

# Inicializa la memoria de la sesión con valores por defecto
inicializar_session_state()

# Dibuja el formulario y nos dice si el botón fue presionado
submit_button = mostrar_formulario_completo()

# --- Lógica Principal ---
if submit_button:
    try:
        with st.spinner("Realizando evaluación completa con el motor clínico..."):
            # Construimos el diccionario de argumentos para miomas desde el session_state
            miomas_args = {
                'tiene_miomas': st.session_state.tiene_miomas == "Sí",
                'mioma_submucoso': st.session_state.mioma_submucoso == "Sí",
                'mioma_submucoso_multiple': st.session_state.mioma_submucoso_multiple == "Sí",
                'mioma_intramural_significativo': st.session_state.mioma_intramural_significativo == "Sí",
                'mioma_subseroso_grande': st.session_state.mioma_subseroso_grande == "Sí"
            }

            # Creamos la instancia de nuestro "cerebro" leyendo los datos desde la memoria de la sesión
            evaluacion = EvaluacionFertilidad(
                edad=st.session_state.edad,
                duracion_ciclo=st.session_state.duracion_ciclo,
                imc=st.session_state.imc_peso / (st.session_state.imc_talla ** 2),
                amh=st.session_state.amh,
                prolactina=st.session_state.prolactina,
                tsh=st.session_state.tsh,
                tpo_ab_positivo=(st.session_state.tpo_ab_positivo == "Sí"),
                insulina_ayunas=st.session_state.insulina_ayunas,
                glicemia_ayunas=st.session_state.glicemia_ayunas,
                tiene_sop=(st.session_state.tiene_sop == "Sí"),
                grado_endometriosis=st.session_state.grado_endometriosis if st.session_state.tiene_endo == "Sí" else 0,
                tipo_adenomiosis=st.session_state.tipo_adenomiosis if st.session_state.tiene_adeno == "Sí" else "",
                tipo_polipo=st.session_state.tipo_polipo if st.session_state.tiene_polipo == "Sí" else "",
                resultado_hsg=st.session_state.resultado_hsg if st.session_state.tiene_hsg == "Sí" else "",
                volumen_seminal=st.session_state.volumen_seminal if st.session_state.tiene_esperma == "Sí" else None,
                concentracion_esperm=st.session_state.concentracion_esperm if st.session_state.tiene_esperma == "Sí" else None,
                motilidad_progresiva=st.session_state.motilidad_progresiva if st.session_state.tiene_esperma == "Sí" else None,
                morfologia_normal=st.session_state.morfologia_normal if st.session_state.tiene_esperma == "Sí" else None,
                vitalidad_esperm=st.session_state.vitalidad_esperm if st.session_state.tiene_esperma == "Sí" else None,
                **miomas_args
            )
            
            evaluacion.ejecutar_evaluacion()

        # Llamamos a la función que se encarga de dibujar todo el informe
        mostrar_informe_completo(evaluacion)
    
    except Exception as e:
        st.error(f"Ha ocurrido un error inesperado al generar el informe: {e}")
        st.error("Por favor, verifique que todos los campos numéricos han sido introducidos correctamente.")
else:
    st.info("⬅️ Por favor, completa tu perfil en la barra lateral. Cuando termines, presiona 'Generar Informe' para ver tu evaluación.")