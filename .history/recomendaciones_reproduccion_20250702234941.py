def obtener_recomendaciones(datos):
    """
    CENTRAL DE RECOMENDACIONES: Determina la técnica de reproducción
    asistida más adecuada, incluyendo la lógica detallada para OTB.
    """
    # --- 1. Extraer los datos necesarios ---
    edad = datos.get('edad', 30)
    amh = datos.get('amh')
    otb = datos.get('tiene_otb', False)
    concentracion = datos.get('concentracion')
    motilidad = datos.get('motilidad')
    baja_reserva_ovarica = datos.get('baja_reserva_ovarica', False)
    trompas_permeables = datos.get('trompas_permeables', False)
    tiene_sop = datos.get('tiene_sop', False)
    # ... (aquí irían los otros datos que ya tenías: concentracion, motilidad, etc.)

    # --- 2. Sistema de decisión jerárquico ---

    # NIVEL 1: Ovodonación (la condición más determinante)
    if (amh is not None and amh < 0.2) or edad > 42:
        return ["✔️ Ovodonación: Recomendada por muy baja reserva ovárica o edad materna avanzada."], "Ovodonación"

    # NIVEL 2: Paciente con ligadura de trompas (OTB)
    if otb:
        # Primero, verificamos que tengamos el dato de AMH para decidir.
        if amh is None:
            return ["✔️ Fecundación In Vitro (FIV): Se necesita el valor de AMH para una recomendación precisa, pero la FIV es la opción más directa tras una ligadura."], "FIV / ICSI"

        # Candidata ideal para Recanalización
        if edad < 35 and amh > 1.5:
            return ["✔️ Recanalización de Trompas: Eres buena candidata para esta cirugía por tu edad (<35 años) y excelente reserva ovárica (AMH > 1.5)."], "Recanalización de Trompas"

        # Mala candidata para Recanalización
        elif edad > 37 and amh < 1.0:
            return ["✔️ Fecundación In Vitro (FIV): No se recomienda la recanalización por la combinación de edad (>37 años) y baja reserva ovárica (AMH < 1.0). La FIV ofrece un éxito mucho mayor."], "FIV / ICSI"

        # Casos intermedios o grises
        else:
            return ["✔️ Fecundación In Vitro (FIV): Para tu perfil de edad y reserva ovárica, la FIV es el tratamiento recomendado para optimizar el tiempo y las probabilidades de éxito."], "FIV / ICSI"

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