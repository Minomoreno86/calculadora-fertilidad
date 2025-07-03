# recomendaciones_reproduccion.py

def obtener_recomendaciones(datos):
    recomendaciones = []
    tecnica_sugerida = ""

    edad = datos.get('edad', 30)
    tiene_sop = datos.get('tiene_sop', False)
    trompas_permeables = datos.get('trompas_permeables', True)
    rem_suficiente = datos.get('rem_suficiente', True)
    factor_masculino_leve = datos.get('factor_masculino_leve', False)
    factor_masculino_severo = datos.get('factor_masculino_severo', False)
    factor_tubario = datos.get('factor_tubario', False)
    infertilidad_origen_desconocido = datos.get('iod', False)
    recanalizacion_trompas = datos.get('recanalizacion_trompas', False)
    baja_reserva_ovarica = datos.get('baja_reserva', False)
    fallo_ovario = datos.get('fallo_ovario', False)

    # ===========================
    # Coito Programado
    # ===========================
    if tiene_sop or infertilidad_origen_desconocido and edad < 35 and trompas_permeables and rem_suficiente:
        recomendaciones.append("✔️ Coito Programado recomendado por SOP o infertilidad de origen desconocido en pareja joven.")
        tecnica_sugerida = "Coito Programado"

    # ===========================
    # Inseminación Intrauterina
    # ===========================
    if factor_masculino_leve or infertilidad_origen_desconocido and rem_suficiente and trompas_permeables and edad < 38:
        recomendaciones.append("✔️ Inseminación Intrauterina sugerida por factor masculino leve o fallo previo de coito programado.")
        tecnica_sugerida = "Inseminación Intrauterina"

    # ===========================
    # FIV / ICSI
    # ===========================
    if factor_masculino_severo or factor_tubario or baja_reserva_ovarica or (infertilidad_origen_desconocido and edad >= 35):
        recomendaciones.append("✔️ FIV / ICSI recomendada por factor tubárico, factor masculino severo o baja reserva ovárica.")
        tecnica_sugerida = "FIV / ICSI"

    # ===========================
    # Ovodonación
    # ===========================
    if fallo_ovario or edad > 42:
        recomendaciones.append("✔️ Ovodonación recomendada por fallo ovárico o edad materna avanzada.")
        tecnica_sugerida = "Ovodonación"

    # ===========================
    # Recanalización
    # ===========================
    if recanalizacion_trompas:
        recomendaciones.append("✔️ Recanalización de trompas recomendada para reversión de ligadura tubárica en mujeres jóvenes (< 37 años) con buena longitud tubárica.")
        tecnica_sugerida = "Recanalización de Trompas"

    if not recomendaciones:
        recomendaciones.append("🔎 No se detectaron criterios claros para técnicas específicas. Se sugiere continuar con evaluación básica o control prenatal habitual.")

    return recomendaciones, tecnica_sugerida