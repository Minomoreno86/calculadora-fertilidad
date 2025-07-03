import numpy as np

# ✅ BUENA PRÁCTICA: Asegúrate de que los imports no estén duplicados.
from textos_clinicos import RECOMENDACIONES
from config import BENCHMARK_PRONOSTICO_POR_EDAD, CLINICAL_INSIGHTS

class EvaluacionFertilidad:
    """
    Calcula el pronóstico de fertilidad basado en múltiples factores clínicos.
    Versión final refactorizada para máxima legibilidad, robustez y mantenibilidad.
    """
    def __init__(self, **datos):
        """
        Constructor de la clase. Llama a la asignación de datos
        y al reseteo de atributos de salida.
        """
        self._asignar_datos_entrada(datos)
        self._reset_output_attributes()

    def _asignar_datos_entrada(self, datos):
        """Asigna los datos de entrada a los atributos de la clase de forma segura."""
        self.edad = datos.get('edad', 30)
        self.duracion_ciclo = datos.get('duracion_ciclo')
        self.imc = datos.get('imc')
        self.amh = datos.get('amh')
        self.prolactina = datos.get('prolactina')
        self.tsh = datos.get('tsh')
        self.tpo_ab_positivo = datos.get('tpo_ab_positivo', False)
        self.insulina_ayunas = datos.get('insulina_ayunas')
        self.glicemia_ayunas = datos.get('glicemia_ayunas')
        self.tiene_sop = datos.get('tiene_sop', False)
        self.grado_endometriosis = datos.get('grado_endometriosis', 0)
        self.tiene_miomas = datos.get('tiene_miomas', False)
        self.mioma_submucoso = datos.get('mioma_submucoso', False)
        self.mioma_intramural_significativo = datos.get('mioma_intramural_significativo', False)
        self.mioma_subseroso_grande = datos.get('mioma_subseroso_grande', False)
        self.tipo_adenomiosis = datos.get('tipo_adenomiosis', "")
        self.tipo_polipo = datos.get('tipo_polipo', "")
        self.resultado_hsg = datos.get('resultado_hsg', "")
        self.tiene_otb = datos.get('tiene_otb', False)
        
        self.volumen_seminal = datos.get('volumen_seminal')
        self.concentracion_esperm = datos.get('concentracion_esperm')
        self.motilidad_progresiva = datos.get('motilidad_progresiva')
        self.morfologia_normal = datos.get('morfologia_normal')
        self.vitalidad_esperm = datos.get('vitalidad_esperm')

    def _reset_output_attributes(self):
        """
        ✅ MEJORA: Inicializa CADA atributo para prevenir 'AttributeError'.
        Formateado para máxima legibilidad.
        """
        # Atributos de factores de cálculo
        self.probabilidad_base_edad_num = 0.0
        self.imc_factor = 1.0
        self.ciclo_factor = 1.0
        self.sop_factor = 1.0
        self.endometriosis_factor = 1.0
        self.mioma_factor = 1.0
        self.adenomiosis_factor = 1.0
        self.polipo_factor = 1.0
        self.hsg_factor = 1.0
        self.otb_factor = 1.0  # Lógica de OTB corregida
        self.amh_factor = 1.0
        self.prolactina_factor = 1.0
        self.tsh_factor = 1.0
        self.homa_factor = 1.0
        self.male_factor = 1.0
        
        # Atributos de texto y diagnóstico
        self.diagnostico_potencial_edad = ""
        self.comentario_imc = ""
        self.comentario_ciclo = ""
        self.severidad_sop = "No aplica"
        self.comentario_sop = ""
        self.comentario_endometriosis = ""
        self.comentario_miomas = ""
        self.comentario_adenomiosis = ""
        self.comentario_polipo = ""
        self.comentario_hsg = ""
        self.diagnostico_reserva = "Evaluación no realizada"
        self.recomendacion_reserva = ""
        self.diagnostico_masculino_detallado = "Normal o sin datos"
        self.comentario_prolactina = ""
        self.comentario_tsh = ""
        self.homa_calculado = None
        self.comentario_homa = ""
        
        # Listas y resultados finales
        self.datos_faltantes = []
        self.recomendaciones_lista = []
        self.insights_clinicos = []
        self.pronostico_categoria = ""
        self.pronostico_emoji = ""
        self.pronostico_frase = ""
        self.benchmark_frase = ""
        self.pronostico_numerico = 0.0

    @property
    def probabilidad_ajustada_final(self):
        """Propiedad para mostrar el pronóstico formateado como texto."""
        return f"{self.pronostico_numerico:.1f}%"

    def ejecutar_evaluacion(self):
        """Orquesta la ejecución de todos los métodos de evaluación y cálculo."""
        metodos_evaluacion = [
            self._evaluar_potencial_por_edad, self._evaluar_imc, self._evaluar_ciclo_menstrual,
            self._evaluar_sop, self._evaluar_endometriosis, self._evaluar_miomatosis,
            self._evaluar_adenomiosis, self._evaluar_polipos, self._evaluar_hsg,
            self._evaluar_otb, self._evaluar_amh, self._evaluar_prolactina,
            self._evaluar_tsh, self._evaluar_indice_homa, self._evaluar_factor_masculino
        ]
        for metodo in metodos_evaluacion:
            metodo()
        
        # ✅ CORRECCIÓN: Lógica de cálculo ahora incluye el otb_factor.
        factores = [
            self.imc_factor, self.ciclo_factor, self.sop_factor, self.endometriosis_factor,
            self.mioma_factor, self.adenomiosis_factor, self.polipo_factor, self.hsg_factor,
            self.otb_factor, self.amh_factor, self.prolactina_factor, self.tsh_factor,
            self.homa_factor, self.male_factor
        ]
        producto_factores = np.prod(factores)
        self.pronostico_numerico = self.probabilidad_base_edad_num * producto_factores

        self._generar_textos_pronostico()
        self._generar_comparativa_benchmark()
        self._recopilar_insights_clinicos()

    # --- MÉTODOS DE EVALUACIÓN ---
    # ✅ CORRECCIÓN: Todos los métodos están correctamente indentados dentro de la clase.

    def _evaluar_potencial_por_edad(self):
        if self.edad < 30: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Fertilidad muy buena", 22.5
        elif self.edad <= 34: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Buena fertilidad", 17.5
        elif self.edad <= 37: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Fecundidad en descenso", 12.5
        elif self.edad <= 40: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Reducción significativa", 7.5
        elif self.edad <= 42: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Baja tasa de embarazo", 3.0
        else: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Probabilidad casi nula", 0.1

    def _evaluar_imc(self):
        if self.imc is None: return
        if self.imc < 18.5: self.comentario_imc, self.imc_factor = "Bajo peso", 0.6
        elif self.imc <= 24.9: self.comentario_imc, self.imc_factor = "Peso normal", 1.0
        else: self.comentario_imc, self.imc_factor = "Sobrepeso/Obesidad", 0.85
    
    def _evaluar_ciclo_menstrual(self):
        if self.duracion_ciclo is None: self.datos_faltantes.append("Duración del ciclo menstrual"); return
        if 21 <= self.duracion_ciclo <= 35: self.comentario_ciclo, self.ciclo_factor = "Ciclo regular", 1.0
        else: self.comentario_ciclo, self.ciclo_factor = "Ciclo irregular", 0.6

    def _evaluar_sop(self):
        if not self.tiene_sop: return
        if self.imc is None or self.duracion_ciclo is None: self.severidad_sop, self.sop_factor = "Indeterminada", 0.6; return
        if self.imc < 25 and self.duracion_ciclo <= 45: self.severidad_sop, self.sop_factor = "Leve", 0.85
        elif self.imc <= 30 and self.duracion_ciclo > 45: self.severidad_sop, self.sop_factor = "Moderado", 0.6
        else: self.severidad_sop, self.sop_factor = "Severo", 0.4

    def _evaluar_endometriosis(self):
        if self.grado_endometriosis == 0: return
        self.comentario_endometriosis = f"Grado {self.grado_endometriosis}"
        if self.grado_endometriosis <= 2: self.endometriosis_factor = 0.8
        else: self.endometriosis_factor = 0.4

    def _evaluar_miomatosis(self):
        if not self.tiene_miomas: return
        if self.mioma_submucoso: self.comentario_miomas, self.mioma_factor = "Submucoso", 0.35
        elif self.mioma_intramural_significativo: self.comentario_miomas, self.mioma_factor = "Intramural significativo", 0.6
        elif self.mioma_subseroso_grande: self.comentario_miomas, self.mioma_factor = "Subseroso grande", 0.85
        else: self.comentario_miomas, self.mioma_factor = "Sin impacto cavitario", 1.0

    def _evaluar_adenomiosis(self):
        if not self.tipo_adenomiosis: return
        if self.tipo_adenomiosis == "focal": self.comentario_adenomiosis, self.adenomiosis_factor = "Focal", 0.85
        else: self.comentario_adenomiosis, self.adenomiosis_factor = "Difusa", 0.5

    def _evaluar_polipos(self):
        if not self.tipo_polipo: return
        self.comentario_polipo, self.polipo_factor = "Pólipo(s) endometrial(es)", 0.7

    def _evaluar_hsg(self):
        if not self.resultado_hsg: self.datos_faltantes.append("Resultado de HSG"); return
        if self.resultado_hsg == "normal": self.comentario_hsg, self.hsg_factor = "Ambas trompas permeables", 1.0
        elif self.resultado_hsg == "unilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción unilateral", 0.7
        elif self.resultado_hsg == "bilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción bilateral", 0.0
        elif self.resultado_hsg == "defecto_uterino": self.comentario_hsg, self.hsg_factor = "Alteración cavidad uterina", 0.3

    def _evaluar_otb(self):
        """✅ MEJORA: Lógica de OTB corregida para usar un factor."""
        if self.tiene_otb:
            self.otb_factor = 0.0

    def _evaluar_amh(self):
        if self.amh is None: self.datos_faltantes.append("Hormona Antimülleriana (AMH)"); return
        if self.amh > 4.0: self.diagnostico_reserva, self.amh_factor = "Alta (sugestivo de SOP)", 0.9
        elif self.amh >= 1.5: self.diagnostico_reserva, self.amh_factor = "Adecuada", 1.0
        elif self.amh >= 1.0: self.diagnostico_reserva, self.amh_factor = "Levemente disminuida", 0.85
        elif self.amh >= 0.5: self.diagnostico_reserva, self.amh_factor = "Baja", 0.6
        else: self.diagnostico_reserva, self.amh_factor = "Muy baja", 0.3
    
    def _evaluar_prolactina(self):
        if self.prolactina is None: self.datos_faltantes.append("Nivel de Prolactina"); return
        if self.prolactina >= 25: self.comentario_prolactina, self.prolactina_factor = "Hiperprolactinemia", 0.6
    
    def _evaluar_tsh(self):
        if self.tsh is None: self.datos_faltantes.append("Nivel de TSH"); return
        if self.tsh > 2.5: self.comentario_tsh, self.tsh_factor = "No óptima para fertilidad", 0.7
    
    def _evaluar_indice_homa(self):
        if self.insulina_ayunas is None or self.glicemia_ayunas is None: self.datos_faltantes.append("Índice HOMA"); return
        self.homa_calculado = (self.insulina_ayunas * self.glicemia_ayunas) / 405
        if self.homa_calculado >= 2.5: self.comentario_homa, self.homa_factor = "Resistencia a la insulina", 0.8
    
    def _evaluar_factor_masculino(self):
        if all(p is None for p in [self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm]): self.datos_faltantes.append("Espermatograma completo"); return
        alteraciones = []
        if self.concentracion_esperm == 0: alteraciones.append((0.0, "Azoospermia"))
        else:
            if self.concentracion_esperm is not None and self.concentracion_esperm < 15: alteraciones.append((0.7, "Oligozoospermia"))
            if self.motilidad_progresiva is not None and self.motilidad_progresiva < 32: alteraciones.append((0.85, "Astenozoospermia"))
            if self.morfologia_normal is not None and self.morfologia_normal < 4: alteraciones.append((0.5, "Teratozoospermia"))
            if self.vitalidad_esperm is not None and self.vitalidad_esperm < 58: alteraciones.append((0.3, "Necrozoospermia"))
        if self.volumen_seminal is not None and self.volumen_seminal < 1.5: alteraciones.append((0.85, "Hipospermia"))
        
        if alteraciones:
            self.male_factor = min(alteraciones, key=lambda item: item[0])[0]
            self.diagnostico_masculino_detallado = ", ".join([item[1] for item in alteraciones])
        else:
            self.diagnostico_masculino_detallado = "Parámetros normales"

    def _generar_textos_pronostico(self):
        """Genera los textos principales del pronóstico, con manejo especial para OTB."""
        # ✅ MEJORA: Caso especial para OTB que anula otros pronósticos.
        if self.otb_factor == 0.0:
            self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "NULO POR OTB", "🔴", "El pronóstico de embarazo espontáneo es nulo debido a una ligadura tubárica (OTB) confirmada. Se requiere Fecundación In Vitro (FIV)."
            return
            
        pronostico_str = self.probabilidad_ajustada_final 
        if self.pronostico_numerico >= 15: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "BUENO", "🟢", f"¡Tu pronóstico de concepción espontánea por ciclo es BUENO ({pronostico_str})!"
        elif self.pronostico_numerico >= 5: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "MODERADO", "🟡", f"Tu pronóstico es MODERADO ({pronostico_str}). Hay factores que se pueden optimizar."
        else: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "BAJO", "🔴", f"Tu pronóstico es BAJO ({pronostico_str}). Se recomienda una evaluación por un especialista."

    def _generar_comparativa_benchmark(self):
        if self.otb_factor == 0.0: self.benchmark_frase = "No aplica por OTB."; return
        if self.edad < 30: rango_edad = "Menos de 30"
        elif self.edad <= 34: rango_edad = "30-34"
        elif self.edad <= 37: rango_edad = "35-37"
        elif self.edad <= 40: rango_edad = "38-40"
        else: rango_edad = "Más de 40"
        benchmark_valor = BENCHMARK_PRONOSTICO_POR_EDAD.get(rango_edad, {}).get("mensual", 0.0)
        diferencia = self.pronostico_numerico - benchmark_valor
        if diferencia > 2: comparativa = "notablemente superior al promedio"
        elif diferencia < -2: comparativa = "notablemente inferior al promedio"
        else: comparativa = "similar al promedio"
        self.benchmark_frase = f"Tu resultado es **{comparativa}** para tu grupo de edad ({rango_edad} años), cuyo pronóstico base es del {benchmark_valor:.1f}%."

    def _recopilar_insights_clinicos(self):
        """
        ✅ MEJORA: Usa el método seguro .get() para prevenir errores si una clave no existe.
        Recopila recomendaciones y textos de ayuda basados en los hallazgos.
        """
        # Recomendaciones generales basadas en hallazgos
        if self.imc_factor != 1.0: self.recomendaciones_lista.append(RECOMENDACIONES.get("IMC_ANORMAL", "Optimizar el peso puede mejorar la fertilidad."))
        if self.ciclo_factor != 1.0: self.recomendaciones_lista.append(RECOMENDACIONES.get("CICLO_IRREGULAR", "Estudiar la causa de los ciclos irregulares es importante."))
        if self.tiene_sop: self.recomendaciones_lista.append(RECOMENDACIONES.get("SOP", "El manejo integral del SOP es clave."))
        # ... y así sucesivamente para cada condición ...

        # Insights clínicos para destacar
        if self.tiene_sop: self.insights_clinicos.append(CLINICAL_INSIGHTS.get("SOP", "El SOP es un factor clave en tu perfil."))
        if self.grado_endometriosis > 0: self.insights_clinicos.append(CLINICAL_INSIGHTS.get("ENDOMETRIOSIS", "La endometriosis está afectando tu pronóstico."))
        if self.mioma_submucoso: self.insights_clinicos.append(CLINICAL_INSIGHTS.get("MIOMA_SUBMUCOSO", "El mioma submucoso requiere atención prioritaria."))
        if self.amh is not None and self.amh < 1.0: self.insights_clinicos.append(CLINICAL_INSIGHTS.get("AMH_BAJA", "La reserva ovárica es un factor a considerar."))
        if self.male_factor < 1.0: self.insights_clinicos.append(CLINICAL_INSIGHTS.get("FACTOR_MASCULINO", "El factor masculino juega un rol importante."))