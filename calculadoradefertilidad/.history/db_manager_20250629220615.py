# db_manager.py
import sqlite3
from datetime import datetime

# (La función crear_conexion y crear_tabla permanecen sin cambios)
def crear_conexion(db_file):
    """Crea una conexión a la base de datos SQLite."""
    conn = None;
    try: conn = sqlite3.connect(db_file); return conn
    except sqlite3.Error as e: print(e)
    return conn

def crear_tabla(conn):
    """Crea la tabla para almacenar los registros de fertilidad."""
    sql_crear_tabla_registros = """
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, edad INTEGER,
        duracion_ciclo INTEGER, imc REAL, tiene_sop INTEGER, grado_endometriosis INTEGER,
        tiene_miomas INTEGER, mioma_submucoso INTEGER, mioma_intramural_significativo INTEGER,
        mioma_subseroso_grande INTEGER, amh REAL, prolactina REAL, tsh REAL,
        tpo_ab_positivo INTEGER, insulina_ayunas REAL, glicemia_ayunas REAL,
        concentracion_esperm REAL, motilidad_progresiva REAL, morfologia_normal REAL,
        vitalidad_esperm REAL, pronostico_final REAL
    );"""
    try: cursor = conn.cursor(); cursor.execute(sql_crear_tabla_registros);
    except sqlite3.Error as e: print(f"Error al crear la tabla: {e}")

# --- AÑADIMOS LA NUEVA FUNCIÓN ---
def insertar_registro(conn, registro_data):
    """
    Inserta un nuevo registro en la tabla 'registros'.
    :param conn: Objeto de conexión a la base de datos.
    :param registro_data: Una tupla con los datos del registro a insertar.
    :return: id del último registro insertado.
    """
    sql = ''' INSERT INTO registros(timestamp, edad, duracion_ciclo, imc, tiene_sop, 
                                    grado_endometriosis, tiene_miomas, mioma_submucoso, 
                                    mioma_intramural_significativo, mioma_subseroso_grande, 
                                    amh, prolactina, tsh, tpo_ab_positivo, insulina_ayunas, 
                                    glicemia_ayunas, concentracion_esperm, motilidad_progresiva, 
                                    morfologia_normal, vitalidad_esperm, pronostico_final)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, registro_data)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error al insertar el registro: {e}")
        return None

# (La función main permanece sin cambios)
def main():
    database = "fertilidad.db"; conn = crear_conexion(database)
    if conn is not None: crear_tabla(conn); conn.close()
    else: print("Error: No se pudo crear la conexión a la base de datos.")

if __name__ == '__main__':
    main()