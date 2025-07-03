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
    resultado_hsg = datos.get('resultado_hsg')
    
    concentracion = datos.get('concentracion_esperm')
    motilidad = datos.get('motilidad_progresiva')

    trompas_permeables = resultado_hsg == 'normal'
    baja_reserva_ovarica = amh is not None and amh < 0.7

    # --- 2. Sistema de Decisión Jerárquico ---

    # NIVEL 1: Ovodonación
    if edad > 42:
        return ["✔️ Ovodonación: Recomendada por edad materna avanzada (>42 años)."], "Ovodonación"

    # NIVEL 2: Ligadura de Trompas (OTB)
    elif otb:
        if amh is None:
            return ["✔️ FIV: Es la opción más directa. Se necesita AMH para una recomendación más precisa."], "FIV / ICSI"
        
        # ✅ CORRECCIÓN: Se usa 'elif' para conectar las condiciones y evitar el fallo.
        if edad < 35 and amh > 1.5:
            return ["✔️ Recanalización de Trompas: Buena candidata por edad y excelente reserva ovárica."], "Recanalización de Trompas"
        else:
            return ["✔️ FIV: Es el tratamiento recomendado para tu perfil para optimizar tiempo y éxito."], "FIV / ICSI"
            
    # NIVEL 3: Causas Graves que indican FIV/ICSI
    elif not trompas_permeables and resultado_hsg is not None:
        return ["✔️ FIV / ICSI: Indicado porque las trompas no son permeables."], "FIV / ICSI"
    elif (concentracion is not None and concentracion < 5) or (motilidad is not None and motilidad < 20):
        return ["✔️ FIV / ICSI: Recomendado por factor masculino moderado a severo."], "FIV / ICSI"
    elif baja_reserva_ovarica and edad >= 35:
        return ["✔️ FIV / ICSI: Sugerido por la combinación de baja reserva y edad."], "FIV / ICSI"

    # NIVEL 4 y 5: Técnicas de Baja Complejidad (solo si las trompas son permeables)
    elif trompas_permeables:
        # Se intenta primero con IIU si hay datos masculinos
        if concentracion is not None and motilidad is not None:
            if concentracion >= 5 and motilidad >= 32:
                return ["✔️ Inseminación Intrauterina (IIU): Buena opción por parámetros seminales adecuados."], "Inseminación Intrauterina"
            elif concentracion >= 5 and 20 <= motilidad < 32:
                return ["✔️ Inseminación Intrauterina (IIU): Posible, pero con éxito limitado por motilidad moderada."], "Inseminación Intrauterina (Éxito Limitado)"

        # Si no aplica IIU, se revisa si aplica Coito Programado
        if tiene_sop and edad < 35:
            return ["✔️ Coito Programado: Recomendado para parejas jóvenes con SOP como causa principal."], "Coito Programado"

    # NIVEL FINAL: Sin criterios claros
    return ["🔎 No se detectaron criterios claros para una técnica específica. Se sugiere continuar con la evaluación."], "Evaluación Continua"