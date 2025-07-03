# Contenido para: tests/conftest.py

import pytest
from models import EvaluacionFertilidad

@pytest.fixture
def evaluacion_base():
    """
    Una fixture que devuelve un objeto EvaluacionFertilidad limpio y básico
    para ser usado en las pruebas.
    """
    datos_iniciales = {}
    evaluacion = EvaluacionFertilidad(**datos_iniciales)
    return evaluacion