# calculadora_riesgo_aborto.py
import numpy as np

class CalculadoraRiesgoAborto:
    def __init__(self, **datos):
        # Factores Maternos
        self.edad = datos.get('edad', 30)
        self.imc = datos.get('imc', 22.0)
        self.tabaquismo = datos.get('tabaquismo', False)
        self.alcohol = datos.get('alcohol', False)
        self.drogas = datos.get('drogas', False)
        self.diabetes = datos.get('diabetes', False)
        self.hipotiroidismo = datos.get('hipotiroidismo', False)
        self.trombofilias = datos.get('trombofilias', False)
        self.inmunologicas = datos.get('inmunologicas', False)
        self.malformaciones = datos.get('malformaciones', False)
        self.cirugias_uterinas = datos.get('cirugias_uterinas', False)
        self.abortos_previos = datos.get('abortos_previos', 0)
        self.infertilidad = datos.get('infertilidad', False)
        self.autoinmunes = datos.get('autoinmunes', False)

        # Factores del Embarazo Actual
        self.sangrado = datos.get('sangrado', False)
        self.dolor_pelvico = datos.get('dolor_pelvico', False)
        self.saco_pequeno = datos.get('saco_pequeno', False)
        self.latido_fetal = datos.get('latido_fetal', True)
        self.fc_fetal_baja = datos.get('fc_fetal_baja', False)
        self.edad_gestacional = datos.get('edad_gestacional', 6)

        # Factores Paternos
        self.edad_paterna = datos.get('edad_paterna', 35)

        # Factores Genéticos
        self.cromosomicas = datos.get('cromosomicas', False)
        self.translocaciones = datos.get('translocaciones', False)

        # Infecciones
        self.torch = datos.get('torch', False)
        self.listeria_sifilis = datos.get('listeria_sifilis', False)

        # Factores Ambientales y Laborales
        self.radiacion = datos.get('radiacion', False)
        self.toxicos = datos.get('toxicos', False)
        self.trabajo_de_pie = datos.get('trabajo_de_pie', False)
        self.turnos_nocturnos = datos.get('turnos_nocturnos', False)

        # Control de factores de riesgo
        self.factores_de_riesgo = []

    def calcular_riesgo(self):
        riesgo = 5  # Riesgo basal en la población general

        # --- Alta Influencia ---
        if self.edad >= 35:
            riesgo += 10
            self.factores_de_riesgo.append("Edad materna avanzada")
        if self.abortos_previos == 1:
            riesgo += 10
            self.factores_de_riesgo.append("1 aborto previo")
        elif self.abortos_previos == 2:
            riesgo += 20
            self.factores_de_riesgo.append("2 abortos previos")
        elif self.abortos_previos >= 3:
            riesgo += 40
            self.factores_de_riesgo.append("Abortos recurrentes (≥3)")

        if self.trombofilias:
            riesgo += 15
            self.factores_de_riesgo.append("Trombofilias diagnosticadas (SAF, Leiden)")
        if self.malformaciones:
            riesgo += 15
            self.factores_de_riesgo.append("Malformaciones uterinas")
        if self.diabetes:
            riesgo += 10
            self.factores_de_riesgo.append("Diabetes no controlada")
        if self.sangrado:
            riesgo += 10
            self.factores_de_riesgo.append("Sangrado persistente")
        if not self.latido_fetal:
            riesgo += 20
            self.factores_de_riesgo.append("Latido fetal ausente")
        if self.fc_fetal_baja:
            riesgo += 10
            self.factores_de_riesgo.append("Frecuencia cardíaca fetal baja (<100 lpm)")

        # --- Influencia Moderada ---
        if self.tabaquismo:
            riesgo += 5
            self.factores_de_riesgo.append("Tabaquismo activo")
        if self.hipotiroidismo:
            riesgo += 5
            self.factores_de_riesgo.append("Hipotiroidismo no tratado")
        if self.imc < 18.5 or self.imc >= 30:
            riesgo += 5
            self.factores_de_riesgo.append("IMC extremo (bajo peso u obesidad)")
        if self.edad_paterna >= 40:
            riesgo += 3
            self.factores_de_riesgo.append("Edad paterna avanzada (>40 años)")
        if self.autoinmunes:
            riesgo += 5
            self.factores_de_riesgo.append("Enfermedades autoinmunes")

        # --- Baja Influencia ---
        if self.alcohol:
            riesgo += 2
            self.factores_de_riesgo.append("Consumo moderado de alcohol")
        if self.drogas:
            riesgo += 5
            self.factores_de_riesgo.append("Consumo de drogas ilícitas")
        if self.inmunologicas:
            riesgo += 5
            self.factores_de_riesgo.append("Inmunológicas (SAF, lupus)")
        if self.infertilidad:
            riesgo += 3
            self.factores_de_riesgo.append("Historia de infertilidad")
        if self.cirugias_uterinas:
            riesgo += 3
            self.factores_de_riesgo.append("Cirugías uterinas previas")
        if self.dolor_pelvico:
            riesgo += 5
            self.factores_de_riesgo.append("Dolor pélvico intenso")
        if self.saco_pequeno:
            riesgo += 5
            self.factores_de_riesgo.append("Saco gestacional pequeño para la edad gestacional")
        if self.edad_gestacional < 6:
            riesgo += 3
            self.factores_de_riesgo.append("Edad gestacional <6 semanas")
        if self.cromosomicas:
            riesgo += 10
            self.factores_de_riesgo.append("Alteraciones cromosómicas")
        if self.translocaciones:
            riesgo += 5
            self.factores_de_riesgo.append("Translocaciones balanceadas")
        if self.torch:
            riesgo += 5
            self.factores_de_riesgo.append("Infección TORCH aguda")
        if self.listeria_sifilis:
            riesgo += 5
            self.factores_de_riesgo.append("Infecciones graves (Listeria, Sífilis)")
        if self.radiacion:
            riesgo += 5
            self.factores_de_riesgo.append("Exposición a radiación alta")
        if self.toxicos:
            riesgo += 3
            self.factores_de_riesgo.append("Exposición a tóxicos (plomo, solventes)")
        if self.trabajo_de_pie:
            riesgo += 3
            self.factores_de_riesgo.append("Trabajo de pie prolongado (>6h/día)")
        if self.turnos_nocturnos:
            riesgo += 2
            self.factores_de_riesgo.append("Turnos nocturnos frecuentes")

        # Limitar riesgo máximo
        riesgo_final = min(riesgo, 85)

        if riesgo_final < 15:
            categoria = "Riesgo Bajo"
            color = "🟢"
            mensaje = "Tu riesgo de aborto es bajo. Se recomienda control prenatal habitual."
        elif riesgo_final < 30:
            categoria = "Riesgo Moderado"
            color = "🟡"
            mensaje = "Tu riesgo de aborto es moderado. Se recomienda seguimiento especializado."
        else:
            categoria = "Riesgo Alto"
            color = "🔴"
            mensaje = "Tu riesgo de aborto es alto. Es prioritaria la evaluación por un especialista."

        return {
            "riesgo_final": riesgo_final,
            "categoria": categoria,
            "color": color,
            "mensaje": mensaje,
            "factores_clave": self.factores_de_riesgo
        }
