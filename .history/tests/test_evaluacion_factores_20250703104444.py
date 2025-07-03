# Contenido para: tests/test_evaluacion_factores.py

# 1. Importamos las herramientas necesarias
import pytest
from models import EvaluacionFertilidad
from logic.evaluacion_factores import evaluar_imc

# 2. Creamos una función de prueba (el nombre DEBE empezar con 'test_')
def test_evaluar_imc():
    """
    Verifica que la función evaluar_imc asigne los factores correctos
    para diferentes valores de IMC.
    """
    # Caso de Prueba 1: Bajo Peso
    datos_bajo_peso = {'imc': 17.0}
    evaluacion_1 = EvaluacionFertilidad(**datos_bajo_peso)
    evaluar_imc(evaluacion_1)
    # 'assert' es la palabra clave que comprueba si algo es verdad.
    # Si no lo es, la prueba falla.
    assert evaluacion_1.imc_factor == 0.6
    assert evaluacion_1.comentario_imc == "Bajo peso"

    # Caso de Prueba 2: Peso Normal
    datos_peso_normal = {'imc': 22.0}
    evaluacion_2 = EvaluacionFertilidad(**datos_peso_normal)
    evaluar_imc(evaluacion_2)
    assert evaluacion_2.imc_factor == 1.0
    assert evaluacion_2.comentario_imc == "Peso normal"

    # Caso de Prueba 3: Sobrepeso
    datos_sobrepeso = {'imc': 28.0}
    evaluacion_3 = EvaluacionFertilidad(**datos_sobrepeso)
    evaluar_imc(evaluacion_3)
    assert evaluacion_3.imc_factor == 0.85
    assert evaluacion_3.comentario_imc == "Sobrepeso/Obesidad"
    