class EvaluacionFertilidad:
    def __init__(self, edad, duracion_ciclo=None, imc=None, amh=None, tiene_sop=False, grado_endometriosis=0):
        """
        Constructor del motor de evaluación.
        # NUEVO: Añadido grado_endometriosis (0 = no, 1-4 = grados).
        """
        # --- Factores de Entrada ---
        self.edad = edad
        self.duracion_ciclo = duracion_ciclo
        self.imc = imc
        self.amh = amh
        self.tiene_sop = tiene_sop
        self.grado_endometriosis = grado_endometriosis

        # --- Atributos de Salida (reseteados) ---
        self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, self.probabilidad_base_edad_num = "", "", 0.0
        self.comentario_imc, self.imc_factor = "", 1.0
        self.severidad_sop, self.comentario_sop, self.sop_factor = "No aplica", "", 1.0
        self.diagnostico_reserva, self.recomendacion_reserva = "Evaluación no realizada.", ""
        # NUEVO: Atributos para Endometriosis
        self.comentario_endometriosis, self.endometriosis_factor = "", 1.0
        
        self.probabilidad_ajustada_final = ""
        self.datos_faltantes = []

    def _evaluar_potencial_por_edad(self):
        # (Sin cambios)
        prob_num = 0.0
        if self.edad < 25: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Alta fertilidad", "25-30%", 27.5
        elif self.edad <= 29: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Fertilidad muy buena", "20-25%", 22.5
        elif self.edad <= 34: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Buena fertilidad", "15-20%", 17.5
        elif self.edad <= 37: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Fecundidad en descenso", "10-15%", 12.5
        elif self.edad <= 40: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Reducción significativa", "5-10%", 7.5
        elif self.edad <= 42: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Baja tasa de embarazo", "1-5%", 3.0
        else: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Muy baja probabilidad", "<1%", 0.5
        self.probabilidad_base_edad_num = prob_num

    def _evaluar_imc(self):
        # (Sin cambios)
        if self.imc is None:
            self.datos_faltantes.append("Índice de Masa Corporal (IMC)")
            return
        if self.imc < 18.5: self.comentario_imc, self.imc_factor = "Bajo peso", 0.6
        elif self.imc <= 24.9: self.comentario_imc, self.imc_factor = "Peso normal", 1.0
        elif self.imc <= 29.9: self.comentario_imc, self.imc_factor = "Sobrepeso", 0.85
        elif self.imc <= 34.9: self.comentario_imc, self.imc_factor = "Obesidad", 0.7
        else: self.comentario_imc, self.imc_factor = "Obesidad severa", 0.5
    
    def _evaluar_sop(self):
        # (Sin cambios)
        if not self.tiene_sop: return
        if self.imc is None or self.duracion_ciclo is None:
            self.severidad_sop, self.comentario_sop, self.sop_factor = "Indeterminada", "Faltan datos de IMC y/o ciclo para clasificar.", 0.6
            return
        if self.imc < 25 and self.duracion_ciclo <= 45: self.severidad_sop, self.comentario_sop, self.sop_factor = "Leve", "Impacto menor en fertilidad espontánea.", 0.85
        elif self.imc <= 30 and self.duracion_ciclo > 45: self.severidad_sop, self.comentario_sop, self.sop_factor = "Moderado", "Fertilidad espontánea significativamente reducida.", 0.6
        else: self.severidad_sop, self.comentario_sop, self.sop_factor = "Severo", "Se recomienda tratamiento especializado como primera línea.", 0.4
            
    def _evaluar_amh(self):
        # (Sin cambios)
        if self.amh is None:
            self.datos_faltantes.append("Hormona Antimülleriana (AMH)")
            self.diagnostico_reserva = "Dato no proporcionado."
            return
        if self.amh > 3.5: self.diagnostico_reserva = "Alta Reserva Ovárica"
        elif self.amh >= 1.5: self.diagnostico_reserva = "Reserva Ovárica Adecuada"
        elif self.amh >= 1.0: self.diagnostico_reserva = "Reserva Ovárica Normal-Baja"
        elif self.amh >= 0.5: self.diagnostico_reserva = "Reserva Ovárica Disminuida"
        else: self.diagnostico_reserva = "Muy Baja Reserva Ovárica"

    def _evaluar_endometriosis(self):
        """
        # NUEVO: Evalúa el grado de endometriosis y determina el factor de ajuste.
        """
        if self.grado_endometriosis == 0:
            return # No hay endometriosis, el factor es 1.0
        
        if self.grado_endometriosis == 1:
            self.comentario_endometriosis = "Grado I (mínima): Puede generar inflamación subclínica que afecte la fertilidad."
            self.endometriosis_factor = 0.9
        elif self.grado_endometriosis == 2:
            self.comentario_endometriosis = "Grado II (leve): Ligera afectación anatómica y adhesiones mínimas."
            self.endometriosis_factor = 0.75
        elif self.grado_endometriosis == 3:
            self.comentario_endometriosis = "Grado III (moderada): Alteración anatómica y/o inflamación significativa. FIV suele ser recomendado."
            self.endometriosis_factor = 0.5
        elif self.grado_endometriosis == 4:
            self.comentario_endometriosis = "Grado IV (severa): Distorsión anatómica severa. La concepción espontánea es muy improbable."
            self.endometriosis_factor = 0.3

    def ejecutar_evaluacion(self):
        """Orquesta todas las evaluaciones y el cálculo final."""
        self._evaluar_potencial_por_edad()
        self._evaluar_imc()
        self._evaluar_sop()
        self._evaluar_amh()
        self._evaluar_endometriosis() # NUEVO paso en la secuencia
        
        # Cálculo final con el nuevo factor de endometriosis
        prob_ajustada = self.probabilidad_base_edad_num * self.imc_factor * self.sop_factor * self.endometriosis_factor
        self.probabilidad_ajustada_final = f"{prob_ajustada:.1f}%"

