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
        self.edad, self.duracion_ciclo, self.imc, self.amh, self.prolactina, self.tsh, self.tpo_ab_positivo, self.insulina_ayunas, self.glicemia_ayunas, self.tiene_sop, self.grado_endometriosis, self.tipo_adenomiosis, self.tipo_polipo, self.resultado_hsg = \
            edad, duracion_ciclo, imc, amh, prolactina, tsh, tpo_ab_positivo, insulina_ayunas, glicemia_ayunas, tiene_sop, grado_endometriosis, tipo_adenomiosis, tipo_polipo, resultado_hsg
        self.tiene_miomas, self.mioma_submucoso, self.mioma_submucoso_multiple, self.mioma_intramural_significativo, self.mioma_subseroso_grande = \
            tiene_miomas, mioma_submucoso, mioma_submucoso_multiple, mioma_intramural_significativo, mioma_subseroso_grande
        self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm = \
            volumen_seminal, concentracion_esperm, motilidad_progresiva, morfologia_normal, vitalidad_esperm

        # --- Atributos de Salida (reseteados) ---
        self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, self.probabilidad_base_edad_num, self.comentario_imc, self.imc_factor, self.severidad_sop, self.comentario_sop, self.sop_factor, self.comentario_endometriosis, self.endometriosis_factor, self.comentario_miomas, self.mioma_factor, self.comentario_adenomiosis, self.adenomiosis_factor, self.comentario_polipo, self.polipo_factor, self.comentario_hsg, self.hsg_factor, self.diagnostico_reserva, self.recomendacion_reserva, self.diagnostico_masculino_detallado, self.male_factor, self.comentario_prolactina, self.prolactina_factor, self.comentario_tsh, self.tsh_factor, self.homa_calculado, self.comentario_homa, self.homa_factor = \
            "", "", 0.0, "", 1.0, "No aplica", "", 1.0, "", 1.0, "", 1.0, "", 1.0, "", 1.0, "", 1.0, "Evaluación no realizada.", "", "Normal o sin datos", 1.0, "", 1.0, "", 1.0, None, "", 1.0
        
        self.probabilidad_ajustada_final = ""
        self.datos_faltantes = []

    def _evaluar_potencial_por_edad(self):
        prob_num=0.0
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

    def _evaluar_miomatosis(self):
        if not self.tiene_miomas: return
        if self.mioma_submucoso and self.mioma_submucoso_multiple: self.comentario_miomas, self.mioma_factor = "Miomatosis submucosa múltiple", 0.3
        elif self.mioma_submucoso: self.comentario_miomas, self.mioma_factor = "Miomatosis submucosa única", 0.4
        elif self.mioma_intramural_significativo: self.comentario_miomas, self.mioma_factor = "Miomatosis intramural significativa", 0.6
        elif self.mioma_subseroso_grande: self.comentario_miomas, self.mioma_factor = "Miomatosis subserosa grande", 0.5
        elif self.tiene_miomas: self.comentario_miomas, self.mioma_factor = "Miomatosis sin impacto cavitario", 0.8
        else: self.comentario_miomas, self.mioma_factor = "Miomatosis subserosa leve", 1.0

    def _evaluar_adenomiosis(self):
        if not self.tipo_adenomiosis: return
        if self.tipo_adenomiosis == "focal": self.comentario_adenomiosis, self.adenomiosis_factor = "Adenomiosis Focal", 0.85
        elif self.tipo_adenomiosis == "difusa_leve": self.comentario_adenomiosis, self.adenomiosis_factor = "Adenomiosis Difusa Leve", 0.7
        elif self.tipo_adenomiosis == "difusa_severa": self.comentario_adenomiosis, self.adenomiosis_factor = "Adenomiosis Difusa Severa", 0.4

    def _evaluar_polipos(self):
        if not self.tipo_polipo: return
        if self.tipo_polipo == "pequeno_unico": self.comentario_polipo, self.polipo_factor = "Pólipo único < 1cm", 0.9
        elif self.tipo_polipo == "moderado_multiple": self.comentario_polipo, self.polipo_factor = "Pólipo moderado o múltiples", 0.7
        elif self.tipo_polipo == "grande": self.comentario_polipo, self.polipo_factor = "Pólipo grande (>2cm)", 0.5

    def _evaluar_hsg(self):
        if not self.resultado_hsg: self.datos_faltantes.append("Resultado de Histerosalpingografía (HSG)"); return
        if self.resultado_hsg == "normal": self.comentario_hsg, self.hsg_factor = "Ambas trompas permeables", 1.0
        elif self.resultado_hsg == "unilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción tubárica unilateral", 0.7
        elif self.resultado_hsg == "defecto_uterino": self.comentario_hsg, self.hsg_factor = "Alteración de la cavidad uterina", 0.3
        elif self.resultado_hsg == "bilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción tubárica bilateral", 0.0

    def _evaluar_amh(self):
        if self.amh is None: self.datos_faltantes.append("Hormona Antimülleriana (AMH)"); return
        if self.amh > 3.5: self.diagnostico_reserva = "Alta Reserva Ovárica"
        elif self.amh >= 1.5: self.diagnostico_reserva = "Reserva Ovárica Adecuada"
        elif self.amh >= 1.0: self.diagnostico_reserva = "Reserva Ovárica Normal-Baja"
        elif self.amh >= 0.5: self.diagnostico_reserva = "Reserva Ovárica Disminuida"
        else: self.diagnostico_reserva = "Muy Baja Reserva Ovárica"

    def _evaluar_prolactina(self):
        if self.prolactina is None: self.datos_faltantes.append("Nivel de Prolactina"); return
        if self.prolactina < 25: self.comentario_prolactina, self.prolactina_factor = "Nivel normal", 1.0
        elif self.prolactina <= 50: self.comentario_prolactina, self.prolactina_factor = "Hiperprolactinemia leve", 0.8
        elif self.prolactina <= 100: self.comentario_prolactina, self.prolactina_factor = "Hiperprolactinemia moderada", 0.5
        else: self.comentario_prolactina, self.prolactina_factor = "Hiperprolactinemia severa", 0.2

    def _evaluar_tsh(self):
        if self.tsh is None: self.datos_faltantes.append("Nivel de TSH"); return
        if self.tsh > 2.5 and self.tpo_ab_positivo: self.comentario_tsh, self.tsh_factor = "Hipotiroidismo subclínico con autoinmunidad", 0.5
        elif self.tsh > 4.0: self.comentario_tsh, self.tsh_factor = "Hipotiroidismo clínico", 0.6
        elif self.tsh > 2.5: self.comentario_tsh, self.tsh_factor = "Hipotiroidismo subclínico", 0.85
        else: self.comentario_tsh, self.tsh_factor = "Función tiroidea óptima", 1.0

    def _evaluar_indice_homa(self):
        if self.insulina_ayunas is None or self.glicemia_ayunas is None: self.datos_faltantes.append("Índice HOMA"); return
        self.homa_calculado = (self.insulina_ayunas * self.glicemia_ayunas) / 405
        if self.homa_calculado < 2.5: self.comentario_homa, self.homa_factor = "Sensibilidad a la insulina normal", 1.0
        elif self.homa_calculado <= 3.9: self.comentario_homa, self.homa_factor = "Resistencia a la insulina leve", 0.85
        elif self.homa_calculado <= 5.9: self.comentario_homa, self.homa_factor = "Resistencia a la insulina moderada", 0.7
        else: self.comentario_homa, self.homa_factor = "Resistencia a la insulina severa", 0.5

    def _evaluar_factor_masculino(self):
        alteraciones = []
        if all(p is None for p in [self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm]): self.datos_faltantes.append("Espermatograma completo"); return
        if self.concentracion_esperm == 0: alteraciones.append((0.1, "Azoospermia"))
        else:
            if self.concentracion_esperm is not None:
                if self.concentracion_esperm < 5: alteraciones.append((0.3, "Oligozoospermia severa"))
                elif self.concentracion_esperm < 15: alteraciones.append((0.7, "Oligozoospermia leve"))
            if self.motilidad_progresiva is not None:
                if self.motilidad_progresiva < 20: alteraciones.append((0.5, "Astenozoospermia severa"))
                elif self.motilidad_progresiva < 32: alteraciones.append((0.85, "Astenozoospermia leve"))
            if self.morfologia_normal is not None and self.morfologia_normal < 4: alteraciones.append((0.5, "Teratozoospermia"))
            if self.vitalidad_esperm is not None and self.vitalidad_esperm < 58: alteraciones.append((0.3, "Necrozoospermia"))
        if self.volumen_seminal is not None and self.volumen_seminal < 1.5: alteraciones.append((0.85, "Hipospermia"))
        if alteraciones:
            alteracion_principal = min(alteraciones, key=lambda item: item[0])
            self.male_factor = alteracion_principal[0]
            self.diagnostico_masculino_detallado = ", ".join([item[1] for item in alteraciones])
        else: self.diagnostico_masculino_detallado = "Parámetros dentro de la normalidad."

    def ejecutar_evaluacion(self):
        """Orquesta todas las evaluaciones."""
        self._evaluar_potencial_por_edad()
        self._evaluar_imc()
        self._evaluar_sop()
        self._evaluar_endometriosis()
        self._evaluar_miomatosis()
        self._evaluar_adenomiosis()
        self._evaluar_polipos()
        self._evaluar_hsg()
        self._evaluar_amh()
        self._evaluar_prolactina()
        self._evaluar_tsh()
        self._evaluar_indice_homa()
        self._evaluar_factor_masculino()
        
        prob_ajustada = self.probabilidad_base_edad_num * self.imc_factor * self.sop_factor * self.endometriosis_factor * self.mioma_factor * self.adenomiosis_factor * self.polipo_factor * self.hsg_factor * self.prolactina_factor * self.tsh_factor * self.homa_factor * self.male_factor
        self.probabilidad_ajustada_final = f"{prob_ajustada:.1f}%"