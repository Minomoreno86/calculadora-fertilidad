# db_manager.py - CÓDIGO COMPLETO Y CORREGIDO

import sqlite3
from datetime import datetime
import pandas as pd
import os # <-- ¡CAMBIO 1: AÑADIDO!

def crear_conexion(db_file):
    """
    Crea una conexión a la base de datos SQLite.
    Si el archivo de la BBDD no existe, lo crea y también las tablas necesarias.
    """
    # <-- ¡CAMBIO 2: LÓGICA COMPLETAMENTE REEMPLAZADA DENTRO DE ESTA FUNCIÓN!
    # Comprobamos si el archivo de la base de datos ya existe ANTES de conectar.
    db_existe = os.path.exists(db_file)
    
    conn = None
    try:
        # Creamos la conexión. SQLite creará el archivo .db si no existe.
        conn = sqlite3.connect(db_file)
        
        # Si la base de datos NO existía, llamamos a tu función para crear las tablas.
        if not db_existe:
            print(f"El archivo '{db_file}' no existía. Creando tablas...")
            crear_tabla(conn) # Usamos tu función crear_tabla que ya es correcta.
        
        return conn
    except sqlite3.Error as e:
        print(e)
        return conn

def crear_tabla(conn):
    """
    Crea la tabla 'registros' si no existe, con todas las columnas necesarias.
    """
    # Esta es la definición de tabla COMPLETA y CORRECTA
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
        mioma_submucoso_multiple INTEGER,
        mioma_intramural_significativo INTEGER,
        mioma_subseroso_grande INTEGER,
        tipo_adenomiosis TEXT,
        tipo_polipo TEXT,
        resultado_hsg TEXT,
        amh REAL,
        prolactina REAL,
        tsh REAL,
        tpo_ab_positivo INTEGER,
        insulina_ayunas REAL,
        glicemia_ayunas REAL,
        volumen_seminal REAL,
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
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")

def insertar_registro(conn, registro_data):
    """
    Inserta un nuevo registro en la tabla 'registros'.
    """
    # El comando INSERT ahora incluye la nueva columna
    sql = ''' INSERT INTO registros(
                timestamp, edad, duracion_ciclo, imc, tiene_sop, 
                grado_endometriosis, tiene_miomas, mioma_submucoso, 
                mioma_submucoso_multiple, mioma_intramural_significativo, 
                mioma_subseroso_grande, tipo_adenomiosis, tipo_polipo, 
                resultado_hsg, amh, prolactina, tsh, tpo_ab_positivo, 
                insulina_ayunas, glicemia_ayunas, volumen_seminal, 
                concentracion_esperm, motilidad_progresiva, morfologia_normal, 
                vitalidad_esperm, pronostico_final
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, registro_data)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al insertar el registro: {e}")
        return None

def leer_todos_los_registros(conn):
    """
    Lee todos los registros de la base de datos y los devuelve como un DataFrame de Pandas.
    """
    try:
        df = pd.read_sql_query("SELECT * FROM registros", conn)
        return df
    except Exception as e:
        print(f"Error al leer los registros: {e}")
        return pd.DataFrame()

def eliminar_registro_por_id(conn, id):
    """
    Elimina un registro específico por su ID.
    """
    sql = 'DELETE FROM registros WHERE id = ?'
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al eliminar el registro con ID {id}: {e}")

def eliminar_todos_los_registros(conn):
    """
    Elimina TODOS los registros de la tabla.
    """
    sql = 'DELETE FROM registros'
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al eliminar todos los registros: {e}")

def main():
    """
    Función principal para ser ejecutada cuando el script se corre directamente.
    Verifica la conexión y la existencia de la tabla.
    """
    database = "fertilidad.db"
    conn = crear_conexion(database)
    if conn is not None:
        print("Base de datos y tabla verificadas.")
        conn.close()
    else:
        print("Error: No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    main()