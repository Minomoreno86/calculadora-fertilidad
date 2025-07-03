# Contenido completo para: calculadora_fertilidad.py

import numpy as np
# Aunque las funciones de lógica usan estos, es buena práctica mantenerlos
# aquí si la clase principal necesita alguna referencia en el futuro.
from textos_clinicos import RECOMENDACIONES
from config import BENCHMARK_PRONOSTICO_POR_EDAD, CLINICAL_INSIGHTS

# ✅ IMPORTACIÓN CENTRALIZADA: Traemos todo desde nuestro nuevo paquete 'logic'.
from logic import (
    evaluar_potencial_por_edad, evaluar_imc, evaluar_ciclo_menstrual,
    evaluar_sop, evaluar_endometriosis, evaluar_miomatosis,
    evaluar_adenomiosis, evaluar_polipos, evaluar_hsg,
    evaluar_otb, evaluar_amh, evaluar_prolactina,
    evaluar_tsh, evaluar_indice_homa, evaluar_factor_masculino,
    generar_textos_pronostico, generar_comparativa_benchmark,
    recopilar_insights_clinicos
)

class EvaluacionFertilidad:
    """
    Orquestador del cálculo de fertilidad. Almacena los datos y resultados,
    y llama a las funciones de lógica externas para realizar los cálculos.
    """
    def __init__(self, **datos):
        self._asignar_datos_entrada(datos)
        self._reset_output_attributes()

    def _asignar_datos_entrada(self, datos):
        # Este método se queda como estaba, su responsabilidad es asignar datos.
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
        # Este método también se queda, es responsable del estado inicial.
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

    def ejecutar_evaluacion(self):
        """
        Orquestador que llama a las funciones de lógica externas.
        """
        funciones_de_evaluacion = [
            evaluar_potencial_por_edad, evaluar_imc, evaluar_ciclo_menstrual,
            evaluar_sop, evaluar_endometriosis, evaluar_miomatosis,
            evaluar_adenomiosis, evaluar_polipos, evaluar_hsg,
            evaluar_otb, evaluar_amh, evaluar_prolactina,
            evaluar_tsh, evaluar_indice_homa, evaluar_factor_masculino
        ]

        # ✅ ORQUESTADOR: Llama a las funciones externas pasándoles 'self'.
        for funcion in funciones_de_evaluacion:
            funcion(self)
        
        factores = [
            self.imc_factor, self.ciclo_factor, self.sop_factor, self.endometriosis_factor,
            self.mioma_factor, self.adenomiosis_factor, self.polipo_factor, self.hsg_factor,
            self.otb_factor, self.amh_factor, self.prolactina_factor, self.tsh_factor,
            self.homa_factor, self.male_factor
        ]
        
        self.pronostico_numerico = self.probabilidad_base_edad_num * np.prod(factores)

        # Llamamos a las funciones de generación de informe
        generar_textos_pronostico(self)
        generar_comparativa_benchmark(self)
        recopilar_insights_clinicos(self)