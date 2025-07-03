def obtener_recomendaciones(datos):
    """
    Central de Recomendaciones con la jerarquía de decisión correcta.
    Determina la técnica de reproducción asistida más adecuada basada en
    un sistema de prioridades y datos clínicos.
    """
    # --- 1. Extraer y procesar los datos de entrada ---
    edad = datos.get('edad', 30)
    amh = datos.get('amh')
    otb = datos.get('tiene_otb', False)
    tiene_sop = datos.get('tiene_sop', False)
    
    # Asumimos que las trompas son permeables a menos que se indique lo contrario
    trompas_permeables = datos.get('resultado_hsg', 'normal') == 'normal'
    
    concentracion = datos.get('concentracion_esperm')
    motilidad = datos.get('motilidad_progresiva')

    # Derivar conceptos clínicos a partir de los datos crudos
    baja_reserva_ovarica = amh is not None and amh < 0.7

    # --- 2. Sistema de Decisión Jerárquico (de mayor a menor prioridad) ---

    # NIVEL 1: Ovodonación (Prioridad Máxima)
    # Condiciones que anulan la posibilidad de usar óvulos propios.
    if edad > 42:
        return ["✔️ Ovodonación: Recomendada por edad materna avanzada (>42 años), que disminuye drásticamente la calidad ovocitaria."], "Ovodonación"

    # NIVEL 2: Ligadura de Trompas (OTB)
    # Esta condición es especial y debe evaluarse antes que otras causas de FIV.
    elif otb:
        if amh is None:
            return ["✔️ Fecundación In Vitro (FIV): Es la opción más directa tras una ligadura. Se necesita el valor de AMH para una recomendación más precisa entre FIV o cirugía."], "FIV / ICSI"
        
        # Candidata ideal para Recanalización Tubárica (cirugía)
        if edad < 35 and amh > 1.5:
            return ["✔️ Recanalización de Trompas: Eres buena candidata para esta cirugía por tu edad (<35 años) y excelente reserva ovárica (AMH > 1.5)."], "Recanalización de Trompas"
        
        # Mala candidata para cirugía o casos intermedios, se prefiere FIV
        else:
            return ["✔️ Fecundación In Vitro (FIV): Para tu perfil de edad y/o reserva ovárica, la FIV es el tratamiento recomendado para optimizar el tiempo y las probabilidades de éxito."], "FIV / ICSI"
            
    # NIVEL 3: Factor Masculino Severo o Factores Femeninos Graves que indican FIV/ICSI
    elif (concentracion is not None and concentracion < 5) or (motilidad is not None and motilidad < 20):
        return ["✔️ FIV / ICSI: Recomendado por un factor masculino moderado a severo que dificulta la fertilización por métodos más sencillos."], "FIV / ICSI"
    
    elif baja_reserva_ovarica and edad >= 35:
         return ["✔️ FIV / ICSI: Sugerido por la combinación de baja reserva ovárica y una edad donde es crucial optimizar cada ciclo."], "FIV / ICSI"

    # NIVEL 4: Inseminación Intrauterina (IIU)
    # Para casos de menor complejidad con trompas permeables.
    elif trompas_permeables and concentracion is not None and motilidad is not None:
        if concentracion >= 5 and motilidad >= 32:
            return ["✔️ Inseminación Intrauterina (IIU): Buena opción por parámetros seminales adecuados y trompas permeables."], "Inseminación Intrauterina"
        elif concentracion >= 5 and 20 <= motilidad < 32:
            return ["✔️ Inseminación Intrauterina (IIU): Es una posibilidad, pero con tasa de éxito limitada por motilidad progresiva moderada."], "Inseminación Intrauterina (Éxito Limitado)"

    # NIVEL 5: Coito Programado
    # El caso de menor complejidad.
    elif tiene_sop and edad < 35 and trompas_permeables:
        return ["✔️ Coito Programado: Recomendado para parejas jóvenes con SOP como causa principal y trompas permeables."], "Coito Programado"

    # NIVEL FINAL: Sin criterios claros
    else:
        return ["🔎 No se detectaron criterios claros para una técnica de reproducción asistida. Se sugiere continuar con la evaluación o buscar embarazo de forma natural."], "Evaluación Continua"