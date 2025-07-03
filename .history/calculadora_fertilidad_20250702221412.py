# VERSIÓN COMPLETA CON CORRECCIÓN DE BUG DE CICLO MENSTRUAL

from textos_clinicos import RECOMENDACIONES
from config import BENCHMARK_PRONOSTICO_POR_EDAD, CLINICAL_INSIGHTS
import numpy as np

RECOMENDACIONES = {
    "EDAD_35": "A partir de los 35, se recomienda no demorar la consulta especializada.", "EDAD_38": "A partir de los 38, el tiempo es un factor crítico.", "EDAD_40": "Con 40 años o más, el tratamiento debe ser prioritario.", "EDAD_43": "A esta edad, las opciones con óvulos propios son muy limitadas.", "IMC_BAJO": "Un IMC bajo puede afectar la ovulación.", "IMC_ALTO": "El sobrepeso puede afectar la calidad ovocitaria.", "CICLO_IRREGULAR": "Los ciclos irregulares pueden indicar problemas de ovulación.", "SOP": "El SOP requiere un manejo integral.", "ENDO_LEVE": "La endometriosis leve puede generar inflamación.", "ENDO_SEVERA": "La endometriosis severa afecta la anatomía.", "MIOMA_SUBMUCOSO": "Los miomas submucosos deben ser extraídos.", "MIOMA_INTRAMURAL": "Miomas intramurales grandes pueden afectar la implantación.", "ADENO_FOCAL": "La adenomiosis focal puede tratarse.", "ADENO_DIFUSA": "La adenomiosis difusa es un reto para la implantación.", "POLIPO": "Los pólipos endometriales deben ser extraídos.", "HSG_UNILATERAL": "La obstrucción unilateral reduce la probabilidad.", "HSG_BILATERAL": "La obstrucción bilateral impide el embarazo espontáneo. La FIV es la solución.", "HSG_DEFECTO": "Un defecto en la cavidad uterina debe ser corregido.", "PRL_ALTA": "La prolactina alta inhibe la ovulación.", "TSH_ALTA": "Una TSH > 2.5 se asocia a problemas de fertilidad.", "TPO_POSITIVO": "Los anticuerpos anti-TPO aumentan el riesgo de fallo de implantación.", "HOMA_ALTO": "La resistencia a la insulina afecta la calidad de los óvulos.", "FACTOR_MASCULINO": "Las alteraciones en el seminograma requieren evaluación por andrología.", "OTB": "La ligadura tubárica impide la concepción natural. Se requiere FIV."
}
BENCHMARK_PRONOSTICO_POR_EDAD = {
    "Menos de 30": {"mensual": 22.5}, "30-34": {"mensual": 17.5}, "35-37": {"mensual": 12.5}, "38-40": {"mensual": 7.5}, "Más de 40": {"mensual": 3.0}
}
CLINICAL_INSIGHTS = {
    "SOP": "El manejo del SOP es clave para mejorar tus resultados.", "ENDOMETRIOSIS": "La endometriosis es un factor inflamatorio importante.", "MIOMA_SUBMUCOSO": "La corrección del mioma submucoso es prioritaria.", "AMH_BAJA": "La baja reserva ovárica sugiere que el tiempo es un factor crucial.", "FACTOR_MASCULINO": "Optimizar el factor masculino puede mejorar el pronóstico."
}
# --- Fin de los datos de ejemplo ---

