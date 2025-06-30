from datetime import datetime, timedelta

class CicloFisiologico:
    def __init__(self, fecha_ultimo_periodo, duracion_ciclo, edad=None, tiene_sop=False):
        """
        Constructor del 'expediente'.
        #ELIMINADO: Se quitó duracion_fase_lutea.
        #NUEVO: Se añaden variables opcionales con valores por defecto.
        """
        # --- Variables Básicas ---
        self.fum_str = fecha_ultimo_periodo
        self.duracion_ciclo = duracion_ciclo
        
        # --- Variables Opcionales (Fase 2) ---
        self.edad = edad
        self.tiene_sop = tiene_sop
        
        # Atributos internos
        self.fum_date = None
        self.error = None
        self.resultados = {}
        self.resultados['notas_clinicas'] = [] # NUEVO: Un lugar para guardar las notas

        self._validar_y_preparar()

    def _validar_y_preparar(self):
        try:
            self.fum_date = datetime.strptime(self.fum_str, '%d-%m-%Y').date()
        except ValueError:
            self.error = "Formato de fecha inválido. Por favor, usa DD-MM-AAAA."

    def calcular_eventos_clave(self):
        """
        Calcula las fechas clave.
        """
        if self.error: return

        fecha_proximo_periodo = self.fum_date + timedelta(days=self.duracion_ciclo)
        
        # ELIMINADO: La lógica de fase lútea. Volvemos al cálculo estándar.
        # Se asume una fase lútea de 14 días como aproximación general.
        fecha_ovulacion = fecha_proximo_periodo - timedelta(days=14)

        inicio_ventana = fecha_ovulacion - timedelta(days=2)
        fin_ventana = fecha_ovulacion + timedelta(days=2)

        self.resultados['proximo_periodo'] = fecha_proximo_periodo.strftime('%d-%m-%Y')
        self.resultados['dia_ovulacion_estimado'] = fecha_ovulacion.strftime('%d-%m-%Y')
        self.resultados['ventana_fertil_inicio'] = inicio_ventana.strftime('%d-%m-%Y')
        self.resultados['ventana_fertil_fin'] = fin_ventana.strftime('%d-%m-%Y')

    # NUEVO: Método para analizar las variables opcionales
    def analizar_factores_opcionales(self):
        """
        Aplica reglas de negocio basadas en el perfil del usuario
        y añade notas clínicas a los resultados.
        """
        if self.error: return
        
        # Regla 1: Edad
        if self.edad is not None and self.edad > 35:
            nota_edad = "A partir de los 35 años, la reserva ovárica puede disminuir. Se recomienda consulta especializada para una evaluación completa."
            self.resultados['notas_clinicas'].append(nota_edad)

        # Regla 2: SOP (Síndrome de Ovario Poliquístico)
        if self.tiene_sop:
            nota_sop = "En casos de SOP, los ciclos pueden ser irregulares y la ovulación puede no ocurrir en la fecha estimada. El seguimiento ecográfico y/o con tests de LH es más preciso."
            self.resultados['notas_clinicas'].append(nota_sop)

    def obtener_resultados_display(self):
        if self.error:
            return {"error": self.error}
        return self.resultados

# --- FASE DE INTERACCIÓN ---

print("--- Calculadora de Fertilidad Profesional (Fase 2) ---")

fecha_input = input("Introduce la fecha de inicio del último periodo (FUM) (DD-MM-AAAA): ")
ciclo_input_str = input("Introduce la duración promedio de tu ciclo (ej: 28): ")

# NUEVO: Pedimos los datos opcionales
print("\n--- Datos Opcionales (puedes dejarlos en blanco) ---")
edad_input_str = input("Introduce tu edad: ")
sop_input_str = input("¿Tienes diagnóstico de SOP (Síndrome de Ovario Poliquístico)? (si/no): ")

try:
    ciclo_input = int(ciclo_input_str)
    
    # Procesamos los datos opcionales
    edad_input = int(edad_input_str) if edad_input_str else None
    sop_input = True if sop_input_str.lower() == 'si' else False

    # Creamos la instancia con todos los datos
    ciclo_actual = CicloFisiologico(
        fecha_ultimo_periodo=fecha_input,
        duracion_ciclo=ciclo_input,
        edad=edad_input,
        tiene_sop=sop_input
    )

    # Ejecutamos la secuencia de cálculo y análisis
    ciclo_actual.calcular_eventos_clave()
    ciclo_actual.analizar_factores_opcionales() # NUEVO paso

    calculos = ciclo_actual.obtener_resultados_display()

    if "error" in calculos:
        print(f"\nError: {calculos['error']}")
    else:
        print("\n--- Resultados del Ciclo ---")
        print(f"Próximo periodo estimado: {calculos['proximo_periodo']}")
        print(f"Día de ovulación estimado: {calculos['dia_ovulacion_estimado']}")
        print(f"Ventana de máxima fertilidad: del {calculos['ventana_fertil_inicio']} al {calculos['ventana_fertil_fin']}")
        
        # NUEVO: Mostramos las notas clínicas si existen
        if calculos['notas_clinicas']:
            print("\n--- Notas Clínicas Personalizadas ---")
            for nota in calculos['notas_clinicas']:
                print(f"- {nota}")

        print("\n*Esta es una herramienta de modelado y no reemplaza el diagnóstico clínico.")

except ValueError:
    print("\nError: La duración del ciclo y la edad deben ser números enteros.")