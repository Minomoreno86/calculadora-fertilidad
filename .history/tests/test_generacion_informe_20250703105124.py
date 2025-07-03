# Contenido actualizado para: tests/test_generacion_informe.py

import pytest
from models import EvaluacionFertilidad
from logic.generacion_informe import generar_textos_pronostico

# El decorador @pytest.mark.parametrize ejecuta la prueba de abajo
# una vez por cada tupla en la lista.
@pytest.mark.parametrize("pronostico_inicial, categoria_esperada, emoji_esperado", [
    (20.0, "BUENO", "🟢"),      # Caso 1: Pronóstico Bueno
    (15.0, "BUENO", "🟢"),      # Caso 2: Límite superior de Moderado
    (8.5, "MODERADO", "🟡"),     # Caso 3: Pronóstico Moderado
    (5.0, "MODERADO", "🟡"),     # Caso 4: Límite superior de Bajo
    (4.9, "BAJO", "🔴"),        # Caso 5: Pronóstico Bajo
    (0.0, "BAJO", "🔴")         # Caso 6: Pronóstico Cero
])
def test_generacion_textos_pronostico(pronostico_inicial, categoria_esperada, emoji_esperado):
    """
    Prueba parametrizada que verifica la categoría y el emoji para
    múltiples valores de pronóstico.
    """
    # Esta es nuestra "plantilla" de prueba
    evaluacion = EvaluacionFertilidad()
    evaluacion.pronostico_numerico = pronostico_inicial
    
    generar_textos_pronostico(evaluacion)
    
    assert evaluacion.pronostico_categoria == categoria_esperada
    assert evaluacion.pronostico_emoji == emoji_esperado

# Aún mantenemos la prueba del caso OTB por separado, ya que es una lógica diferente
def test_generar_texto_caso_otb():
    eval_otb = EvaluacionFertilidad()
    eval_otb.otb_factor = 0.0 # Simulamos que tiene OTB
    generar_textos_pronostico(eval_otb)
    assert eval_otb.pronostico_categoria == "REQUIERE TRATAMIENTO"