# En: database/logros_crud.py
import pandas as pd
from datetime import datetime
from config import LOGROS_DISPONIBLES

def inicializar_logros(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM logros")
    if cursor.fetchone()[0] == 0:
        for logro in LOGROS_DISPONIBLES:
            cursor.execute("INSERT INTO logros (nombre, descripcion) VALUES (?, ?)", (logro['nombre'], logro['descripcion']))
        conn.commit()

def desbloquear_logro(conn, nombre_logro):
    sql = "UPDATE logros SET obtenido = 1, timestamp = ? WHERE nombre = ? AND obtenido = 0"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.cursor().execute(sql, (timestamp, nombre_logro))
    conn.commit()

def obtener_logros(conn):
    return pd.read_sql_query("SELECT * FROM logros", conn)