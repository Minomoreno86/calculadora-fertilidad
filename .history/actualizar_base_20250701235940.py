import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('fertilidad.db')
cursor = conn.cursor()

try:
    # Intentar agregar la columna 'tema'
    cursor.execute('ALTER TABLE registros ADD COLUMN tema TEXT;')
    conn.commit()
    print("✅ Columna 'tema' agregada correctamente a la base de datos.")
except Exception as e:
    print(f"⚠️ Error al modificar la base de datos: {e}")
finally:
    conn.close()
