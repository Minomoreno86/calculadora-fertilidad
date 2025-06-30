# Importamos las herramientas necesarias del módulo datetime
from datetime import datetime, timedelta

def calcular_ventana_fertil(fecha_ultimo_periodo_str, duracion_ciclo):
    """
    Calcula la ventana de fertilidad y la próxima fecha de periodo.

    Args:
        fecha_ultimo_periodo_str (str): La fecha en formato 'YYYY-MM-DD'.
        duracion_ciclo (int): La duración promedio del ciclo en días.

    Returns:
        dict: Un diccionario con las fechas calculadas o un mensaje de error.
    """
    try:
        # Paso 1: Convertir el texto de la fecha a un objeto 'date' de Python
        fecha_ultimo_periodo = datetime.strptime(fecha_ultimo_periodo_str, '%Y-%m-%d').date()
    except ValueError:
        return {"error": "Formato de fecha inválido. Por favor, usa AAAA-MM-DD."}

    # Paso 2: Calcular la fecha estimada del próximo periodo
    fecha_proximo_periodo = fecha_ultimo_periodo + timedelta(days=duracion_ciclo)

    # Paso 3: Calcular la fecha estimada de ovulación (14 días ANTES del próximo periodo)
    fecha_ovulacion = fecha_proximo_periodo - timedelta(days=14)

    # Paso 4: Calcular la ventana fértil (5 días antes de la ovulación hasta el día de la ovulación)
    inicio_ventana_fertil = fecha_ovulacion - timedelta(days=5)
    fin_ventana_fertil = fecha_ovulacion

    # Paso 5: Organizar los resultados en un diccionario para devolverlos
    # Usamos .strftime('%Y-%m-%d') para convertir las fechas de vuelta a texto legible
    resultados = {
        "proximo_periodo": fecha_proximo_periodo.strftime('%Y-%m-%d'),
        "dia_ovulacion_estimado": fecha_ovulacion.strftime('%Y-%m-%d'),
        "ventana_fertil_inicio": inicio_ventana_fertil.strftime('%Y-%m-%d'),
        "ventana_fertil_fin": fin_ventana_fertil.strftime('%Y-%m-%d')
    }
    
    return resultados

# --- Zona de Interacción con el Usuario (Nuestra 'app' de terminal) ---

print("--- Calculadora de Fertilidad ---")

# Pedimos los datos al usuario
fecha_input = input("Introduce la fecha de inicio de tu último periodo (formato AAAA-MM-DD): ")
ciclo_input_str = input("Introduce la duración promedio de tu ciclo (ej: 28): ")

# Validamos que la duración del ciclo sea un número
try:
    ciclo_input_int = int(ciclo_input_str)
    
    # Llamamos a nuestra función 'cerebro' con los datos del usuario
    calculos = calcular_ventana_fertil(fecha_input, ciclo_input_int)

    # Mostramos los resultados
    if "error" in calculos:
        print(f"\nError: {calculos['error']}")
    else:
        print("\n--- Resultados Estimados ---")
        print(f"Tu próximo periodo podría empezar alrededor del: {calculos['proximo_periodo']}")
        print(f"Tu día de ovulación estimado es: {calculos['dia_ovulacion_estimado']}")
        print(f"Tu ventana de máxima fertilidad es del {calculos['ventana_fertil_inicio']} al {calculos['ventana_fertil_fin']}.")
        print("\nRecuerda: Esto es una estimación y no reemplaza el consejo médico.")

except ValueError:
    print("\nError: La duración del ciclo debe ser un número entero (ej: 28).")