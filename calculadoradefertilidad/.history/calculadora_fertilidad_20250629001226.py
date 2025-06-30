# calculadora_fertilidad.py (Refactorizado y con Recomendaciones)

# NUEVO: Importamos el diccionario de recomendaciones desde nuestro nuevo archivo.
from textos_clinicos import RECOMENDACIONES

class EvaluacionFertilidad:
    def __init__(self, edad, duracion_ciclo=None, imc=None, amh=None, prolactina=None, tsh=None, tpo_ab_positivo=False, 
                 insulina_ayunas=None, glicemia_ayunas=None, 
                 tiene_sop=False, grado_endometriosis=0, 
                 tiene_miomas=False, mioma_submucoso=False, mioma_submucoso_multiple=False, 
                 mioma_intramural_significativo=False, mioma_subseroso_grande=False,
                 tipo_adenomiosis="", tipo_polipo="", resultado_hsg="",
                 volumen_seminal=None, concentracion_esperm=None, motilidad_progresiva=None, morfologia_normal=None, vitalidad_esperm=None):
        """ Constructor completo del motor de evaluación. """
        # Asignación de todos los factores de entrada
        self.edad, self.duracion_ciclo, self.imc, self.amh, self.prolactina, self.tsh, self.tpo_ab_positivo, self.insulina_ayunas, self.glicemia_ayunas, self.tiene_sop, self.grado_endometriosis, self.tipo_adenomiosis, self.tipo_polipo, self.resultado_hsg = edad, duracion_ciclo, imc, amh, prolactina, tsh, tpo_ab_positivo, insulina_ayunas, glicemia_ayunas, tiene_sop, grado_endometriosis, tipo_adenomiosis, tipo_polipo, resultado_hsg
        self.tiene_miomas, self.mioma_submucoso, self.mioma_submucoso_multiple, self.mioma_intramural_significativo, self.mioma_subseroso_grande = tiene_miomas, mioma_submucoso, mioma_submucoso_multiple, mioma_intramural_significativo, mioma_subseroso_grande
        self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm = volumen_seminal, concentracion_esperm, motilidad_progresiva, morfologia_normal, vitalidad_esperm

        # --- Atributos de Salida (reseteados) ---
        self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, self.probabilidad_base_edad_num, self.comentario_imc, self.imc_factor, self.severidad_sop, self.comentario_sop, self.sop_factor, self.comentario_endometriosis, self.endometriosis_factor, self.comentario_miomas, self.mioma_factor, self.comentario_adenomiosis, self.adenomiosis_factor, self.comentario_polipo, self.polipo_factor, self.comentario_hsg, self.hsg_factor, self.diagnostico_reserva, self.recomendacion_reserva, self.diagnostico_masculino_detallado, self.male_factor, self.comentario_prolactina, self.prolactina_factor, self.comentario_tsh, self.tsh_factor, self.homa_calculado, self.comentario_homa, self.homa_factor = "", "", 0.0, "", 1.0, "No aplica", "", 1.0, "", 1.0, "", 1.0, "", 1.0, "", 1.0, "", 1.0, "Evaluación no realizada.", "", "Normal o sin datos", 1.0, "", 1.0, "", 1.0, None, "", 1.0
        
        self.probabilidad_ajustada_final = ""
        self.datos_faltantes = []
        # NUEVO: La lista que contendrá todas las recomendaciones.
        self.recomendaciones_lista = []

    def _evaluar_potencial_por_edad(self):
        prob_num=0.0
        if self.edad < 35: pass
        elif self.edad <= 37: self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_35"])
        elif self.edad <= 40: self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_38"])
        elif self.edad <= 42: self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_40"])
        else: self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_43"])
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
        if self.imc < 18.5: self.comentario_imc, self.imc_factor = "Bajo peso", 0.6; self.recomendaciones_lista.append(RECOMENDACIONES["IMC_BAJO"])
        elif self.imc <= 24.9: self.comentario_imc, self.imc_factor = "Peso normal", 1.0
        elif self.imc > 24.9: self.comentario_imc, self.imc_factor = "Sobrepeso/Obesidad", 0.85; self.recomendaciones_lista.append(RECOMENDACIONES["IMC_ALTO"])

    def _evaluar_sop(self):
        if not self.tiene_sop: return
        self.recomendaciones_lista.append(RECOMENDACIONES["SOP"])
        if self.imc is None or self.duracion_ciclo is None: self.severidad_sop, self.sop_factor = "Indeterminada", 0.6; return
        if self.imc < 25 and self.duracion_ciclo <= 45: self.severidad_sop, self.sop_factor = "Leve", 0.85
        elif self.imc <= 30 and self.duracion_ciclo > 45: self.severidad_sop, self.sop_factor = "Moderado", 0.6
        else: self.severidad_sop, self.sop_factor = "Severo", 0.4

    def _evaluar_endometriosis(self):
        if self.grado_endometriosis == 0: return
        if self.grado_endometriosis <= 2: self.comentario_endometriosis, self.endometriosis_factor = f"Grado {self.grado_endometriosis}", 0.8; self.recomendaciones_lista.append(RECOMENDACIONES["ENDO_LEVE"])
        else: self.comentario_endometriosis, self.endometriosis_factor = f"Grado {self.grado_endometriosis}", 0.4; self.recomendaciones_lista.append(RECOMENDACIONES["ENDO_SEVERA"])
        
    def _evaluar_miomatosis(self):
        if not self.tiene_miomas: return
        if self.mioma_submucoso: self.comentario_miomas, self.mioma_factor = "Miomatosis submucosa", 0.35; self.recomendaciones_lista.append(RECOMENDACIONES["MIOMA_SUBMUCOSO"])
        elif self.mioma_intramural_significativo: self.comentario_miomas, self.mioma_factor = "Miomatosis intramural significativa", 0.6; self.recomendaciones_lista.append(RECOMENDACIONES["MIOMA_INTRAMURAL"])
        elif self.mioma_subseroso_grande: self.comentario_miomas, self.mioma_factor = "Miomatosis subserosa grande", 0.85; self.recomendaciones_lista.append(RECOMENDACIONES["MIOMA_SUBSEROSO"])
        else: self.comentario_miomas, self.mioma_factor = "Miomatosis sin impacto cavitario", 1.0

    def _evaluar_adenomiosis(self):
        if not self.tipo_adenomiosis: return
        if self.tipo_adenomiosis == "focal": self.comentario_adenomiosis, self.adenomiosis_factor = "Adenomiosis Focal", 0.85; self.recomendaciones_lista.append(RECOMENDACIONES["ADENO_FOCAL"])
        else: self.comentario_adenomiosis, self.adenomiosis_factor = f"Adenomiosis Difusa", 0.5; self.recomendaciones_lista.append(RECOMENDACIONES["ADENO_DIFUSA"])

    def _evaluar_polipos(self):
        if not self.tipo_polipo: return
        self.comentario_polipo, self.polipo_factor = "Pólipo(s) endometrial(es)", 0.7; self.recomendaciones_lista.append(RECOMENDACIONES["POLIPO"])

    def _evaluar_hsg(self):
        if not self.resultado_hsg: self.datos_faltantes.append("Resultado de Histerosalpingografía (HSG)"); return
        if self.resultado_hsg == "normal": self.comentario_hsg, self.hsg_factor = "Ambas trompas permeables", 1.0
        elif self.resultado_hsg == "unilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción tubárica unilateral", 0.7; self.recomendaciones_lista.append(RECOMENDACIONES["HSG_UNILATERAL"])
        elif self.resultado_hsg == "bilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción tubárica bilateral", 0.0; self.recomendaciones_lista.append(RECOMENDACIONES["HSG_BILATERAL"])
        elif self.resultado_hsg == "defecto_uterino": self.comentario_hsg, self.hsg_factor = "Alteración de la cavidad uterina", 0.3; self.recomendaciones_lista.append(RECOMENDACIONES["HSG_DEFECTO"])

    def _evaluar_amh(self):
        if self.amh is None: self.datos_faltantes.append("Hormona Antimülleriana (AMH)"); return
        if self.amh > 3.5: self.diagnostico_reserva = "Alta Reserva Ovárica"
        elif self.amh >= 1.5: self.diagnostico_reserva = "Reserva Ovárica Adecuada"
        elif self.amh < 1.0: self.diagnostico_reserva = "Baja Reserva Ovárica"; self.recomendaciones_lista.append(RECOMENDACIONES["AMH_BAJA"])
        
    def _evaluar_prolactina(self):
        if self.prolactina is None: self.datos_faltantes.append("Nivel de Prolactina"); return
        if self.prolactina >= 25: self.comentario_prolactina, self.prolactina_factor = "Hiperprolactinemia", 0.6; self.recomendaciones_lista.append(RECOMENDACIONES["PRL_ALTA"])

    def _evaluar_tsh(self):
        if self.tsh is None: self.datos_faltantes.append("Nivel de TSH"); return
        if self.tsh > 2.5: self.comentario_tsh, self.tsh_factor = "Función tiroidea no óptima", 0.7; self.recomendaciones_lista.append(RECOMENDACIONES["TSH_ALTA"])
        if self.tpo_ab_positivo: self.recomendaciones_lista.append(RECOMENDACIONES["TPO_POSITIVO"])
        
    def _evaluar_indice_homa(self):
        if self.insulina_ayunas is None or self.glicemia_ayunas is None: self.datos_faltantes.append("Índice HOMA"); return
        self.homa_calculado = (self.insulina_ayunas * self.glicemia_ayunas) / 405
        if self.homa_calculado >= 2.5: self.comentario_homa, self.homa_factor = "Resistencia a la insulina", 0.8; self.recomendaciones_lista.append(RECOMENDACIONES["HOMA_ALTO"])

    def _evaluar_factor_masculino(self):
        alteraciones = []
        if all(p is None for p in [self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm]): self.datos_faltantes.append("Espermatograma completo"); return
        if self.concentracion_esperm == 0: alteraciones.append((0.1, "Azoospermia"))
        else:
            if self.concentracion_esperm is not None and self.concentracion_esperm < 15: alteraciones.append((0.7, "Oligozoospermia"))
            if self.motilidad_progresiva is not None and self.motilidad_progresiva < 32: alteraciones.append((0.85, "Astenozoospermia"))
            if self.morfologia_normal is not None and self.morfologia_normal < 4: alteraciones.append((0.5, "Teratozoospermia"))
            if self.vitalidad_esperm is not None and self.vitalidad_esperm < 58: alteraciones.append((0.3, "Necrozoospermia"))
        if self.volumen_seminal is not None and self.volumen_seminal < 1.5: alteraciones.append((0.85, "Hipospermia"))
        if alteraciones:
            alteracion_principal = min(alteraciones, key=lambda item: item[0])
            self.male_factor = alteracion_principal[0]
            self.diagnostico_masculino_detallado = ", ".join([item[1] for item in alteraciones])
            self.recomendaciones_lista.append(RECOMENDACIONES["FACTOR_MASCULINO"])
        else: self.diagnostico_masculino_detallado = "Parámetros dentro de la normalidad."

    def ejecutar_evaluacion(self):
        metodos_evaluacion = [self._evaluar_potencial_por_edad, self._evaluar_imc, self._evaluar_sop, self._evaluar_endometriosis, self._evaluar_miomatosis, self._evaluar_adenomiosis, self._evaluar_polipos, self._evaluar_hsg, self._evaluar_amh, self._evaluar_prolactina, self._evaluar_tsh, self._evaluar_indice_homa, self._evaluar_factor_masculino]
        for metodo in metodos_evaluacion: metodo()
        
        prob_ajustada = self.probabilidad_base_edad_num * self.imc_factor * self.sop_factor * self.endometriosis_factor * self.mioma_factor * self.adenomiosis_factor * self.polipo_factor * self.hsg_factor * self.prolactina_factor * self.tsh_factor * self.homa_factor * self.male_factor
        self.probabilidad_ajustada_final = f"{prob_ajustada:.1f}%"

