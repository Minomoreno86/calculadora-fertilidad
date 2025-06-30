# config.py
# Este archivo centraliza la configuración de TODAS las variables que se pueden simular.
# Facilita añadir o modificar variables en el futuro sin tocar la lógica de la UI.

SIMULATABLE_VARIABLES = {
    # === PASO 1: PERFIL BÁSICO ===
    'imc': {
        'label': "IMC",
        'type': 'slider',
        'min': 18.0,
        'max': 40.0,
        'step': 0.1,
        'format': "%.1f kg/m²"
    },
    'duracion_ciclo': {
        'label': "Duración del Ciclo (días)",
        'type': 'slider',
        'min': 21,
        'max': 90,
        'step': 1,
        'format': "%d días"
    },

    # === PASO 2: HISTORIAL CLÍNICO ===
    'tiene_miomas': {
        'label': "Simular Resección de Miomas",
        'type': 'boolean'
    },
    'tiene_polipo': {
        'label': "Simular Resección de Pólipos",
        'type': 'boolean'
    },
    
    # === PASO 3: LABORATORIO ===
    'amh': {
        'label': "Hormona Antimülleriana (AMH)",
        'type': 'slider',
        'min': 0.0,
        'max': 20.0,
        'step': 0.1,
        'format': "%.2f ng/mL"
    },
    'prolactina': {
        'label': "Prolactina (ideal < 25)",
        'type': 'slider',
        'min': 0.0,
        'max': 50.0,
        'step': 0.5,
        'format': "%.1f ng/mL"
    },
    'tsh': {
        'label': "TSH (ideal < 2.5)",
        'type': 'slider',
        'min': 0.5,
        'max': 10.0,
        'step': 0.1,
        'format': "%.2f µUI/mL"
    },
    'insulina_ayunas': {
        'label': "Insulina en Ayunas",
        'type': 'slider',
        'min': 1.0,
        'max': 50.0,
        'step': 0.5,
        'format': "%.1f μU/mL"
    },
    'glicemia_ayunas': {
        'label': "Glicemia en Ayunas",
        'type': 'slider',
        'min': 50.0,
        'max': 200.0,
        'step': 1.0,
        'format': "%.0f mg/dL"
    },

    # === PASO 4: FACTOR MASCULINO ===
    'volumen_seminal': {
        'label': "Volumen Seminal (mL)",
        'type': 'slider',
        'min': 0.0,
        'max': 10.0,
        'step': 0.1,
        'format': "%.1f mL"
    },
    'concentracion_esperm': {
        'label': "Concentración Espermática (M/mL)",
        'type': 'slider',
        'min': 0.0,
        'max': 200.0,
        'step': 1.0,
        'format': "%.1f M/mL"
    },
    'motilidad_progresiva': {
        'label': "Motilidad Progresiva (%)",
        'type': 'slider',
        'min': 0,
        'max': 100,
        'step': 1,
        'format': "%d%%"
    },
    'morfologia_normal': {
        'label': "Morfología Normal (%)",
        'type': 'slider',
        'min': 0,
        'max': 100,
        'step': 1,
        'format': "%d%%"
    },
    'vitalidad_esperm': {
        'label': "Vitalidad Espermática (%)",
        'type': 'slider',
        'min': 0,
        'max': 100,
        'step': 1,
        'format': "%d%%"
    }
}