class EvaluacionFertilidad:
    """
    Calcula el pronóstico de fertilidad basado en múltiples factores clínicos.
    Refactorizada para máxima legibilidad (PEP 8) y mantenibilidad.
    """
    def __init__(self, **datos):
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
        """Inicializa todos los atributos de resultados a sus valores por defecto."""
        # ✅ BUENA PRÁCTICA: Formateado para legibilidad (PEP 8)
        self.probabilidad_base_edad_num = 0.0
        self.imc_factor, self.ciclo_factor, self.sop_factor = 1.0, 1.0, 1.0
        self.endometriosis_factor, self.mioma_factor, self.adenomiosis_factor = 1.0, 1.0, 1.0
        self.polipo_factor, self.hsg_factor, self.otb_factor = 1.0, 1.0, 1.0 # 🔥 Añadido otb_factor
        self.amh_factor, self.prolactina_factor, self.tsh_factor = 1.0, 1.0, 1.0
        self.homa_factor, self.male_factor = 1.0, 1.0
        
        self.diagnostico_potencial_edad, self.comentario_imc, self.comentario_ciclo = "", "", ""
        self.severidad_sop, self.comentario_sop, self.comentario_endometriosis = "No aplica", "", ""
        self.comentario_miomas, self.comentario_adenomiosis, self.comentario_polipo = "", "", ""
        self.comentario_hsg, self.diagnostico_reserva, self.recomendacion_reserva = "", "Evaluación no realizada.", ""
        self.diagnostico_masculino_detallado, self.comentario_prolactina = "Normal o sin datos", ""
        self.comentario_tsh, self.homa_calculado, self.comentario_homa = "", None, ""
        
        self.datos_faltantes, self.recomendaciones_lista, self.insights_clinicos = [], [], []
        self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "", "", ""
        self.benchmark_frase, self.pronostico_numerico = "", 0.0

    @property
    def probabilidad_ajustada_final(self):
        return f"{self.pronostico_numerico:.1f}%"

    # ✅ CORRECCIÓN: Todos los métodos indentados correctamente dentro de la clase.
    def ejecutar_evaluacion(self):
        metodos_evaluacion = [
            self._evaluar_potencial_por_edad, self._evaluar_imc, self._evaluar_ciclo_menstrual,
            self._evaluar_sop, self._evaluar_endometriosis, self._evaluar_miomatosis,
            self._evaluar_adenomiosis, self._evaluar_polipos, self._evaluar_hsg,
            self._evaluar_otb, self._evaluar_amh, self._evaluar_prolactina,
            self._evaluar_tsh, self._evaluar_indice_homa, self._evaluar_factor_masculino
        ]
        for metodo in metodos_evaluacion:
            metodo()
        
        # ✅ CORRECCIÓN: otb_factor incluido en el cálculo para anularlo si es necesario.
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

    def _evaluar_potencial_por_edad(self):
        if self.edad < 30: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Fertilidad muy buena", 22.5
        elif self.edad <= 34: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Buena fertilidad", 17.5
        elif self.edad <= 37: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Fecundidad en descenso", 12.5; self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_35"])
        elif self.edad <= 40: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Reducción significativa", 7.5; self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_38"])
        elif self.edad <= 42: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Baja tasa de embarazo", 3.0; self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_40"])
        else: self.diagnostico_potencial_edad, self.probabilidad_base_edad_num = "Probabilidad nula o anecdótica", 0.0; self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_43"])

    def _evaluar_imc(self):
        if self.imc is None: return
        if self.imc < 18.5: self.comentario_imc, self.imc_factor = "Bajo peso", 0.6; self.recomendaciones_lista.append(RECOMENDACIONES["IMC_BAJO"])
        elif self.imc <= 24.9: self.comentario_imc, self.imc_factor = "Peso normal", 1.0
        else: self.comentario_imc, self.imc_factor = "Sobrepeso/Obesidad", 0.85; self.recomendaciones_lista.append(RECOMENDACIONES["IMC_ALTO"])
    
    def _evaluar_ciclo_menstrual(self):
        if self.duracion_ciclo is None: self.datos_faltantes.append("Duración del ciclo menstrual"); return
        if 21 <= self.duracion_ciclo <= 35: self.comentario_ciclo, self.ciclo_factor = "Ciclo regular", 1.0
        else: self.comentario_ciclo, self.ciclo_factor = "Ciclo irregular", 0.6; self.recomendaciones_lista.append(RECOMENDACIONES["CICLO_IRREGULAR"])

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
        elif self.mioma_subseroso_grande: self.comentario_miomas, self.mioma_factor = "Miomatosis subserosa grande", 0.85
        else: self.comentario_miomas, self.mioma_factor = "Miomatosis sin impacto cavitario", 1.0

    def _evaluar_adenomiosis(self):
        if not self.tipo_adenomiosis: return
        if self.tipo_adenomiosis == "focal": self.comentario_adenomiosis, self.adenomiosis_factor = "Adenomiosis Focal", 0.85; self.recomendaciones_lista.append(RECOMENDACIONES["ADENO_FOCAL"])
        else: self.comentario_adenomiosis, self.adenomiosis_factor = "Adenomiosis Difusa", 0.5; self.recomendaciones_lista.append(RECOMENDACIONES["ADENO_DIFUSA"])

    def _evaluar_polipos(self):
        if not self.tipo_polipo: return
        self.comentario_polipo, self.polipo_factor = "Pólipo(s) endometrial(es)", 0.7; self.recomendaciones_lista.append(RECOMENDACIONES["POLIPO"])

    def _evaluar_hsg(self):
        if not self.resultado_hsg: self.datos_faltantes.append("Resultado de HSG"); return
        if self.resultado_hsg == "normal": self.comentario_hsg, self.hsg_factor = "Ambas trompas permeables", 1.0
        elif self.resultado_hsg == "unilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción tubárica unilateral", 0.7; self.recomendaciones_lista.append(RECOMENDACIONES["HSG_UNILATERAL"])
        elif self.resultado_hsg == "bilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción tubárica bilateral", 0.0; self.recomendaciones_lista.append(RECOMENDACIONES["HSG_BILATERAL"])
        elif self.resultado_hsg == "defecto_uterino": self.comentario_hsg, self.hsg_factor = "Alteración de cavidad uterina", 0.3; self.recomendaciones_lista.append(RECOMENDACIONES["HSG_DEFECTO"])

    # 🔥 MÉTODO REFACTORIZADO PARA USAR UN FACTOR
    def _evaluar_otb(self):
        if self.tiene_otb:
            self.otb_factor = 0.0
            self.recomendaciones_lista.append(RECOMENDACIONES["OTB"])
            
    def _evaluar_amh(self):
        if self.amh is None: self.datos_faltantes.append("Hormona Antimülleriana (AMH)"); return
        
        # ✅ CORRECCIÓN: Lógica integrada para evitar errores si AMH es None.
        if self.amh > 3.0:
            self.diagnostico_reserva = "Alta reserva ovárica (sugestivo de SOP)"
            self.amh_factor = 0.9
            self.recomendaciones_lista.append("AMH elevada, sugiere alta reserva ovárica, se debe evaluar posibilidad de SOP.")
            if not self.tiene_sop: self.tiene_sop = True
        elif 1.0 <= self.amh <= 3.0: self.diagnostico_reserva, self.amh_factor = "Reserva ovárica normal", 1.0
        elif 0.7 <= self.amh < 1.0: self.diagnostico_reserva, self.amh_factor = "Reserva ovárica disminuida leve", 0.85; self.recomendaciones_lista.append("AMH levemente baja, considerar evaluación de la reserva ovárica.")
        elif 0.3 <= self.amh < 0.7: self.diagnostico_reserva, self.amh_factor = "Baja reserva ovárica", 0.6; self.recomendaciones_lista.append("AMH baja, pronóstico ovárico comprometido.")
        else: self.diagnostico_reserva, self.amh_factor = "Reserva ovárica severamente baja", 0.3; self.recomendaciones_lista.append("AMH muy baja, considerar técnicas de alta complejidad.")

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
            self.recomendaciones_lista.append(RECOMENDACIONES["FACTOR_MASCULINO"])
        else: self.diagnostico_masculino_detallado = "Parámetros dentro de la normalidad."
            
    def _generar_textos_pronostico(self):
        if self.otb_factor == 0.0:
            self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "NULO", "🔴", "El pronóstico de embarazo espontáneo es nulo debido a una ligadura tubárica (OTB) confirmada. Se requiere Fecundación In Vitro (FIV)."
            return
            
        pronostico_str = self.probabilidad_ajustada_final 
        if self.pronostico_numerico >= 15: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "BUENO", "🟢", f"¡Tu pronóstico de concepción espontánea por ciclo es BUENO ({pronostico_str})! Tienes una probabilidad favorable."
        elif self.pronostico_numerico >= 5: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "MODERADO", "🟡", f"Tu pronóstico es MODERADO ({pronostico_str}). Existen posibilidades, pero hay factores que se pueden optimizar."
        else: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "BAJO", "🔴", f"Tu pronóstico es BAJO ({pronostico_str}). Se recomienda encarecidamente una evaluación por un especialista."

    def _generar_comparativa_benchmark(self):
        if self.otb_factor == 0.0: self.benchmark_frase = ""; return
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
        if self.tiene_sop: self.insights_clinicos.append(CLINICAL_INSIGHTS["SOP"])
        if self.grado_endometriosis > 0: self.insights_clinicos.append(CLINICAL_INSIGHTS["ENDOMETRIOSIS"])
        if self.mioma_submucoso: self.insights_clinicos.append(CLINICAL_INSIGHTS["MIOMA_SUBMUCOSO"])
        if self.amh is not None and self.amh < 1.0: self.insights_clinicos.append(CLINICAL_INSIGHTS["AMH_BAJA"])
        if self.male_factor < 1.0: self.insights_clinicos.append(CLINICAL_INSIGHTS["FACTOR_MASCULINO"])
        
