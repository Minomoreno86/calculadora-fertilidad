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
abortos_previos = st.number_input("Número de abortos previos", min_value=0, max_value=10, value=0)

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

# Preguntar si la paciente está embarazada
embarazada = st.selectbox("¿Está actualmente embarazada?", ["No", "Sí"])

if embarazada == "Sí":
    st.divider()
    st.header("🤰 Factores del Embarazo Actual")

    col4, col5 = st.columns(2)

    with col4:
        sangrado = st.toggle("Sangrado transvaginal persistente")
        dolor_pelvico = st.toggle("Dolor pélvico intenso")
        saco_pequeno = st.toggle("Saco gestacional pequeño para edad gestacional")

    with col5:
        latido_fetal = st.toggle("Latido fetal presente", value=True)
        fc_fetal_baja = st.toggle("Frecuencia cardíaca fetal baja (<100 lpm)")
        edad_gestacional = st.number_input("Edad gestacional (semanas)", min_value=4, max_value=20, value=6)
else:
    # Valores por defecto si no está embarazada
    sangrado = False
    dolor_pelvico = False
    saco_pequeno = False
    latido_fetal = True
    fc_fetal_baja = False
    edad_gestacional = 6
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
    st.header("📊 Comparación con Modelos Internacionales")

# Datos aproximados (valores de referencia del benchmark)
riesgo_fertili_calc = resultado['riesgo_final']

# Simulación del riesgo con Datayze (simplificado)
if edad < 35:
    riesgo_datayze = 10
elif 35 <= edad < 40:
    riesgo_datayze = 20
else:
    riesgo_datayze = 35
riesgo_datayze += abortos_previos * 5

# Simulación del riesgo con Tommy’s
if abortos_previos == 0:
    riesgo_tommys = 10
elif abortos_previos == 1:
    riesgo_tommys = 25
elif abortos_previos == 2:
    riesgo_tommys = 35
else:
    riesgo_tommys = 50
riesgo_tommys += 5 if imc >= 30 else 0

# Simulación del riesgo con S-PRESTO
riesgo_spresto = 10
riesgo_spresto += 5 if tabaquismo else 0
riesgo_spresto += 5 if alcohol else 0
riesgo_spresto += 5 if abortos_previos > 0 else 0
riesgo_spresto += 5 if imc >= 30 else 0

# Mostrar la comparación
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("FertiliCalc Pro", f"{riesgo_fertili_calc:.1f} %", "Nuestra calculadora personalizada")

with col2:
    st.metric("Datayze", f"{riesgo_datayze:.1f} %", "Estimación simplificada basada en Datayze")

with col3:
    st.metric("Tommy’s (UK)", f"{riesgo_tommys:.1f} %", "Modelo basado en aborto recurrente")

with col4:
    st.metric("S-PRESTO (Asia)", f"{riesgo_spresto:.1f} %", "Puntaje preconcepcional")

st.info("💡 Este comparador es una referencia educativa y no reemplaza la interpretación clínica personalizada.")

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