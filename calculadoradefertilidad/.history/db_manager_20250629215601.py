# db_manager.py
import sqlite3
from datetime import datetime

def crear_conexion(db_file):
    """Crea una conexión a la base de datos SQLite."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def crear_tabla(conn):
    """Crea la tabla para almacenar los registros de fertilidad."""
    
    # Este es el "esquema" de nuestra tabla. Define cada columna y su tipo de dato.
    # TEXT: para texto, INTEGER: para números enteros, REAL: para números con decimales.
    # TIMESTAMP: para guardar la fecha y hora.
    sql_crear_tabla_registros = """
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        edad INTEGER,
        duracion_ciclo INTEGER,
        imc REAL,
        tiene_sop INTEGER,
        grado_endometriosis INTEGER,
        tiene_miomas INTEGER,
        mioma_submucoso INTEGER,
        mioma_intramural_significativo INTEGER,
        mioma_subseroso_grande INTEGER,
        amh REAL,
        prolactina REAL,
        tsh REAL,
        tpo_ab_positivo INTEGER,
        insulina_ayunas REAL,
        glicemia_ayunas REAL,
        concentracion_esperm REAL,
        motilidad_progresiva REAL,
        morfologia_normal REAL,
        vitalidad_esperm REAL,
        pronostico_final REAL
    );
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql_crear_tabla_registros)
        print("Tabla 'registros' creada con éxito o ya existente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")

def main():
    database = "fertilidad.db"
    
    # Crea una conexión a la base de datos (se creará el archivo si no existe)
    conn = crear_conexion(database)
    
    if conn is not None:
        # Crea la tabla
        crear_tabla(conn)
        conn.close()
    else:
        print("Error: No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    main()