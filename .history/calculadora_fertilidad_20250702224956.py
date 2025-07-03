import numpy as np
# --- Asumimos que estos archivos existen y son correctos ---
from textos_clinicos import RECOMENDACIONES
from config import BENCHMARK_PRONOSTICO_POR_EDAD, CLINICAL_INSIGHTS

class EvaluacionFertilidad:
    """
    Calcula el pronóstico de fertilidad basado en múltiples factores clínicos.
    Refactorizada para máxima legibilidad (PEP 8) y mantenibilidad.
    """
    def __init__(self, **datos):
        self._asignar_datos_entrada(datos)
        self._reset_output_attributes()

    def _asignar_datos_entrada(self, datos):
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
        # Atributos de factores
        self.imc_factor, self.ciclo_factor, self.sop_factor = 1.0, 1.0, 1.0
        self.endometriosis_factor, self.mioma_factor, self.adenomiosis_factor = 1.0, 1.0, 1.0
        self.polipo_factor, self.hsg_factor = 1.0, 1.0
        self.amh_factor, self.prolactina_factor, self.tsh_factor = 1.0, 1.0, 1.0
        self.homa_factor, self.male_factor = 1.0, 1.0
        # ✅ CORRECCIÓN: Se añade el otb_factor
        self.otb_factor = 1.0
        
        # Atributos de texto y diagnóstico
        self.probabilidad_base_edad_num = 0.0
        self.diagnostico_potencial_edad, self.comentario_imc, self.comentario_ciclo = "", "", ""
        # ... (resto de inicializaciones)
        self.datos_faltantes, self.recomendaciones_lista, self.insights_clinicos = [], [], []
        self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "", "", ""
        self.benchmark_frase, self.pronostico_numerico = "", 0.0


    @property
    def probabilidad_ajustada_final(self):
        return f"{self.pronostico_numerico:.1f}%"

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

        # ✅ CORRECCIÓN: Se añade el otb_factor a la lista de cálculo
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

    # --- ✅ CORRECCIÓN: Todos los métodos que siguen están correctamente indentados ---

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
        if self.duracion_ciclo is None:
            self.datos_faltantes.append("Duración del ciclo menstrual")
            return
        if 21 <= self.duracion_ciclo <= 35:
            self.comentario_ciclo = "Ciclo regular"
            self.ciclo_factor = 1.0
        else:
            self.comentario_ciclo = "Ciclo irregular"
            self.ciclo_factor = 0.6
            self.recomendaciones_lista.append(RECOMENDACIONES.get("CICLO_IRREGULAR", "Ciclo irregular detectado."))

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

    # ✅ CORRECCIÓN: Lógica de OTB refactorizada para usar un factor.
    def _evaluar_otb(self):
        if self.tiene_otb:
            self.otb_factor = 0.0
            self.recomendaciones_lista.append(RECOMENDACIONES.get("OTB", "Ligadura tubárica detectada. Se requiere FIV."))

    def _evaluar_amh(self):
        # ... (el resto de los métodos se mantienen igual, solo asegúrate de que estén indentados) ...
        pass # Placeholder para el resto de tus métodos

    def _evaluar_prolactina(self):
        pass

    def _evaluar_tsh(self):
        pass

    def _evaluar_indice_homa(self):
        pass

    def _evaluar_factor_masculino(self):
        pass
    
    def _generar_textos_pronostico(self):
        # ✅ CORRECCIÓN: Se añade un caso especial para la OTB
        if self.otb_factor == 0.0:
            self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "NULO", "🔴", "El pronóstico de embarazo espontáneo es nulo debido a una ligadura tubárica (OTB) confirmada. Se requiere Fecundación In Vitro (FIV)."
            return

        pronostico_str = self.probabilidad_ajustada_final 
        if self.pronostico_numerico >= 15: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "BUENO", "🟢", f"¡Tu pronóstico de concepción espontánea por ciclo es BUENO ({pronostico_str})! Tienes una probabilidad favorable."
        elif self.pronostico_numerico >= 5: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "MODERADO", "🟡", f"Tu pronóstico es MODERADO ({pronostico_str}). Existen posibilidades, pero hay factores que se pueden optimizar."
        else: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "BAJO", "🔴", f"Tu pronóstico es BAJO ({pronostico_str}). Se recomienda encarecidamente una evaluación por un especialista."

    def _generar_comparativa_benchmark(self):
        if self.otb_factor == 0.0:
            self.benchmark_frase = "No aplica por OTB."
            return
        # ... (resto de la lógica sin cambios)
        pass

    def _recopilar_insights_clinicos(self):
        # ... (resto de la lógica sin cambios)
        pass


if __name__ == '__main__':
    print("--- Módulo de Prueba para EvaluacionFertilidad (Versión Corregida) ---")
    
    # Prueba 1: Caso sin OTB
    print("\n--- PRUEBA 1: PACIENTE CON CICLO IRREGULAR ---")
    datos_prueba_1 = {"edad": 36, "amh": 1.2, "duracion_ciclo": 45}
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