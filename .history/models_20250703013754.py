# Contenido para: models.py

import numpy as np
# Este archivo no debe importar nada de 'logic'

class EvaluacionFertilidad:
    """Define la estructura de datos para una evaluación de fertilidad."""
    def __init__(self, **datos):
        self._asignar_datos_entrada(datos)
        self._reset_output_attributes()

    def _asignar_datos_entrada(self, datos):
        # ... (el método completo, sin cambios)
        
    def _reset_output_attributes(self):
        """Resetea los atributos de salida de la evaluación de fertilidad."""
        pass

    @property
    def probabilidad_ajustada_final(self):
        return f"{self.pronostico_numerico:.1f}%"