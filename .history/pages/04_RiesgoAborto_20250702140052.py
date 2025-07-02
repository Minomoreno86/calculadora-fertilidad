# pages/04_RiesgoAborto.py
import streamlit as st
from datetime import datetime
from calculadora_riesgo_aborto import CalculadoraRiesgoAborto
from db_manager import crear_conexion, insertar_riesgo_aborto

st.set_page_config(page_title="Calculadora de Riesgo de Aborto", page_icon="⚠️", layout="wide")
st.title("⚠️ Calculadora Predictiva de Riesgo de Aborto")

st.markdown("## Completa cuidadosamente cada sección:")

# ==============================
# Sección 1: Factores Maternos
# ==============================
st.header("👩 Factores Maternos")

edad = st.number_input("Edad materna (años)", min_value=18, max_value=55, value=30)
imc = st.number_input("IMC", min_value=15.0, max_value=45.0, value=22.0, step=0.1)
edad_paterna = st.number_input("Edad paterna (años)", min_value=18, max_value=75, value=35)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    tabaquismo = st.toggle("Tabaquismo activo")
    alcohol = st.toggle("Consumo moderado de alcohol")
    drogas = st.toggle("Consumo de drogas ilícitas")
    diabetes = st.toggle("Diabetes Mellitus")
    hipotiroidismo = st.toggle("Hipotiroidismo no tratado")
    trombofilias = st.toggle("Trombofilias (SAF, Leiden, etc.)")
    inmunologicas = st.toggle("Inmunológicas (SAF, lupus)")
    malformaciones = st.toggle("Malformaciones uterinas")
    cirugias_uterinas = st.toggle("Cirugías uterinas previas")
    infertilidad = st.toggle("Historia de infertilidad")
    autoinmunes = st.toggle("Enfermedades autoinmunes")

with col2:
    abortos_previos = st.number_input("Número de abortos previos", min_value=0, max_value=10, value=0)

with col3:
    sangrado = st.toggle("Sangrado transvaginal persistente")
    dolor_pelvico = st.toggle("Dolor pélvico intenso")
    saco_pequeno = st.toggle("Saco gestacional pequeño para edad gestacional")
    latido_fetal = st.toggle("Latido fetal presente", value=True)
    fc_fetal_baja = st.toggle("Frecuencia cardíaca fetal baja (<100 lpm)")
    edad_gestacional = st.number_input("Edad gestacional (semanas)", min_value=4, max_value=20, value=6)

# ==============================
# Sección 2: Factores Genéticos y Infecciosos
# ==============================
st.divider()
st.header("🧬 Factores Genéticos e Infecciosos")

col4, col5 = st.columns(2)

with col4:
    cromosomicas = st.toggle("Alteraciones cromosómicas diagnosticadas")
    translocaciones = st.toggle("Translocaciones balanceadas (padres)")

with col5:
    torch = st.toggle("Infección TORCH aguda")
    listeria_sifilis = st.toggle("Listeria, sífilis u otras infecciones graves")

# ==============================
# Sección 3: Factores Ambientales y Laborales
# ==============================
st.divider()
st.header("🏭 Factores Ambientales y Laborales")

col6, col7 = st.columns(2)

with col6:
    radiacion = st.toggle("Exposición significativa a radiación (>5 rad)")
    toxicos = st.toggle("Exposición a tóxicos (plomo, solventes)")

with col7:
    trabajo_de_pie = st.toggle("Trabajo de pie prolongado (>6 horas por día)")
    turnos_nocturnos = st.toggle("Turnos laborales nocturnos frecuentes")

# ==============================
# Cálculo de Riesgo
# ==============================
st.divider()

