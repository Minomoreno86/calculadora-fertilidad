class EvaluacionFertilidad:
    def __init__(self, edad, duracion_ciclo=None, imc=None, amh=None, prolactina=None, tsh=None, tpo_ab_positivo=False, 
                 insulina_ayunas=None, glicemia_ayunas=None, # NUEVO
                 tiene_sop=False, grado_endometriosis=0, 
                 volumen_seminal=None, concentracion_esperm=None, motilidad_progresiva=None, morfologia_normal=None, vitalidad_esperm=None):
        """
        Constructor del motor de evaluación.
        # NUEVO: Añadidos 'insulina_ayunas' y 'glicemia_ayunas'.
        """
        # --- Factores de Entrada Femeninos ---
        self.edad, self.duracion_ciclo, self.imc, self.amh, self.prolactina, self.tsh, self.tpo_ab_positivo, self.insulina_ayunas, self.glicemia_ayunas, self.tiene_sop, self.grado_endometriosis = \
            edad, duracion_ciclo, imc, amh, prolactina, tsh, tpo_ab_positivo, insulina_ayunas, glicemia_ayunas, tiene_sop, grado_endometriosis
        
        # --- Factores de Entrada Masculinos ---
        self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm = \
            volumen_seminal, concentracion_esperm, motilidad_progresiva, morfologia_normal, vitalidad_esperm

        # --- Atributos de Salida (reseteados) ---
        # ... (atributos anteriores sin cambios) ...
        self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, self.probabilidad_base_edad_num, self.comentario_imc, self.imc_factor, self.severidad_sop, self.comentario_sop, self.sop_factor, self.comentario_endometriosis, self.endometriosis_factor, self.diagnostico_reserva, self.recomendacion_reserva, self.diagnostico_masculino_detallado, self.male_factor, self.comentario_prolactina, self.prolactina_factor, self.comentario_tsh, self.tsh_factor = \
            "", "", 0.0, "", 1.0, "No aplica", "", 1.0, "", 1.0, "Evaluación no realizada.", "", "Normal o sin datos", 1.0, "", 1.0, "", 1.0

        # NUEVO: Atributos para HOMA
        self.homa_calculado = None
        self.comentario_homa, self.homa_factor = "", 1.0
        
        self.probabilidad_ajustada_final = ""
        self.datos_faltantes = []

    # --- MÉTODOS DE EVALUACIÓN (los anteriores no cambian) ---
    def _evaluar_potencial_por_edad(self):
        prob_num=0.0;
        if self.edad<25:self.diagnostico_potencial_edad,self.probabilidad_base_edad_str,prob_num="Alta fertilidad","25-30%",27.5
        elif self.edad<=29:self.diagnostico_potencial_edad,self.probabilidad_base_edad_str,prob_num="Fertilidad muy buena","20-25%",22.5
        elif self.edad<=34:self.diagnostico_potencial_edad,self.probabilidad_base_edad_str,prob_num="Buena fertilidad","15-20%",17.5
        elif self.edad<=37:self.diagnostico_potencial_edad,self.probabilidad_base_edad_str,prob_num="Fecundidad en descenso","10-15%",12.5
        elif self.edad<=40:self.diagnostico_potencial_edad,self.probabilidad_base_edad_str,prob_num="Reducción significativa","5-10%",7.5
        elif self.edad<=42:self.diagnostico_potencial_edad,self.probabilidad_base_edad_str,prob_num="Baja tasa de embarazo","1-5%",3.0
        else:self.diagnostico_potencial_edad,self.probabilidad_base_edad_str,prob_num="Muy baja probabilidad","<1%",0.5
        self.probabilidad_base_edad_num=prob_num
    def _evaluar_imc(self):
        if self.imc is None:return
        if self.imc<18.5:self.comentario_imc,self.imc_factor="Bajo peso",0.6
        elif self.imc<=24.9:self.comentario_imc,self.imc_factor="Peso normal",1.0
        elif self.imc<=29.9:self.comentario_imc,self.imc_factor="Sobrepeso",0.85
        elif self.imc<=34.9:self.comentario_imc,self.imc_factor="Obesidad",0.7
        else:self.comentario_imc,self.imc_factor="Obesidad severa",0.5
    def _evaluar_sop(self):
        if not self.tiene_sop:return
        if self.imc is None or self.duracion_ciclo is None:self.severidad_sop,self.sop_factor="Indeterminada",0.6;return
        if self.imc<25 and self.duracion_ciclo<=45:self.severidad_sop,self.sop_factor="Leve",0.85
        elif self.imc<=30 and self.duracion_ciclo>45:self.severidad_sop,self.sop_factor="Moderado",0.6
        else:self.severidad_sop,self.sop_factor="Severo",0.4
    def _evaluar_endometriosis(self):
        if self.grado_endometriosis==0:return
        if self.grado_endometriosis==1:self.comentario_endometriosis,self.endometriosis_factor="Grado I",0.9
        elif self.grado_endometriosis==2:self.comentario_endometriosis,self.endometriosis_factor="Grado II",0.75
        elif self.grado_endometriosis==3:self.comentario_endometriosis,self.endometriosis_factor="Grado III",0.5
        elif self.grado_endometriosis==4:self.comentario_endometriosis,self.endometriosis_factor="Grado IV",0.3
    def _evaluar_amh(self):
        if self.amh is None:self.datos_faltantes.append("Hormona Antimülleriana (AMH)");return
        if self.amh>3.5:self.diagnostico_reserva="Alta Reserva Ovárica"
        elif self.amh>=1.5:self.diagnostico_reserva="Reserva Ovárica Adecuada"
        elif self.amh>=1.0:self.diagnostico_reserva="Reserva Ovárica Normal-Baja"
        elif self.amh>=0.5:self.diagnostico_reserva="Reserva Ovárica Disminuida"
        else:self.diagnostico_reserva="Muy Baja Reserva Ovárica"
    def _evaluar_prolactina(self):
        if self.prolactina is None:self.datos_faltantes.append("Nivel de Prolactina");return
        if self.prolactina<25:self.comentario_prolactina,self.prolactina_factor="Nivel normal.",1.0
        elif self.prolactina<=50:self.comentario_prolactina,self.prolactina_factor="Hiperprolactinemia leve.",0.8
        elif self.prolactina<=100:self.comentario_prolactina,self.prolactina_factor="Hiperprolactinemia moderada.",0.5
        else:self.comentario_prolactina,self.prolactina_factor="Hiperprolactinemia severa.",0.2
    def _evaluar_tsh(self):
        if self.tsh is None:self.datos_faltantes.append("Nivel de TSH");return
        if self.tsh>2.5 and self.tpo_ab_positivo:self.comentario_tsh,self.tsh_factor="Hipotiroidismo subclínico con autoinmunidad.",0.5
        elif self.tsh>4.0:self.comentario_tsh,self.tsh_factor="Hipotiroidismo clínico.",0.6
        elif self.tsh>2.5:self.comentario_tsh,self.tsh_factor="Hipotiroidismo subclínico.",0.85
        else:self.comentario_tsh,self.tsh_factor="Función tiroidea óptima.",1.0
    def _evaluar_factor_masculino(self):
        alteraciones=[]
        if all(p is None for p in[self.volumen_seminal,self.concentracion_esperm,self.motilidad_progresiva,self.morfologia_normal,self.vitalidad_esperm]):self.datos_faltantes.append("Espermatograma completo");return
        if self.concentracion_esperm==0:alteraciones.append((0.1,"Azoospermia"))
        else:
            if self.concentracion_esperm is not None:
                if self.concentracion_esperm<5:alteraciones.append((0.3,"Oligozoospermia severa"))
                elif self.concentracion_esperm<15:alteraciones.append((0.7,"Oligozoospermia leve"))
            if self.motilidad_progresiva is not None:
                if self.motilidad_progresiva<20:alteraciones.append((0.5,"Astenozoospermia severa"))
                elif self.motilidad_progresiva<32:alteraciones.append((0.85,"Astenozoospermia leve"))
            if self.morfologia_normal is not None and self.morfologia_normal<4:alteraciones.append((0.5,"Teratozoospermia"))
            if self.vitalidad_esperm is not None and self.vitalidad_esperm<58:alteraciones.append((0.3,"Necrozoospermia"))
        if self.volumen_seminal is not None and self.volumen_seminal<1.5:alteraciones.append((0.85,"Hipospermia"))
        if alteraciones:
            alteracion_principal=min(alteraciones,key=lambda item:item[0])
            self.male_factor=alteracion_principal[0]
            self.diagnostico_masculino_detallado=", ".join([item[1] for item in alteraciones])
        else:self.diagnostico_masculino_detallado="Parámetros dentro de la normalidad."

    def _evaluar_indice_homa(self):
        """
        # NUEVO: Calcula el HOMA y determina el factor de ajuste.
        """
        if self.insulina_ayunas is None or self.glicemia_ayunas is None:
            self.datos_faltantes.append("Índice HOMA (requiere Insulina y Glicemia)")
            return
        
        # Cálculo del índice HOMA
        self.homa_calculado = (self.insulina_ayunas * self.glicemia_ayunas) / 405
        
        # Asignación del factor basado en el HOMA calculado
        if self.homa_calculado < 2.5:
            self.comentario_homa = "Sensibilidad a la insulina normal."
            self.homa_factor = 1.0
        elif self.homa_calculado <= 3.9:
            self.comentario_homa = "Resistencia a la insulina leve."
            self.homa_factor = 0.85
        elif self.homa_calculado <= 5.9:
            self.comentario_homa = "Resistencia a la insulina moderada."
            self.homa_factor = 0.7
        else: # HOMA >= 6.0
            self.comentario_homa = "Resistencia a la insulina severa."
            self.homa_factor = 0.5


    def ejecutar_evaluacion(self):
        """Orquesta todas las evaluaciones."""
        self._evaluar_potencial_por_edad()
        self._evaluar_imc()
        self._evaluar_sop()
        self._evaluar_endometriosis()
        self._evaluar_amh()
        self._evaluar_prolactina()
        self._evaluar_tsh()
        self._evaluar_indice_homa() # NUEVO
        self._evaluar_factor_masculino()
        
        # Cálculo final con todos los factores
        prob_ajustada = self.probabilidad_base_edad_num * self.imc_factor * self.sop_factor * self.endometriosis_factor * self.prolactina_factor * self.tsh_factor * self.homa_factor * self.male_factor
        self.probabilidad_ajustada_final = f"{prob_ajustada:.1f}%"

