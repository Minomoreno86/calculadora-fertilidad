# En tests/test_evaluacion_factores.py
from models import EvaluacionFertilidad

def evaluar_imc(evaluacion):
    """Verifica la asignación de factores de IMC usando una fixture."""
    
    # Ya no necesitamos crear el objeto, pytest nos lo da.
    evaluacion.imc = 17.0
    evaluar_imc(evaluacion)
    assert evaluacion.imc_factor == 0.6
    
    # Podemos reutilizar el mismo objeto para los otros casos
    evaluacion.imc = 22.0
    evaluar_imc(evaluacion)
    assert evaluacion.imc_factor == 1.0