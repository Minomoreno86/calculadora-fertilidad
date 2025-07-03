# Contenido completo para: logic/__init__.py

# Importa todas las funciones del módulo de evaluación de factores
from .evaluacion_factores import (
    evaluar_potencial_por_edad, 
    evaluar_imc, 
    evaluar_ciclo_menstrual,
    evaluar_sop, 
    evaluar_endometriosis, 
    evaluar_miomatosis,
    evaluar_adenomiosis, 
    evaluar_polipos, 
    evaluar_hsg,
    evaluar_otb, 
    evaluar_amh, 
    evaluar_prolactina,
    evaluar_tsh, 
    evaluar_indice_homa, 
    evaluar_factor_masculino
)

# Importa todas las funciones del módulo de generación de informes
from .generacion_informe import (
    generar_textos_pronostico, 
    generar_comparativa_benchmark,
    recopilar_insights_clinicos
)