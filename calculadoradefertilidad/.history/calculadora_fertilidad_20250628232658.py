class EvaluacionFertilidad:
    def __init__(self, edad, duracion_ciclo=None, imc=None, amh=None, tiene_sop=False, grado_endometriosis=0, 
                 volumen_seminal=None, concentracion_esperm=None, motilidad_progresiva=None, morfologia_normal=None, vitalidad_esperm=None):
        """
        Constructor del motor de evaluación.
        # NUEVO: Añadidos todos los parámetros del Factor Masculino.
        """
        # --- Factores de Entrada Femeninos ---
        self.edad, self.duracion_ciclo, self.imc, self.amh, self.tiene_sop, self.grado_endometriosis = \
            edad, duracion_ciclo, imc, amh, tiene_sop, grado_endometriosis
        
        # --- NUEVO: Factores de Entrada Masculinos ---
        self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm = \
            volumen_seminal, concentracion_esperm, motilidad_progresiva, morfologia_normal, vitalidad_esperm

        # --- Atributos de Salida (reseteados para cada ejecución) ---
        self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, self.probabilidad_base_edad_num = "", "", 0.0
        self.comentario_imc, self.imc_factor = "", 1.0
        self.severidad_sop, self.comentario_sop, self.sop_factor = "No aplica", "", 1.0
        self.comentario_endometriosis, self.endometriosis_factor = "", 1.0
        self.diagnostico_reserva, self.recomendacion_reserva = "Evaluación no realizada.", ""
        # NUEVO: Atributos para Factor Masculino
        self.comentario_masculino, self.male_factor = "Normal o sin datos", 1.0
        
        self.probabilidad_ajustada_final = ""
        self.datos_faltantes = []

    # --- MÉTODOS DE EVALUACIÓN FEMENINOS (sin cambios) ---
    def _evaluar_potencial_por_edad(self):
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
        if self.imc is None: return
        if self.imc < 18.5: self.comentario_imc, self.imc_factor = "Bajo peso", 0.6
        elif self.imc <= 24.9: self.comentario_imc, self.imc_factor = "Peso normal", 1.0
        elif self.imc <= 29.9: self.comentario_imc, self.imc_factor = "Sobrepeso", 0.85
        elif self.imc <= 34.9: self.comentario_imc, self.imc_factor = "Obesidad", 0.7
        else: self.comentario_imc, self.imc_factor = "Obesidad severa", 0.5
    def _evaluar_sop(self):
        if not self.tiene_sop: return
        if self.imc is None or self.duracion_ciclo is None: self.severidad_sop, self.sop_factor = "Indeterminada", 0.6; return
        if self.imc < 25 and self.duracion_ciclo <= 45: self.severidad_sop, self.sop_factor = "Leve", 0.85
        elif self.imc <= 30 and self.duracion_ciclo > 45: self.severidad_sop, self.sop_factor = "Moderado", 0.6
        else: self.severidad_sop, self.sop_factor = "Severo", 0.4
    def _evaluar_endometriosis(self):
        if self.grado_endometriosis == 0: return
        if self.grado_endometriosis == 1: self.comentario_endometriosis, self.endometriosis_factor = "Grado I", 0.9
        elif self.grado_endometriosis == 2: self.comentario_endometriosis, self.endometriosis_factor = "Grado II", 0.75
        elif self.grado_endometriosis == 3: self.comentario_endometriosis, self.endometriosis_factor = "Grado III", 0.5
        elif self.grado_endometriosis == 4: self.comentario_endometriosis, self.endometriosis_factor = "Grado IV", 0.3
    def _evaluar_amh(self):
        if self.amh is None: return
        if self.amh > 3.5: self.diagnostico_reserva = "Alta Reserva Ovárica"
        elif self.amh >= 1.5: self.diagnostico_reserva = "Reserva Ovárica Adecuada"
        elif self.amh >= 1.0: self.diagnostico_reserva = "Reserva Ovárica Normal-Baja"
        elif self.amh >= 0.5: self.diagnostico_reserva = "Reserva Ovárica Disminuida"
        else: self.diagnostico_reserva = "Muy Baja Reserva Ovárica"
    
    def _evaluar_factor_masculino(self):
        """
        # NUEVO: Evalúa todos los parámetros masculinos y escoge el factor más severo.
        """
        alteraciones = [] # Lista para guardar las alteraciones encontradas (factor, comentario)
        
        # Si no se proporciona ningún dato, no hacemos nada.
        if all(p is None for p in [self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm]):
            self.datos_faltantes.append("Espermatograma completo")
            return

        # 1. Azoospermia (la condición más severa, se revisa primero)
        if self.concentracion_esperm == 0:
            alteraciones.append((0.1, "Azoospermia: Ausencia de espermatozoides. Requiere valoración especializada urgente."))
        else:
            # 2. Concentración
            if self.concentracion_esperm is not None:
                if self.concentracion_esperm < 5: alteraciones.append((0.3, "Oligozoospermia severa (<5M/mL)"))
                elif self.concentracion_esperm < 15: alteraciones.append((0.7, "Oligozoospermia leve (5-14M/mL)"))
            # 3. Motilidad
            if self.motilidad_progresiva is not None:
                if self.motilidad_progresiva < 20: alteraciones.append((0.5, "Astenozoospermia severa (<20%)"))
                elif self.motilidad_progresiva < 32: alteraciones.append((0.85, "Astenozoospermia leve (20-31%)"))
            # 4. Morfología
            if self.morfologia_normal is not None and self.morfologia_normal < 4:
                alteraciones.append((0.5, "Teratozoospermia (<4% normales)"))
            # 5. Vitalidad
            if self.vitalidad_esperm is not None and self.vitalidad_esperm < 58:
                alteraciones.append((0.3, "Necrozoospermia (<58% vivos)"))
        
        # 6. Volumen
        if self.volumen_seminal is not None and self.volumen_seminal < 1.5:
            alteraciones.append((0.85, "Hipospermia (<1.5 mL)"))

        # Si encontramos alguna alteración, escogemos la más severa (la de menor factor)
        if alteraciones:
            alteracion_principal = min(alteraciones, key=lambda item: item[0])
            self.male_factor = alteracion_principal[0]
            self.comentario_masculino = alteracion_principal[1]

    def ejecutar_evaluacion(self):
        """Orquesta todas las evaluaciones, incluyendo el nuevo factor masculino."""
        # Factores Femeninos
        self._evaluar_potencial_por_edad()
        self._evaluar_imc()
        self._evaluar_sop()
        self._evaluar_endometriosis()
        self._evaluar_amh()
        # Factor Masculino
        self._evaluar_factor_masculino()
        
        # Cálculo final con todos los factores
        prob_ajustada = self.probabilidad_base_edad_num * self.imc_factor * self.sop_factor * self.endometriosis_factor * self.male_factor
        self.probabilidad_ajustada_final = f"{prob_ajustada:.1f}%"