# --- FASE DE INTERACCIÓN ---

print("--- Evaluación de Fertilidad de Pareja v11 (con Índice HOMA) ---")
print("\n--- Datos Femeninos ---")
edad_str = input("Introduce la edad de la paciente: ")
sop_str = input("¿Tiene diagnóstico de SOP? (si/no): ")
ciclo_str = input("Introduce la duración promedio de su ciclo en días (ej: 30): ")
endo_str = input("¿Tiene diagnóstico de endometriosis? (si/no): ")
grado_endo = 0
if endo_str.lower() == 'si':
    grado_str = input("¿Qué grado de endometriosis (1, 2, 3 o 4)?: ")
    grado_endo = int(grado_str) if grado_str in ['1','2','3','4'] else 0
imc_str = input("Introduce el IMC (kg/m²) (deja en blanco si no lo tienes): ")

print("\n--- Datos Endocrinológicos Femeninos ---")
amh_str = input("Nivel de AMH (ng/mL): ")
prl_str = input("Nivel de Prolactina (ng/mL): ")
tsh_str = input("Nivel de TSH (µUI/mL): ")
tpo_str = "no"
if tsh_str and float(tsh_str) > 2.5:
    tpo_str = input("¿Tiene anticuerpos antitiroideos (TPO-Ab) positivos? (si/no): ")
