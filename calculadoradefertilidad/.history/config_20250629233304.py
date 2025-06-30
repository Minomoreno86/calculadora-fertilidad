# config.py
SIMULATABLE_VARIABLES = {
    'imc': {
        'label': "IMC", 'type': 'slider', 'min': 18.0, 'max': 40.0, 'step': 0.1,
        'format_spec': "%.1f", 'unit': ' kg/m²'
    },
    'duracion_ciclo': {
        'label': "Duración del Ciclo (días)", 'type': 'slider', 'min': 21, 'max': 90, 'step': 1,
        'format_spec': "%d", 'unit': ' días'
    },
    'tiene_miomas': {'label': "Simular Resección de Miomas", 'type': 'boolean'},
    'tiene_polipo': {'label': "Simular Resección de Pólipos", 'type': 'boolean'},
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