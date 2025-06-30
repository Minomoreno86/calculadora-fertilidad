# db_manager.py
import sqlite3
from datetime import datetime
import pandas as pd # <-- ¡NUEVA IMPORTACIÓN!

# ... (crear_conexion y crear_tabla sin cambios) ...

def insertar_registro(conn, registro_data):
    # ... (sin cambios)
    pass

# --- AÑADIMOS LA NUEVA FUNCIÓN DE LECTURA ---
def leer_todos_los_registros(conn):
    """
    Lee todos los registros de la base de datos y los devuelve como un DataFrame de Pandas.
    """
    try:
        # La consulta SQL para seleccionar todo de la tabla 'registros'
        df = pd.read_sql_query("SELECT * FROM registros", conn)
        return df
    except Exception as e:
        print(f"Error al leer los registros: {e}")
        return pd.DataFrame() # Devuelve un DataFrame vacío en caso de error

# ... (main y if __name__ sin cambios) ...