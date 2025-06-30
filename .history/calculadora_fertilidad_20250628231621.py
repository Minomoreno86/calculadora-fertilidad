class EvaluacionFertilidad:
    def __init__(self, edad, duracion_ciclo=None, imc=None, amh=None, tiene_sop=False):
        """
        Constructor del motor de evaluación.
        # NUEVO: Añadidos tiene_sop y duracion_ciclo.
        """
        # --- Factores de Entrada ---
        self.edad = edad
        self.duracion_ciclo = duracion_ciclo
        self.imc = imc
        self.amh = amh
        self.tiene_sop = tiene_sop

        # --- Atributos de Salida (Edad) ---
        self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, self.probabilidad_base_edad_num = "", "", 0.0

        # --- Atributos de Salida (IMC) ---
        self.comentario_imc, self.imc_factor = "", 1.0

        # --- NUEVO: Atributos de Salida (SOP) ---
        self.severidad_sop, self.comentario_sop, self.sop_factor = "No aplica", "", 1.0

        # --- Atributos de Salida (AMH) ---
        self.diagnostico_reserva, self.recomendacion_reserva = "Evaluación no realizada.", ""
        
        # --- Atributo Final ---
        self.probabilidad_ajustada_final = ""
        self.datos_faltantes = []

    def _evaluar_potencial_por_edad(self):
        # (Sin cambios, el mismo de la lección anterior)
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
        # (Sin cambios, el mismo de la lección anterior)
        if self.imc is None:
            self.datos_faltantes.append("Índice de Masa Corporal (IMC)")
            self.comentario_imc = "Dato no proporcionado."
            return
        if self.imc < 18.5: self.comentario_imc, self.imc_factor = "Bajo peso", 0.6
        elif self.imc <= 24.9: self.comentario_imc, self.imc_factor = "Peso normal", 1.0
        elif self.imc <= 29.9: self.comentario_imc, self.imc_factor = "Sobrepeso", 0.85
        elif self.imc <= 34.9: self.comentario_imc, self.imc_factor = "Obesidad", 0.7
        else: self.comentario_imc, self.imc_factor = "Obesidad severa", 0.5
    
    def _evaluar_sop(self):
        """
        # NUEVO: Evalúa la severidad del SOP y determina el factor de ajuste.
        """
        if not self.tiene_sop:
            return # Si no hay SOP, el factor es 1.0 y no hacemos nada.
        
        # Verificación de datos necesarios para clasificar el SOP
        if self.imc is None or self.duracion_ciclo is None:
            self.severidad_sop = "Indeterminada (faltan datos)"
            self.comentario_sop = "Se indicó SOP, pero faltan datos de IMC y/o duración de ciclo para clasificar su severidad y ajustar la probabilidad."
            self.sop_factor = 0.6 # Asignamos un factor moderado por defecto en caso de duda
            if self.imc is None: self.datos_faltantes.append("IMC (necesario para clasificar SOP)")
            if self.duracion_ciclo is None: self.datos_faltantes.append("Duración de ciclo (necesario para clasificar SOP)")
            return
            
        # Lógica de clasificación de severidad del SOP
        if self.imc < 25 and self.duracion_ciclo <= 45:
            self.severidad_sop = "Leve"
            self.comentario_sop = "Ciclos relativamente regulares. El impacto en la fertilidad espontánea es menor, pero existente."
            self.sop_factor = 0.85
        elif self.imc <= 30 and self.duracion_ciclo > 45:
            self.severidad_sop = "Moderado"
            self.comentario_sop = "Anovulación frecuente y/o sobrepeso. La fertilidad espontánea está significativamente reducida."
            self.sop_factor = 0.6
        else: # self.imc > 30 o anovulación persistente (asumida con ciclos muy largos)
            self.severidad_sop = "Severo"
            self.comentario_sop = "Anovulación crónica y/u obesidad. Se recomienda tratamiento especializado como primera línea."
            self.sop_factor = 0.4
            
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

    def ejecutar_evaluacion(self):
        """Orquesta todas las evaluaciones y el cálculo final."""
        self._evaluar_potencial_por_edad()
        self._evaluar_imc()
        self._evaluar_sop() # Se ejecuta después de IMC y ciclo
        self._evaluar_amh()
        
        # Cálculo final con el nuevo factor
        prob_ajustada = self.probabilidad_base_edad_num * self.imc_factor * self.sop_factor
        self.probabilidad_ajustada_final = f"{prob_ajustada:.1f}%"

# --- FASE DE INTERACCIÓN ---

print("--- Módulo de Evaluación de Fertilidad v5 (con Lógica SOP) ---")
edad_str = input("Introduce la edad de la paciente: ")
sop_str = input("¿Tiene diagnóstico de SOP? (si/no): ")
ciclo_str = input("Introduce la duración promedio de su ciclo en días (ej: 30, 45, 60): ")
imc_str = input("Introduce el IMC (kg/m²) (deja en blanco si no lo tienes): ")
amh_str = input("Introduce el nivel de AMH (ng/mL) (deja en blanco si no lo tienes): ")

try:
    edad = int(edad_str)
    tiene_sop = True if sop_str.lower() == 'si' else False
    ciclo = int(ciclo_str) if ciclo_str else None
    imc = float(imc_str) if imc_str else None
    amh = float(amh_str) if amh_str else None

    evaluacion = EvaluacionFertilidad(edad=edad, duracion_ciclo=ciclo, imc=imc, amh=amh, tiene_sop=tiene_sop)
    evaluacion.ejecutar_evaluacion()
    
    print("\n" + "="*15 + " INFORME DE FERTILIDAD " + "="*15)
    print("\n--- 1. Probabilidad de Concepción por Ciclo ---")
    print(f"Probabilidad basal (por edad): {evaluacion.probabilidad_base_edad_str} (aprox. {evaluacion.probabilidad_base_edad_num}%)")
    print(f"Factor de ajuste (por IMC): x{evaluacion.imc_factor}")
    if tiene_sop: print(f"Factor de ajuste (por SOP {evaluacion.severidad_sop}): x{evaluacion.sop_factor}")
    print(f"PROBABILIDAD AJUSTADA FINAL (por ciclo): {evaluacion.probabilidad_ajustada_final}")
    
    print("\n--- 2. Análisis de Factores ---")
    print(f"Potencial por Edad ({edad} años): {evaluacion.diagnostico_potencial_edad}")
    if tiene_sop: print(f"Impacto del SOP ({evaluacion.severidad_sop}): {evaluacion.comentario_sop}")
    if imc: print(f"Impacto del IMC ({imc} kg/m²): {evaluacion.comentario_imc}")
    print(f"Reserva Ovárica (AMH): {evaluacion.diagnostico_reserva}")
    
    if evaluacion.datos_faltantes:
        print("\n" + "-"*40)
        print("Para una evaluación más precisa, se recomienda proporcionar:")
        for dato in evaluacion.datos_faltantes: print(f"- {dato}")
    print("\n" + "="*52)

except ValueError:
    print("\nError: La edad, ciclo, IMC y AMH deben ser números válidos.")