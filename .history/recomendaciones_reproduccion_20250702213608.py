
def obtener_recomendaciones(datos):
    recomendaciones = []
    tecnica_sugerida = ""

    edad = datos.get('edad', 30)
    tiene_sop = datos.get('tiene_sop', False)
    trompas_permeables = datos.get('trompas_permeables', True)
    concentracion = datos.get('concentracion', 20.0)
    motilidad = datos.get('motilidad', 40.0)
    factor_tubario = datos.get('factor_tubario', False)
  
    recanalizacion_trompas = datos.get('recanalizacion_trompas', False)
    baja_reserva_ovarica = datos.get('baja_reserva', False)
    fallo_ovario = datos.get('fallo_ovario', False)

    # ===========================
    # Recanalización de Trompas
    # ===========================
    if recanalizacion_trompas:
        recomendaciones.append("✔️ Recanalización de trompas recomendada para reversión de ligadura tubárica en mujeres jóvenes (< 37 años) con buena longitud tubárica.")
        tecnica_sugerida = "Recanalización de Trompas"

    # ===========================
    # Coito Programado
    # ===========================
    if tiene_sop and edad < 35 and trompas_permeables:
        recomendaciones.append("✔️ Coito Programado recomendado por SOP  en pareja joven.")
        tecnica_sugerida = "Coito Programado"

    # ===========================
    # Factor Masculino: IIU, FIV o ICSI
    # ===========================
    if concentracion >= 5 and motilidad >= 32:
        recomendaciones.append("✔️ Inseminación Intrauterina (IIU) recomendada por parámetros seminales adecuados (≥ 5 millones/ml y motilidad ≥ 32%).")
        tecnica_sugerida = "Inseminación Intrauterina"

    elif concentracion >= 5 and 20 <= motilidad < 32:
        recomendaciones.append("✔️ IIU posible pero con baja tasa de éxito debido a motilidad moderada (20-31%).")
        tecnica_sugerida = "Inseminación Intrauterina (Éxito Limitado)"

    elif concentracion < 1:
        recomendaciones.append("✔️ ICSI sin discusión. La concentración espermática es inferior a 1 millón/ml.")
        tecnica_sugerida = "ICSI"

    elif concentracion < 5 or motilidad < 20:
        recomendaciones.append("✔️ FIV o ICSI recomendada por concentración < 5 millones/ml o motilidad progresiva < 20%.")
        tecnica_sugerida = "FIV / ICSI"

    # ===========================
    # FIV por otros factores
    # ===========================
    if factor_tubario or (baja_reserva_ovarica and edad >= 35):
        recomendaciones.append("✔️ FIV / ICSI recomendada por factor tubárico, baja reserva ovárica  en paciente ≥ 35 años.")
        tecnica_sugerida = "FIV / ICSI"

    # ===========================
    # Ovodonación
    # ===========================
    if fallo_ovario or edad > 42:
        recomendaciones.append("✔️ Ovodonación recomendada por fallo ovárico o edad materna avanzada.")
        tecnica_sugerida = "Ovodonación"

    if not recomendaciones:
        recomendaciones.append("🔎 No se detectaron criterios claros para técnicas específicas. Se sugiere continuar con evaluación básica o control prenatal habitual.")

    return recomendaciones, tecnica_sugerida