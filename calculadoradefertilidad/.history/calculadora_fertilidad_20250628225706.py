from datetime import datetime, timedelta

# --- FASE DE MODELADO: EL CEREBRO DE LA APLICACIÓN ---
# Aquí definimos la plantilla para nuestro "Paciente Digital"

class CicloFisiologico:
    def __init__(self, fecha_ultimo_periodo, duracion_ciclo, duracion_fase_lutea=14):
        """
        El constructor de nuestro 'expediente'. Se ejecuta al crear un nuevo ciclo.
        'self' se refiere a la instancia específica del ciclo que estamos creando.
        """
        # --- Variables Básicas (Basadas en tu expertise) ---
        self.fum_str = fecha_ultimo_periodo
        self.duracion_ciclo = duracion_ciclo
        self.duracion_fase_lutea = duracion_fase_lutea
        
        # Atributos que calcularemos después
        self.fum_date = None
        self.error = None
        self.resultados = {}

        # Iniciar el proceso de validación y cálculo
        self._validar_y_preparar()

    def _validar_y_preparar(self):
        """Un método 'privado' para validar la FUM y prepararla."""
        try:
            self.fum_date = datetime.strptime(self.fum_str, '%d-%m-%Y').date()
        except ValueError:
            self.error = "Formato de fecha inválido. Por favor, usa DD-MM-AAAA."

    def calcular_eventos_clave(self):
        """
        El método principal que realiza todos los cálculos basados en las variables.
        """
        if self.error:
            return # Si hubo un error en la fecha, no calculamos nada.

        # 1. Calcular próximo periodo
        fecha_proximo_periodo = self.fum_date + timedelta(days=self.duracion_ciclo)

        # 2. Calcular ovulación (¡USANDO TU LÓGICA EXPERTA!)
        # La ovulación ocurre 'duracion_fase_lutea' días ANTES del próximo periodo.
        fecha_ovulacion = fecha_proximo_periodo - timedelta(days=self.duracion_fase_lutea)

        # 3. Calcular ventana fértil (2 días antes, ovulación, 2 días después)
        inicio_ventana = fecha_ovulacion - timedelta(days=2)
        fin_ventana = fecha_ovulacion + timedelta(days=2)

        # Guardamos los resultados formateados
        self.resultados = {
            "proximo_periodo": fecha_proximo_periodo.strftime('%d-%m-%Y'),
            "dia_ovulacion_estimado": fecha_ovulacion.strftime('%d-%m-%Y'),
            "ventana_fertil_inicio": inicio_ventana.strftime('%d-%m-%Y'),
            "ventana_fertil_fin": fin_ventana.strftime('%d-%m-%Y')
        }
        
    def obtener_resultados_display(self):
        """Devuelve los resultados para mostrarlos al usuario."""
        if self.error:
            return {"error": self.error}
        return self.resultados

# --- FASE DE INTERACCIÓN: LA 'APP' DE TERMINAL ---
# Esta parte no cambia mucho, pero ahora usa nuestra nueva Clase.

print("--- Calculadora de Fertilidad Profesional ---")

# 1. Recolectamos los datos del usuario
fecha_input = input("Introduce la fecha de inicio del último periodo (FUM) (DD-MM-AAAA): ")
ciclo_input_str = input("Introduce la duración promedio de tu ciclo (ej: 28): ")
lutea_input_str = input("Introduce la duración de tu fase lútea (presiona Enter para usar 14 días): ")

try:
    ciclo_input = int(ciclo_input_str)
    # Si el usuario no ingresa nada para la fase lútea, usamos el default de 14
    lutea_input = int(lutea_input_str) if lutea_input_str else 14

    # 2. Creamos una instancia de nuestro "paciente digital"
    ciclo_actual = CicloFisiologico(
        fecha_ultimo_periodo=fecha_input,
        duracion_ciclo=ciclo_input,
        duracion_fase_lutea=lutea_input
    )

    # 3. Le pedimos que calcule los eventos
    ciclo_actual.calcular_eventos_clave()

    # 4. Obtenemos y mostramos los resultados
    calculos = ciclo_actual.obtener_resultados_display()

    if "error" in calculos:
        print(f"\nError: {calculos['error']}")
    else:
        print("\n--- Resultados del Ciclo ---")
        print(f"Próximo periodo estimado: {calculos['proximo_periodo']}")
        print(f"Día de ovulación estimado: {calculos['dia_ovulacion_estimado']}")
        print(f"Ventana de máxima fertilidad: del {calculos['ventana_fertil_inicio']} al {calculos['ventana_fertil_fin']}")
        print("\n*Cálculos basados en una duración de ciclo de {ciclo_input} días y una fase lútea de {lutea_input} días.")
        print("*Esta es una herramienta de modelado y no reemplaza el diagnóstico clínico.")

except ValueError:
    print("\nError: La duración del ciclo y de la fase lútea deben ser números enteros.")