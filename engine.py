import numpy as np

# Importa la ESTRUCTURA de datos desde models
from models import EvaluacionFertilidad 

# Importa toda la LÓGICA desde el paquete 'logic'
from logic import (
    evaluar_potencial_por_edad, evaluar_imc, evaluar_ciclo_menstrual,
    evaluar_sop, evaluar_endometriosis, evaluar_miomatosis,
    evaluar_adenomiosis, evaluar_polipos, evaluar_hsg,
    evaluar_otb, evaluar_amh, evaluar_prolactina,
    evaluar_tsh, evaluar_indice_homa, evaluar_factor_masculino,
    generar_textos_pronostico, generar_comparativa_benchmark,
    recopilar_insights_clinicos
)

def ejecutar_evaluacion_completa(evaluacion: EvaluacionFertilidad):
    """
    Motor de cálculo. Recibe un objeto EvaluacionFertilidad,
    ejecuta todas las reglas de lógica y lo modifica con los resultados.
    """
    # 1. Lista de todas las funciones que calculan los factores
    funciones_de_evaluacion = [
        evaluar_potencial_por_edad, evaluar_imc, evaluar_ciclo_menstrual,
        evaluar_sop, evaluar_endometriosis, evaluar_miomatosis,
        evaluar_adenomiosis, evaluar_polipos, evaluar_hsg,
        evaluar_otb, evaluar_amh, evaluar_prolactina,
        evaluar_tsh, evaluar_indice_homa, evaluar_factor_masculino
    ]

    # Ejecuta cada función de evaluación, pasándole el objeto para que lo modifique
    for funcion in funciones_de_evaluacion:
        funcion(evaluacion)
    
    # 2. Recopila todos los factores calculados
    factores = [
        evaluacion.imc_factor, evaluacion.ciclo_factor, evaluacion.sop_factor, 
        evaluacion.endometriosis_factor, evaluacion.mioma_factor, evaluacion.adenomiosis_factor, 
        evaluacion.polipo_factor, evaluacion.hsg_factor, evaluacion.otb_factor, 
        evaluacion.amh_factor, evaluacion.prolactina_factor, evaluacion.tsh_factor,
        evaluacion.homa_factor, evaluacion.male_factor
    ]
    
    # 3. Realiza el cálculo del pronóstico final
    evaluacion.pronostico_numerico = evaluacion.probabilidad_base_edad_num * np.prod(factores)

    # 4. Llama a las funciones que generan los textos del informe
    generar_textos_pronostico(evaluacion)
    generar_comparativa_benchmark(evaluacion)
    recopilar_insights_clinicos(evaluacion)