# NUEVOS INPUTS
print("\n--- Perfil Metabólico (para Índice HOMA) ---")
insulina_str = input("Insulina en ayunas (μU/mL): ")
glicemia_str = input("Glicemia en ayunas (mg/dL): ")

print("\n--- Datos Masculinos ---")
# ... (Flujo de espermatograma sin cambios) ...
tiene_esperma_str=input("¿La pareja tiene un análisis de espermatograma? (si/no): ")
vol_str,conc_str,mot_str,morf_str,vit_str=[None]*5
if tiene_esperma_str.lower()=='si':
    print("\n--- Detalle del Espermatograma ---")
    vol_str=input("Volumen (mL): ")
    conc_str=input("Concentración (millones/mL): ")
    mot_str=input("Motilidad progresiva (%): ")
    morf_str=input("Morfología normal (%): ")
    vit_str=input("Vitalidad (%): ")

try:
    evaluacion = EvaluacionFertilidad(
        # ... (asignación de variables)
        edad=int(edad_str), duracion_ciclo=int(ciclo_str) if ciclo_str else None,
        imc=float(imc_str) if imc_str else None, amh=float(amh_str) if amh_str else None,
        prolactina=float(prl_str) if prl_str else None, tsh=float(tsh_str) if tsh_str else None,
        tpo_ab_positivo=(tpo_str.lower() == 'si'),
        insulina_ayunas=float(insulina_str) if insulina_str else None, # NUEVO
        glicemia_ayunas=float(glicemia_str) if glicemia_str else None, # NUEVO
        tiene_sop=(sop_str.lower() == 'si'), grado_endometriosis=grado_endo,
        volumen_seminal=float(vol_str) if vol_str else None, concentracion_esperm=float(conc_str) if conc_str else None,
        motilidad_progresiva=float(mot_str) if mot_str else None, morfologia_normal=float(morf_str) if morf_str else None,
        vitalidad_esperm=float(vit_str) if vit_str else None
    )
    evaluacion.ejecutar_evaluacion()
    
    print("\n" + "="*15 + " INFORME DE FERTILIDAD DE PAREJA " + "="*15)
    print("\n--- 1. Pronóstico de Concepción por Ciclo ---")
    print(f"Probabilidad basal (por edad femenina): {evaluacion.probabilidad_base_edad_num}%")
    factores_ginecologicos = evaluacion.imc_factor * evaluacion.sop_factor * evaluacion.endometriosis_factor
    factores_endocrinos = evaluacion.prolactina_factor * evaluacion.tsh_factor * evaluacion.homa_factor # NUEVO
    print(f"  x Factores Ginecológicos (IMC, SOP, Endo): {factores_ginecologicos:.2f}")
    print(f"  x Factores Endocrinos (PRL, TSH, HOMA): {factores_endocrinos:.2f}")
    print(f"  x Factor Masculino: {evaluacion.male_factor:.2f}")
    print("-" * 52)
    print(f"PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO: {evaluacion.probabilidad_ajustada_final}")
    print("-" * 52)

    print("\n--- 2. Análisis Detallado de Factores ---")
    print("Femeninos:")
    # ... (print factores femeninos detallado) ...
    print(f"  - Edad ({evaluacion.edad} años): {evaluacion.diagnostico_potencial_edad}")
    if evaluacion.grado_endometriosis>0:print(f"  - Endometriosis: {evaluacion.comentario_endometriosis}")
    if evaluacion.tiene_sop:print(f"  - SOP: {evaluacion.severidad_sop}")
    if evaluacion.imc:print(f"  - IMC ({evaluacion.imc} kg/m²): {evaluacion.comentario_imc}")
    if evaluacion.homa_calculado:print(f"  - Resistencia a Insulina (HOMA: {evaluacion.homa_calculado:.2f}): {evaluacion.comentario_homa}") # NUEVO
    print(f"  - Reserva Ovárica (AMH): {evaluacion.diagnostico_reserva}")
    if evaluacion.prolactina:print(f"  - Prolactina: {evaluacion.comentario_prolactina}")
    if evaluacion.tsh:print(f"  - Función Tiroidea (TSH): {evaluacion.comentario_tsh}")
    
    print("Masculinos:")
    print(f"  - Espermatograma: {evaluacion.diagnostico_masculino_detallado}")

    if evaluacion.datos_faltantes:
        # ... (print datos faltantes)
        print("\n" + "-"*40)
        print("Para una evaluación más precisa, se recomienda proporcionar:")
        for dato in evaluacion.datos_faltantes:print(f"- {dato}")
    print("\n" + "="*52)

except ValueError:
    print("\nError: Todos los datos numéricos deben ser válidos.")