# ===================================================================
# PARTE 2: BLOQUE DE EJECUCIÓN (El que "enciende" el motor)
# ===================================================================

print("--- Evaluación de Fertilidad de Pareja v16 (Refactorizado con Recomendaciones) ---")
# (Aquí va todo el bloque de inputs, que es idéntico al de la lección anterior)
# ...
try:
    # (Aquí va toda la creación de la instancia de la clase, que es idéntica a la anterior)
    # ...
    evaluacion = EvaluacionFertilidad( # ... todos los parámetros ...
    )
    evaluacion.ejecutar_evaluacion()
    
    # (El bloque del informe ahora incluye la sección de recomendaciones)
    print("\n" + "="*15 + " INFORME DE FERTILIDAD DE PAREJA " + "="*15)
    # ... (Print de la sección 1 - Pronóstico) ...
    print("\n--- 2. Análisis Detallado de Factores ---")
    # ... (Print de la sección 2 - Diagnósticos) ...
    
    # NUEVO: Sección de recomendaciones
    if evaluacion.recomendaciones_lista:
        # Usamos set() para eliminar recomendaciones duplicadas y luego lo convertimos a lista para mantener un orden
        recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
        print("\n--- 3. PLAN DE ACCIÓN Y RECOMENDACIONES ---")
        for i, rec in enumerate(recomendaciones_unicas, 1):
            print(f"  {i}. {rec}")

    if evaluacion.datos_faltantes:
        print("\n" + "-"*40)
        print("Para una evaluación más precisa, se recomienda proporcionar:")
        for dato in evaluacion.datos_faltantes: print(f"- {dato}")
    print("\n" + "="*52)

except Exception as e:
    print(f"\nHa ocurrido un error inesperado: {e}")