# calculadora_riesgo_aborto.py
import numpy as np

class CalculadoraRiesgoAborto:
    def __init__(self, **datos):
        self.edad = datos.get('edad', 30)
        self.imc = datos.get('imc', 22.0)
        self.abortos_previos = datos.get('abortos_previos', 0)
        self.tiene_miomas = datos.get('tiene_miomas', False)
        self.tiene_adenomiosis = datos.get('tiene_adenomiosis', False)
        self.tiene_sop = datos.get('tiene_sop', False)
        self.tiene_diabetes = datos.get('tiene_diabetes', False)
        self.tiene_tiroides = datos.get('tiene_tiroides', False)
        self.prolactina_alta = datos.get('prolactina_alta', False)
        self.infecciones_previas = datos.get('infecciones_previas', False)
        self.calidad_semen_alterada = datos.get('calidad_semen_alterada', False)

    def calcular_riesgo(self):
        # Riesgo base poblacional
        riesgo_base = 10  # % riesgo poblacional general

        # Modificadores de riesgo
        if self.edad >= 35: riesgo_base += 5
        if self.edad >= 40: riesgo_base += 10

        if self.imc < 18.5 or self.imc >= 30: riesgo_base += 5

        if self.abortos_previos == 1: riesgo_base += 10
        if self.abortos_previos >= 2: riesgo_base += 20

        if self.tiene_miomas: riesgo_base += 5
        if self.tiene_adenomiosis: riesgo_base += 5
        if self.tiene_sop: riesgo_base += 3
        if self.tiene_diabetes: riesgo_base += 5
        if self.tiene_tiroides: riesgo_base += 5
        if self.prolactina_alta: riesgo_base += 2
        if self.infecciones_previas: riesgo_base += 3
        if self.calidad_semen_alterada: riesgo_base += 2

        # Limitar riesgo máximo a 80%
        riesgo_final = min(riesgo_base, 80)

        if riesgo_final < 15:
            categoria = "Riesgo Bajo"
            color = "🟢"
            mensaje = "Tu riesgo de aborto es bajo, sigue con tus controles habituales."
        elif riesgo_final < 30:
            categoria = "Riesgo Moderado"
            color = "🟡"
            mensaje = "Tu riesgo de aborto es moderado, se recomienda control más estrecho."
        else:
            categoria = "Riesgo Alto"
            color = "🔴"
            mensaje = "Tu riesgo de aborto es alto, es prioritaria una consulta especializada."

        return {
            "riesgo_final": riesgo_final,
            "categoria": categoria,
            "color": color,
            "mensaje": mensaje
        }
