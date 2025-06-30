# config.py
# Este archivo centraliza la configuración de TODAS las variables que se pueden simular,
# los datos de benchmark y los insights clínicos.

SIMULATABLE_VARIABLES = {
    # === PASO 1: PERFIL BÁSICO ===
    'imc': {
        'label': "IMC", 'type': 'slider', 'min': 18.0, 'max': 40.0, 'step': 0.1,
        'format_spec': "%.1f", 'unit': ' kg/m²'
    },
    'duracion_ciclo': {
        'label': "Duración del Ciclo (días)", 'type': 'slider', 'min': 21, 'max': 90, 'step': 1,
        'format_spec': "%d", 'unit': ' días'
    },

    # === PASO 2: HISTORIAL CLÍNICO ===
    'tiene_miomas': { 
        'label': "Simular Resección de Miomas", 'type': 'boolean' 
    },
    'tiene_polipo': { 
        'label': "Simular Resección de Pólipos", 'type': 'boolean' 
    },
    
    # === PASO 3: LABORATORIO ===
    'amh': {
        'label': "Hormona Antimülleriana (AMH)", 'type': 'slider', 'min': 0.0, 'max': 20.0, 'step': 0.1,
        'format_spec': "%.2f", 'unit': ' ng/mL'
    },
    'prolactina': {
        'label': "Prolactina (ideal < 25)", 'type': 'slider', 'min': 0.0, 'max': 50.0, 'step': 0.5,
        'format_spec': "%.1f", 'unit': ' ng/mL'
    },
    'tsh': {
        'label': "TSH (ideal < 2.5)", 'type': 'slider', 'min': 0.5, 'max': 10.0, 'step': 0.1,
        'format_spec': "%.2f", 'unit': ' µUI/mL'
    },
    'insulina_ayunas': {
        'label': "Insulina en Ayunas", 'type': 'slider', 'min': 1.0, 'max': 50.0, 'step': 0.5,
        'format_spec': "%.1f", 'unit': ' μU/mL'
    },
    'glicemia_ayunas': {
        'label': "Glicemia en Ayunas", 'type': 'slider', 'min': 50.0, 'max': 200.0, 'step': 1.0,
        'format_spec': "%.0f", 'unit': ' mg/dL'
    },

    # === PASO 4: FACTOR MASCULINO ===
    'volumen_seminal': { 
        'label': "Volumen Seminal (mL)", 'type': 'slider', 'min': 0.0, 'max': 10.0, 'step': 0.1, 
        'format_spec': "%.1f", 'unit': ' mL' 
    },
    'concentracion_esperm': { 
        'label': "Concentración Espermática (M/mL)", 'type': 'slider', 'min': 0.0, 'max': 200.0, 'step': 1.0, 
        'format_spec': "%.1f", 'unit': ' M/mL' 
    },
    'motilidad_progresiva': { 
        'label': "Motilidad Progresiva (%)", 'type': 'slider', 'min': 0, 'max': 100, 'step': 1, 
        'format_spec': "%d", 'unit': '%' 
    },
    'morfologia_normal': { 
        'label': "Morfología Normal (%)", 'type': 'slider', 'min': 0, 'max': 100, 'step': 1, 
        'format_spec': "%d", 'unit': '%' 
    },
    'vitalidad_esperm': { 
        'label': "Vitalidad Espermática (%)", 'type': 'slider', 'min': 0, 'max': 100, 'step': 1, 
        'format_spec': "%d", 'unit': '%' 
    }
}

# --- DATOS DE BENCHMARK ---
BENCHMARK_PRONOSTICO_POR_EDAD = {
    "Menos de 30": {"mensual": 22.5, "anual": 85},
    "30-34": {"mensual": 17.5, "anual": 75},
    "35-37": {"mensual": 12.5, "anual": 66},
    "38-40": {"mensual": 7.5, "anual": 44},
    "Más de 40": {"mensual": 2.5, "anual": 28}
}

# --- PERLAS DE SABIDURÍA CLÍNICA ---
CLINICAL_INSIGHTS = {
    "SOP": "El SOP es una de las causas principales de ovulación irregular. Cerca del 75% de las mujeres con SOP pueden tener dificultades para concebir de forma natural, pero con tratamiento, las tasas de éxito mejoran sustancialmente.",
    "ENDOMETRIOSIS": "La endometriosis puede reducir la probabilidad de embarazo mensual de un ~20% (población general) a un 2-10%. Afecta el entorno pélvico y puede impactar la calidad de los óvulos.",
    "MIOMA_SUBMUCOSO": "Los miomas submucosos (dentro de la cavidad) son los más perjudiciales para la fertilidad, pudiendo reducir la probabilidad de implantación en un 50%. Su resección quirúrgica suele mejorar notablemente el pronóstico.",
    "AMH_BAJA": "Una AMH baja (< 1.0 ng/mL) indica una reserva ovárica disminuida. Puede reducir la ventana de oportunidad y se asocia con una probabilidad de concepción un ~23% menor en comparación con una AMH normal para la misma edad.",
    "FACTOR_MASCULINO": "Las alteraciones en el espermatograma son un factor muy significativo. Parámetros como la concentración, motilidad o morfología por debajo de lo normal impactan directamente la capacidad de fecundar el óvulo."
}