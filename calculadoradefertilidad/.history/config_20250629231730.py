# config.py
# Este archivo centraliza la configuración de las variables que se pueden simular.
# Facilita añadir o modificar variables en el futuro sin tocar la lógica de la UI.

SIMULATABLE_VARIABLES = {
    'imc': {
        'label': "IMC",
        'min': 18.0,
        'max': 40.0,
        'step': 0.1,
        'format': "%.1f"
    },
    'tsh': {
        'label': "TSH (ideal < 2.5)",
        'min': 0.5,
        'max': 10.0,
        'step': 0.1,
        'format': "%.2f"
    },
    'prolactina': {
        'label': "Prolactina (ideal < 25)",
        'min': 0.0,
        'max': 50.0,
        'step': 0.5,
        'format': "%.1f"
    },
    'concentracion_esperm': {
        'label': "Concentración Espermática (M/mL)",
        'min': 0.0,
        'max': 200.0,
        'step': 1.0,
        'format': "%.1f"
    },
    'motilidad_progresiva': {
        'label': "Motilidad Progresiva (%)",
        'min': 0,
        'max': 100,
        'step': 1,
        'format': "%d"
    },
    'morfologia_normal': {
        'label': "Morfología Normal (%)",
        'min': 0,
        'max': 100,
        'step': 1,
        'format': "%d"
    }
    # Podemos añadir más variables aquí en el futuro fácilmente
}