if __name__ == '__main__':
    print("--- Módulo de Prueba para EvaluacionFertilidad (Versión Corregida y Refactorizada) ---")
    
    # Prueba 1: Caso sin OTB
    print("\n--- PRUEBA 1: PACIENTE SIN OTB ---")
    datos_prueba_1 = {"edad": 36, "amh": 0.2, "duracion_ciclo": 45}
    evaluacion_1 = EvaluacionFertilidad(**datos_prueba_1)
    evaluacion_1.ejecutar_evaluacion()
    print(evaluacion_1.pronostico_frase)
    print(f"Pronóstico Numérico: {evaluacion_1.probabilidad_ajustada_final}")
    
    # Prueba 2: Caso con OTB
    print("\n--- PRUEBA 2: PACIENTE CON OTB ---")
    datos_prueba_2 = {"edad": 32, "amh": 2.5, "duracion_ciclo": 28, "tiene_otb": True}
    evaluacion_2 = EvaluacionFertilidad(**datos_prueba_2)
    evaluacion_2.ejecutar_evaluacion()
    print(evaluacion_2.pronostico_frase)
    print(f"Pronóstico Numérico: {evaluacion_2.probabilidad_ajustada_final}")
    print(f"Factor OTB aplicado: {evaluacion_2.otb_factor}")