if st.button("Calcular Riesgo de Aborto"):
    calculadora = CalculadoraRiesgoAborto(
        edad=edad, imc=imc, edad_paterna=edad_paterna,
        tabaquismo=tabaquismo, alcohol=alcohol, drogas=drogas, diabetes=diabetes, hipotiroidismo=hipotiroidismo,
        trombofilias=trombofilias, inmunologicas=inmunologicas, malformaciones=malformaciones, cirugias_uterinas=cirugias_uterinas,
        abortos_previos=abortos_previos, infertilidad=infertilidad, autoinmunes=autoinmunes,
        sangrado=sangrado, dolor_pelvico=dolor_pelvico, saco_pequeno=saco_pequeno, latido_fetal=latido_fetal,
        fc_fetal_baja=fc_fetal_baja, edad_gestacional=edad_gestacional,
        cromosomicas=cromosomicas, translocaciones=translocaciones,
        torch=torch, listeria_sifilis=listeria_sifilis,
        radiacion=radiacion, toxicos=toxicos, trabajo_de_pie=trabajo_de_pie, turnos_nocturnos=turnos_nocturnos
    )
    resultado = calculadora.calcular_riesgo()

    # Guardamos el resultado en session_state
    st.session_state.riesgo_aborto_resultado = resultado
    st.session_state.riesgo_aborto_datos = {
        "edad": edad,
        "imc": imc,
        "edad_paterna": edad_paterna,
        "tabaquismo": tabaquismo,
        "alcohol": alcohol,
        "drogas": drogas,
        "diabetes": diabetes,
        "hipotiroidismo": hipotiroidismo,
        "trombofilias": trombofilias,
        "inmunologicas": inmunologicas,
        "malformaciones": malformaciones,
        "cirugias_uterinas": cirugias_uterinas,
        "abortos_previos": abortos_previos,
        "infertilidad": infertilidad,
        "autoinmunes": autoinmunes,
        "sangrado": sangrado,
        "dolor_pelvico": dolor_pelvico,
        "saco_pequeno": saco_pequeno,
        "latido_fetal": latido_fetal,
        "fc_fetal_baja": fc_fetal_baja,
        "edad_gestacional": edad_gestacional,
        "cromosomicas": cromosomicas,
        "translocaciones": translocaciones,
        "torch": torch,
        "listeria_sifilis": listeria_sifilis,
        "radiacion": radiacion,
        "toxicos": toxicos,
        "trabajo_de_pie": trabajo_de_pie,
        "turnos_nocturnos": turnos_nocturnos
    }

    # Mostrar resultados
    st.subheader(f"{resultado['color']} {resultado['categoria']}")
    st.metric(label="Riesgo Estimado de Aborto", value=f"{resultado['riesgo_final']} %")
    st.info(resultado['mensaje'])

    st.write("### Factores que más contribuyen a tu riesgo:")
    for factor in resultado['factores_clave']:
        st.warning(f"🔹 {factor}")

    st.divider()

# ==============================
# Guardar Resultado
# ==============================
if st.button("Guardar Evaluación de Riesgo"):
    if 'riesgo_aborto_resultado' in st.session_state:
        resultado = st.session_state.riesgo_aborto_resultado
        datos = st.session_state.riesgo_aborto_datos

        conn = crear_conexion("fertilidad.db")
        if conn is not None:
            try:
                datos_registro = (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datos['edad'], datos['imc'], datos['abortos_previos'], int(datos['tiene_miomas']) if 'tiene_miomas' in datos else 0,
                    int(datos['malformaciones']), int(datos['trombofilias']), int(datos['diabetes']), int(datos['hipotiroidismo']),
                    int(datos['trombofilias']), int(datos['inmunologicas']), int(datos['autoinmunes']),
                    resultado['riesgo_final'], resultado['categoria']
                )
                insertar_riesgo_aborto(conn, datos_registro)
                st.toast('¡Evaluación guardada con éxito!', icon='✅')
                conn.close()
            except Exception as e:
                st.error(f"Error al guardar: {e}")
                conn.close()
    else:
        st.warning("⚠️ Primero debes calcular el riesgo antes de poder guardarlo.")