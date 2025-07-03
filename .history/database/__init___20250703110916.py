# En: database/__init__.py

from .connection import crear_conexion_y_tablas
from .perfiles_crud import (
    preparar_registro_db,
    insertar_registro,
    leer_todos_los_registros,
    eliminar_registro_por_id,
    eliminar_todos_los_registros
)
from .riesgos_crud import insertar_riesgo_aborto, leer_todos_los_riesgos
from .logros_crud import inicializar_logros, desbloquear_logro, obtener_logros