# --- FASE DE INTERACCIÓN (Ahora mucho más completa) ---

print("--- Evaluación de Fertilidad de Pareja v7 ---")
print("\n--- Datos Femeninos ---")
# ... (código de input para mujer, igual al anterior)
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

print("\n--- Datos Masculinos (Espermatograma) ---")
# NUEVO: Inputs para el factor masculino
vol_str = input("Volumen (mL): ")
conc_str = input("Concentración (millones/mL): ")
mot_str = input("Motilidad progresiva (%): ")
morf_str = input("Morfología normal (%): ")
vit_str = input("Vitalidad (%): ")

try:
    evaluacion = EvaluacionFertilidad(
        # Inputs femeninos
        edad=int(edad_str),
        duracion_ciclo=int(ciclo_str) if ciclo_str else None,
        imc=float(imc_str) if imc_str else None,
        amh=float(amh_str) if amh_str else None,
        tiene_sop=(sop_str.lower() == 'si'),
        grado_endometriosis=grado_endo,
        # Inputs masculinos
        volumen_seminal=float(vol_str) if vol_str else None,
        concentracion_esperm=float(conc_str) if conc_str else None,
        motilidad_progresiva=float(mot_str) if mot_str else None,
        morfologia_normal=float(morf_str) if morf_str else None,
        vitalidad_esperm=float(vit_str) if vit_str else None
    )
    evaluacion.ejecutar_evaluacion()
    
    print("\n" + "="*15 + " INFORME DE FERTILIDAD DE PAREJA " + "="*15)
    print("\n--- 1. Pronóstico de Concepción por Ciclo ---")
    print(f"Probabilidad basal (por edad femenina): {evaluacion.probabilidad_base_edad_num}%")
    print(f"  x Factor Femenino (combinado): {(evaluacion.imc_factor * evaluacion.sop_factor * evaluacion.endometriosis_factor):.2f}")
    print(f"  x Factor Masculino ({evaluacion.comentario_masculino}): {evaluacion.male_factor}")
    print("-" * 52)
    print(f"PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO: {evaluacion.probabilidad_ajustada_final}")
    print("-" * 52)

    print("\n--- 2. Análisis Detallado de Factores ---")
    print("Femeninos:")
    print(f"  - Edad ({evaluacion.edad} años): {evaluacion.diagnostico_potencial_edad}")
    if evaluacion.grado_endometriosis > 0: print(f"  - Endometriosis: {evaluacion.comentario_endometriosis}")
    if evaluacion.tiene_sop: print(f"  - SOP: {evaluacion.severidad_sop}")
    if evaluacion.imc: print(f"  - IMC ({evaluacion.imc} kg/m²): {evaluacion.comentario_imc}")
    print(f"  - Reserva Ovárica (AMH): {evaluacion.diagnostico_reserva}")
    print("Masculinos:")
    print(f"  - Espermatograma: {evaluacion.comentario_masculino}")

    if evaluacion.datos_faltantes:
        print("\n" + "-"*40)
        print("Para una evaluación más precisa, se recomienda proporcionar:")
        for dato in evaluacion.datos_faltantes: print(f"- {dato}")
    print("\n" + "="*52)

except ValueError:
    print("\nError: Todos los datos numéricos deben ser válidos.")