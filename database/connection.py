import sqlite3
import os

def _crear_tabla_registros(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, edad INTEGER,
        duracion_ciclo INTEGER, imc REAL, tiene_sop INTEGER, grado_endometriosis INTEGER,
        tiene_miomas INTEGER, mioma_submucoso INTEGER, mioma_submucoso_multiple INTEGER,
        mioma_intramural_significativo INTEGER, mioma_subseroso_grande INTEGER,
        tipo_adenomiosis TEXT, tipo_polipo TEXT, resultado_hsg TEXT, amh REAL,
        prolactina REAL, tsh REAL, tpo_ab_positivo INTEGER, insulina_ayunas REAL,
        glicemia_ayunas REAL, volumen_seminal REAL, concentracion_esperm REAL,
        motilidad_progresiva REAL, morfologia_normal REAL, vitalidad_esperm REAL,
        pronostico_final REAL, tema TEXT
    );
    """
    conn.cursor().execute(sql)

def _crear_tabla_riesgo_aborto(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS riesgo_aborto (
        id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, edad INTEGER,
        imc REAL, abortos_previos INTEGER, tiene_miomas INTEGER, tiene_adenomiosis INTEGER,
        tiene_sop INTEGER, tiene_diabetes INTEGER, tiene_tiroides INTEGER,
        prolactina_alta INTEGER, infecciones_previas INTEGER, calidad_semen_alterada INTEGER,
        riesgo_final REAL, categoria TEXT
    );
    """
    conn.cursor().execute(sql)

def _crear_tabla_logros(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS logros (
        id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL UNIQUE,
        descripcion TEXT NOT NULL, obtenido INTEGER DEFAULT 0, timestamp TEXT
    );
    """
    conn.cursor().execute(sql)

def crear_conexion_y_tablas(db_file="fertilidad.db"):
    """
    Crea una conexión a la base de datos y asegura que todas las tablas existan.
    """
    conn = sqlite3.connect(db_file, check_same_thread=False)
    
    # Llama a las funciones para crear cada tabla
    _crear_tabla_registros(conn)
    _crear_tabla_riesgo_aborto(conn)
    _crear_tabla_logros(conn)

    # Guarda los cambios (creación de tablas)
    conn.commit()
    return conn