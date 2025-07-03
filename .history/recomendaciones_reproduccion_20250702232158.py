def obtener_recomendaciones(datos):
    """
    Determina la técnica de reproducción asistida más adecuada
    basada en un sistema de prioridades jerárquicas y datos clínicos.
    """
    # --- 1. Extraer y traducir los datos de entrada ---
    edad = datos.get('edad', 30)
    amh = datos.get('amh') # Necesitamos el valor de la AMH
    otb = datos.get('tiene_otb', False)
    fallo_ovario = datos.get('fallo_ovario', False) # Asumimos que esto podría venir de otra lógica
    
    tiene_sop = datos.get('tiene_sop', False)
    # Si no se especifica, asumimos que las trompas son permeables para lógicas como IIU o coito.
    trompas_permeables = datos.get('resultado_hsg', 'normal') == 'normal' 
    
    concentracion = datos.get('concentracion_esperm')
    motilidad = datos.get('motilidad_progresiva')

    # --- 2. Derivar conceptos clínicos a partir de los datos ---
    # ✅ LÓGICA MEJORADA: La baja reserva se determina por la AMH.
    baja_reserva_ovarica = amh is not None and amh < 0.7

    # --- 3. Sistema de decisión jerárquico (de mayor a menor complejidad) ---

    # NIVEL 1: Ovodonación (la condición más determinante)
    if fallo_ovario or edad > 42:
        return ["✔️ Ovodonación: Recomendada por fallo ovárico o edad materna avanzada (>42 años)."], "Ovodonación"

    # NIVEL 2: Paciente con ligadura de trompas (OTB)
    # ✅ LÓGICA MEJORADA: Se decide entre Recanalización o FIV.
    if otb:
        # Buena candidata para cirugía reconstructiva
        if edad < 35 and amh is not None and amh > 1.0:
            return ["✔️ Recanalización de Trompas: Por ser joven y con buena reserva ovárica, la cirugía para revertir la ligadura es una opción viable."], "Recanalización de Trompas"
        # En el resto de los casos con OTB, la FIV es más directa y efectiva
        else:
            return ["✔️ Fecundación In Vitro (FIV): Es el tratamiento recomendado, ya que no necesita el uso de las trompas y ofrece las mejores tasas de éxito en este escenario."], "FIV / ICSI"

    # NIVEL 3: Factor Masculino Severo o Factores Femeninos Graves
    if (concentracion is not None and concentracion < 1):
        return ["✔️ ICSI: Indicado por factor masculino muy severo (concentración < 1 millón/ml)."], "ICSI"
        
    if (baja_reserva_ovarica and edad >= 35) or (concentracion is not None and concentracion < 5) or (motilidad is not None and motilidad < 20):
        return ["✔️ FIV / ICSI: Recomendado por baja reserva en >35 años o por factor masculino moderado a severo."], "FIV / ICSI"

    # NIVEL 4: Inseminación Intrauterina (Factor Masculino Leve o Causa Inexplicada)
    if trompas_permeables and concentracion is not None and motilidad is not None:
        if concentracion >= 5 and motilidad >= 32:
            return ["✔️ Inseminación Intrauterina (IIU): Buena opción por parámetros seminales adecuados y trompas permeables."], "Inseminación Intrauterina"
        elif concentracion >= 5 and 20 <= motilidad < 32:
            return ["✔️ Inseminación Intrauterina (IIU): Es posible, pero con tasa de éxito limitada por motilidad moderada."], "Inseminación Intrauterina (Éxito Limitado)"

    # NIVEL 5: Coito Programado (Casos de baja complejidad)
    if tiene_sop and edad < 35 and trompas_permeables:
        return ["✔️ Coito Programado: Recomendado para parejas jóvenes con SOP como causa principal y trompas permeables."], "Coito Programado"

    # NIVEL 6: Caso por defecto si no se cumple ninguna condición
    return ["🔎 No se detectaron criterios claros para una técnica específica. Se sugiere continuar con la evaluación o buscar embarazo de forma natural."], "Evaluación Continua"