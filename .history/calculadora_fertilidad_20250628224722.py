# Importamos las herramientas necesarias del módulo datetime
from datetime import datetime, timedelta

def calcular_ventana_fertil(fecha_ultimo_periodo_str, duracion_ciclo):
    """
    Calcula la ventana de fertilidad y la próxima fecha de periodo.

    Args:
        fecha_ultimo_periodo_str (str): La fecha en formato 'DD-MM-YYYY'.
        duracion_ciclo (int): La duración promedio del ciclo en días.

    Returns:
        dict: Un diccionario con las fechas calculadas o un mensaje de error.
    """
    try:
        fecha_ultimo_periodo = datetime.strptime(fecha_ultimo_periodo_str, '%d-%m-%Y').date()
    except ValueError:
        return {"error": "Formato de fecha inválido. Por favor, usa DD-MM-AAAA."}

    fecha_proximo_periodo = fecha_ultimo_periodo + timedelta(days=duracion_ciclo)
    fecha_ovulacion = fecha_proximo_periodo - timedelta(days=14)

    # CAMBIO: Aquí ajustamos la regla para calcular la ventana fértil.
    # Ahora será 2 días antes y 2 días después del día de la ovulación.
    inicio_ventana_fertil = fecha_ovulacion - timedelta(days=2)
    fin_ventana_fertil = fecha_ovulacion + timedelta(days=2)

    resultados = {
        "proximo_periodo": fecha_proximo_periodo.strftime('%d-%m-%Y'),
        "dia_ovulacion_estimado": fecha_ovulacion.strftime('%d-%m-%Y'),
        "ventana_fertil_inicio": inicio_ventana_fertil.strftime('%d-%m-%Y'),
        "ventana_fertil_fin": fin_ventana_fertil.strftime('%d-%m-%Y')
    }
    
    return resultados

# --- Zona de Interacción con el Usuario (Nuestra 'app' de terminal) ---

print("--- Calculadora de Fertilidad ---")
fecha_input = input("Introduce la fecha de inicio de tu último periodo (formato DD-MM-AAAA): ")
ciclo_input_str = input("Introduce la duración promedio de tu ciclo (ej: 28): ")

try:
    ciclo_input_int = int(ciclo_input_str)
    calculos = calcular_ventana_fertil(fecha_input, ciclo_input_int)

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