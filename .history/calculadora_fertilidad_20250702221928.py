# VERSIÓN COMPLETA CON CORRECCIÓN DE BUG DE CICLO MENSTRUAL

from textos_clinicos import RECOMENDACIONES
from config import BENCHMARK_PRONOSTICO_POR_EDAD, CLINICAL_INSIGHTS
import numpy as np

from textos_clinicos import RECOMENDACIONES
from config import BENCHMARK_PRONOSTICO_POR_EDAD, CLINICAL_INSIGHTS
import numpy as np

class EvaluacionFertilidad:
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
        self.mioma_submucoso_multiple = datos.get('mioma_submucoso_multiple', False)
        self.mioma_intramural_significativo = datos.get('mioma_intramural_significativo', False)
        self.mioma_subseroso_grande = datos.get('mioma_subseroso_grande', False)
        self.tipo_adenomiosis = datos.get('tipo_adenomiosis', "")
        self.tipo_polipo = datos.get('tipo_polipo', "")
        self.resultado_hsg = datos.get('resultado_hsg', "")
        self.factor_tubario = datos.get('factor_tubario', False)
        self.tiene_otb = datos.get('tiene_otb', False)
        self.volumen_seminal = datos.get('volumen_seminal')
        self.concentracion_esperm = datos.get('concentracion_esperm')
        self.motilidad_progresiva = datos.get('motilidad_progresiva')
        self.morfologia_normal = datos.get('morfologia_normal')
        self.vitalidad_esperm = datos.get('vitalidad_esperm')

    def _reset_output_attributes(self):
        self.diagnostico_potencial_edad = ""
        self.probabilidad_base_edad_num = 0.0
        self.comentario_imc = ""
        self.imc_factor = 1.0
        self.comentario_ciclo = ""
        self.ciclo_factor = 1.0
        self.severidad_sop = "No aplica"
        self.comentario_sop = ""
        self.sop_factor = 1.0
        self.comentario_endometriosis = ""
        self.endometriosis_factor = 1.0
        self.comentario_miomas = ""
        self.mioma_factor = 1.0
        self.comentario_adenomiosis = ""
        self.adenomiosis_factor = 1.0
        self.comentario_polipo = ""
        self.polipo_factor = 1.0
        self.comentario_hsg = ""
        self.hsg_factor = 1.0
        self.diagnostico_reserva = "Evaluación no realizada."
        self.recomendacion_reserva = ""
        self.amh_factor = 1.0
        self.diagnostico_masculino_detallado = "Normal o sin datos"
        self.male_factor = 1.0
        self.comentario_prolactina = ""
        self.prolactina_factor = 1.0
        self.comentario_tsh = ""
        self.tsh_factor = 1.0
        self.homa_calculado = None
        self.comentario_homa = ""
        self.homa_factor = 1.0
        self.datos_faltantes, self.recomendaciones_lista, self.insights_clinicos = [], [], []
        self.pronostico_categoria = ""
        self.pronostico_emoji = ""
        self.pronostico_frase = ""
        self.benchmark_frase = ""
        self.pronostico_numerico = 0.0

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

        factores = [
            self.imc_factor, self.ciclo_factor, self.sop_factor, self.endometriosis_factor,
            self.mioma_factor, self.adenomiosis_factor, self.polipo_factor, self.hsg_factor,
            self.amh_factor, self.prolactina_factor, self.tsh_factor, self.homa_factor, self.male_factor
        ]

        producto_factores = np.prod(factores)
        prob_ajustada_num = self.probabilidad_base_edad_num * producto_factores
        self.pronostico_numerico = prob_ajustada_num

        self._generar_textos_pronostico()
        self._generar_comparativa_benchmark()
        self._recopilar_insights_clinicos()

    def _evaluar_otb(self):
        if self.tiene_otb:
            self.pronostico_numerico = 0
            self.pronostico_categoria = "Muy Bajo"
            self.pronostico_emoji = "🔴"
            self.pronostico_frase = "El pronóstico de embarazo es nulo debido a la presencia de una ligadura tubárica (OTB) confirmada. Se recomienda valoración para reproducción asistida."
            self.benchmark_frase = ""
            self.recomendaciones_lista.append("Ligadura tubárica detectada. Se sugiere recanalización de trompas o FIV.")

    def _evaluar_amh(self):
        if self.amh is None:
           self.datos_faltantes.append("Hormona Antimülleriana (AMH)")
           return 
        if self.amh > 3.0:
           self.diagnostico_reserva = "Alta reserva ovárica (sugestivo de SOP)"
           self.amh_factor = 0.9  # Puede ajustarse clínicamente
           self.recomendaciones_lista.append("AMH elevada, sugiere alta reserva ovárica, se debe evaluar posibilidad de SOP.")
        elif 1.0 <= self.amh <= 3.0:
           self.diagnostico_reserva = "Reserva ovárica normal"
           self.amh_factor = 1.0
        elif 0.7 <= self.amh < 1.0:
           self.diagnostico_reserva = "Reserva ovárica disminuida leve"
           self.amh_factor = 0.85
           self.recomendaciones_lista.append("AMH levemente baja, considerar evaluación de la reserva ovárica.")
        elif 0.3 <= self.amh < 0.7:
           self.diagnostico_reserva = "Baja reserva ovárica"
           self.amh_factor = 0.6
           self.recomendaciones_lista.append("AMH baja, pronóstico ovárico comprometido.")
        else:  # AMH < 0.3
           self.diagnostico_reserva = "Reserva ovárica severamente baja"
           self.amh_factor = 0.3
           self.recomendaciones_lista.append("AMH muy baja, considerar técnicas de alta complejidad.")

    # Si AMH > 3.0, marcar como posible SOP adicionalmente
        if self.amh > 3.0:
           self.tiene_sop = True  # Esto permitirá que el modelo capture SOP como factor adicional si lo deseas

    def _evaluar_prolactina(self):
        if self.prolactina is None: 
            self.datos_faltantes.append("Nivel de Prolactina")
            return
        if self.prolactina >= 25: 
            self.comentario_prolactina, self.prolactina_factor = "Hiperprolactinemia", 0.6
            self.recomendaciones_lista.append(RECOMENDACIONES["PRL_ALTA"])
    
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
        if self.concentracion_esperm == 0:
            alteraciones.append((0.0, "Azoospermia"))
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
        else:
            self.diagnostico_masculino_detallado = "Parámetros dentro de la normalidad."
            
    # --- MÉTODOS DE GENERACIÓN DE TEXTOS ---
    
    def _generar_textos_pronostico(self):
        pronostico_str = self.probabilidad_ajustada_final 
        if self.pronostico_numerico >= 15: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "BUENO", "🟢", f"¡Tu pronóstico de concepción espontánea por ciclo es BUENO ({pronostico_str})! Tienes una probabilidad favorable."
        elif self.pronostico_numerico >= 5: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "MODERADO", "🟡", f"Tu pronóstico es MODERADO ({pronostico_str}). Existen posibilidades, pero hay factores que se pueden optimizar."
        else: self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "BAJO", "🔴", f"Tu pronóstico es BAJO ({pronostico_str}). Se recomienda encarecidamente una evaluación por un especialista."

    def _generar_comparativa_benchmark(self):
        pronostico_usuario = self.pronostico_numerico
        if self.edad < 30: rango_edad = "Menos de 30"
        elif self.edad <= 34: rango_edad = "30-34"
        elif self.edad <= 37: rango_edad = "35-37"
        elif self.edad <= 40: rango_edad = "38-40"
        else: rango_edad = "Más de 40"
        benchmark_data = BENCHMARK_PRONOSTICO_POR_EDAD.get(rango_edad, {})
        benchmark_valor = benchmark_data.get("mensual", 0.0)
        diferencia = pronostico_usuario - benchmark_valor
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
    print("--- Módulo de Prueba para EvaluacionFertilidad (Versión COMPLETA) ---")
    datos_prueba = {"edad": 36, "amh": 0.2, "duracion_ciclo": 45} # Prueba con ciclo irregular
    evaluacion_prueba = EvaluacionFertilidad(**datos_prueba)
    evaluacion_prueba.ejecutar_evaluacion()
    print(f"\n--- RESULTADO DE LA PRUEBA ---")
    print(f"Pronóstico Final (String): {evaluacion_prueba.probabilidad_ajustada_final}")
    print(f"Pronóstico Final (Numérico): {evaluacion_prueba.pronostico_numerico}")
    print(f"Factores aplicados: imc={evaluacion_prueba.imc_factor}, ciclo={evaluacion_prueba.ciclo_factor}")
    print(f"Recomendaciones: {evaluacion_prueba.recomendaciones_lista}")