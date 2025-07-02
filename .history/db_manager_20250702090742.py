# db_manager.py - CÓDIGO COMPLETO Y CORREGIDO

import sqlite3
from datetime import datetime
import pandas as pd
import os # <-- ¡CAMBIO 1: AÑADIDO!
import streamlit as st

def crear_conexion(db_file):
    """
    Crea una conexión a la base de datos SQLite.
    Si el archivo no existe, lo crea y también las tablas necesarias.
    Si el archivo ya existe, verifica que las tablas estén completas.
    """
    import sqlite3
    import os
    db_existe = os.path.exists(db_file)
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        if not db_existe:
            crear_tabla(conn)
            crear_tabla_logros(conn)
            inicializar_logros(conn)
        else:
            # 👇 Verificar si la tabla logros existe aunque la base ya exista
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logros'")
            tabla_logros = cursor.fetchone()
            if not tabla_logros:
                crear_tabla_logros(conn)
                inicializar_logros(conn)
        
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
        pronostico_final REAL,
        tema TEXT
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_crear_tabla_registros)
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")
def crear_tabla_logros(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS logros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        obtenido INTEGER DEFAULT 0,
        timestamp TEXT
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
    except sqlite3.Error as e:
        print(f"Error al crear la tabla logros: {e}")

def inicializar_logros(conn):
    from config import LOGROS_DISPONIBLES
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM logros")
    if cursor.fetchone()[0] == 0:
        for logro in LOGROS_DISPONIBLES:
            cursor.execute(
                "INSERT INTO logros (nombre, descripcion, obtenido, timestamp) VALUES (?, ?, ?, ?)",
                (logro['nombre'], logro['descripcion'], 0, None)
            )
        conn.commit()

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
    vitalidad_esperm, pronostico_final, tema
) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, registro_data)
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        raise e  # 👈 Este cambio es obligatorio
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
    # El siguiente bloque debe estar indentado dentro de una función o eliminado si no se usa.
    # Si quieres ejecutar estas funciones al correr el script, debes definir 'db_existe' y 'conn' en este contexto.
    # Por ejemplo, podrías mover este bloque dentro de la función main() después de crear la conexión.
    # Aquí te muestro cómo hacerlo correctamente:

    # main()
    # database = "fertilidad.db"
    # conn = crear_conexion(database)
    # db_existe = os.path.exists(database)
    # if not db_existe:
    #     crear_tabla(conn)
    #     crear_tabla_logros(conn)  # 👈 NUEVO
    #     inicializar_logros(conn)  # 👈 NUEVO

    from datetime import datetime

def preparar_registro_db(evaluacion):
    """
    Toma un objeto de evaluación y lo transforma en una tupla
    lista para ser insertada en la base de datos.
    """
    try:
        # Extrae el valor numérico del pronóstico
        pronostico_num = float(evaluacion.probabilidad_ajustada_final.replace('%', ''))
    except:
        pronostico_num = 0.0

    # Construye la tupla con todos los datos en el orden correcto para la BBDD
    registro_tuple = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        evaluacion.edad,
        evaluacion.duracion_ciclo,
        round(evaluacion.imc, 2) if evaluacion.imc is not None else None,
        1 if evaluacion.tiene_sop else 0,
        evaluacion.grado_endometriosis,
        1 if evaluacion.tiene_miomas else 0,
        1 if getattr(evaluacion, 'mioma_submucoso', False) else 0,
        1 if getattr(evaluacion, 'mioma_submucoso_multiple', False) else 0,
        1 if getattr(evaluacion, 'mioma_intramural_significativo', False) else 0,
        1 if getattr(evaluacion, 'mioma_subseroso_grande', False) else 0,
        evaluacion.tipo_adenomiosis,
        evaluacion.tipo_polipo,
        evaluacion.resultado_hsg,
        evaluacion.amh,
        evaluacion.prolactina,
        evaluacion.tsh,
        1 if evaluacion.tpo_ab_positivo else 0,
        evaluacion.insulina_ayunas,
        evaluacion.glicemia_ayunas,
        evaluacion.volumen_seminal,
        evaluacion.concentracion_esperm,
        evaluacion.motilidad_progresiva,
        evaluacion.morfologia_normal,
        evaluacion.vitalidad_esperm,
        pronostico_num,
        st.session_state.get('tema', 'light')

    )
    return registro_tuple
from datetime import datetime

def desbloquear_logro(conn, nombre_logro):
    cursor = conn.cursor()
    cursor.execute("UPDATE logros SET obtenido = 1, timestamp = ? WHERE nombre = ? AND obtenido = 0", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), nombre_logro))
    conn.commit()

def obtener_logros(conn):
    return pd.read_sql_query("SELECT * FROM logros", conn)
