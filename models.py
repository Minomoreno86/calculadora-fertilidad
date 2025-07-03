# Contenido completo para: models.py

import numpy as np

class EvaluacionFertilidad:
    """Define la estructura de datos para una evaluación de fertilidad."""
    def __init__(self, **datos):
        self._asignar_datos_entrada(datos)
        self._reset_output_attributes()

    def _asignar_datos_entrada(self, datos):
        # ✅ CONTENIDO COMPLETO: Este método debe crear todos los atributos de entrada.
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
        # ✅ CONTENIDO COMPLETO: Este método debe crear y resetear todos los atributos de salida.
        self.probabilidad_base_edad_num = 0.0
        self.imc_factor, self.ciclo_factor, self.sop_factor = 1.0, 1.0, 1.0
        self.endometriosis_factor, self.mioma_factor, self.adenomiosis_factor = 1.0, 1.0, 1.0
        self.polipo_factor, self.hsg_factor, self.otb_factor = 1.0, 1.0, 1.0
        self.amh_factor, self.prolactina_factor, self.tsh_factor = 1.0, 1.0, 1.0
        self.homa_factor, self.male_factor = 1.0, 1.0
        self.diagnostico_potencial_edad, self.comentario_imc, self.comentario_ciclo = "", "", ""
        self.severidad_sop, self.comentario_sop, self.comentario_endometriosis = "No aplica", "", ""
        self.comentario_miomas, self.comentario_adenomiosis, self.comentario_polipo = "", "", ""
        self.comentario_hsg, self.diagnostico_reserva = "", "Evaluación no realizada"
        self.diagnostico_masculino_detallado, self.comentario_prolactina = "Normal o sin datos", ""
        self.comentario_tsh, self.homa_calculado, self.comentario_homa = "", None, ""
        self.datos_faltantes, self.recomendaciones_lista, self.insights_clinicos = [], [], []
        self.pronostico_categoria, self.pronostico_emoji, self.pronostico_frase = "", "", ""
        self.benchmark_frase, self.pronostico_numerico = "", 0.0

    @property
    def probabilidad_ajustada_final(self):
        return f"{self.pronostico_numerico:.1f}%"