# --- FASE DE INTERACCIÓN ---

print("--- Módulo de Evaluación de Fertilidad v6 (con Endometriosis) ---")
edad_str = input("Introduce la edad de la paciente: ")
sop_str = input("¿Tiene diagnóstico de SOP? (si/no): ")
ciclo_str = input("Introduce la duración promedio de su ciclo en días (ej: 30): ")
endo_str = input("¿Tiene diagnóstico de endometriosis? (si/no): ")
grado_endo = 0
if endo_str.lower() == 'si':
    grado_str = input("¿Qué grado de endometriosis (1, 2, 3 o 4)?: ")
    grado_endo = int(grado_str) if grado_str in ['1','2','3','4'] else 0

imc_str = input("Introduce el IMC (kg/m²) (deja en blanco si no lo tienes): ")
amh_str = input("Introduce el nivel de AMH (ng/mL) (deja en blanco si no lo tienes): ")

try:
    evaluacion = EvaluacionFertilidad(
        edad=int(edad_str),
        duracion_ciclo=int(ciclo_str) if ciclo_str else None,
        imc=float(imc_str) if imc_str else None,
        amh=float(amh_str) if amh_str else None,
        tiene_sop=(sop_str.lower() == 'si'),
        grado_endometriosis=grado_endo
    )
    evaluacion.ejecutar_evaluacion()
    
    print("\n" + "="*15 + " INFORME DE FERTILIDAD " + "="*15)
    print("\n--- 1. Pronóstico de Concepción por Ciclo ---")
    print(f"Probabilidad basal (por edad): {evaluacion.probabilidad_base_edad_num}%")
    print(f"  x Factor IMC: {evaluacion.imc_factor}")
    if evaluacion.tiene_sop: print(f"  x Factor SOP ({evaluacion.severidad_sop}): {evaluacion.sop_factor}")
    if evaluacion.grado_endometriosis > 0: print(f"  x Factor Endometriosis (Grado {evaluacion.grado_endometriosis}): {evaluacion.endometriosis_factor}")
    print("-" * 52)
    print(f"PRONÓSTICO AJUSTADO DE EMBARAZO PARA ESTE CICLO: {evaluacion.probabilidad_ajustada_final}")
    print("-" * 52)
    
    print("\n--- 2. Análisis Detallado de Factores ---")
    print(f"- Edad ({evaluacion.edad} años): {evaluacion.diagnostico_potencial_edad}")
    if evaluacion.grado_endometriosis > 0: print(f"- Endometriosis (Grado {evaluacion.grado_endometriosis}): {evaluacion.comentario_endometriosis}")
    if evaluacion.tiene_sop: print(f"- SOP ({evaluacion.severidad_sop}): {evaluacion.comentario_sop}")
    if evaluacion.imc: print(f"- IMC ({evaluacion.imc} kg/m²): {evaluacion.comentario_imc}")
    print(f"- Reserva Ovárica (AMH): {evaluacion.diagnostico_reserva}")
    
    if evaluacion.datos_faltantes:
        print("\n" + "-"*40)
        print("Para una evaluación más precisa, se recomienda proporcionar:")
        for dato in evaluacion.datos_faltantes: print(f"- {dato}")
    print("\n" + "="*52)

except ValueError:
    print("\nError: La edad, ciclo, grado e IMC deben ser números válidos.")