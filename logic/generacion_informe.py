from config import BENCHMARK_PRONOSTICO_POR_EDAD, CLINICAL_INSIGHTS
from textos_clinicos import RECOMENDACIONES

def generar_textos_pronostico(evaluacion):
    """Genera los textos principales del pronóstico, con manejo especial para OTB."""
    if evaluacion.otb_factor == 0.0:
        evaluacion.pronostico_categoria = "REQUIERE TRATAMIENTO"
        evaluacion.pronostico_emoji = "🔴"
        evaluacion.pronostico_frase = (
            "El embarazo espontáneo no es posible debido a la ligadura de trompas (OTB). "
            "Consulta la sección de recomendaciones para ver el tratamiento sugerido en tu caso."
        )
        return
        
    pronostico_str = evaluacion.probabilidad_ajustada_final 
    if evaluacion.pronostico_numerico >= 15:
        evaluacion.pronostico_categoria, evaluacion.pronostico_emoji, evaluacion.pronostico_frase = "BUENO", "🟢", f"¡Tu pronóstico de concepción espontánea por ciclo es BUENO ({pronostico_str})!"
    elif evaluacion.pronostico_numerico >= 5:
        evaluacion.pronostico_categoria, evaluacion.pronostico_emoji, evaluacion.pronostico_frase = "MODERADO", "🟡", f"Tu pronóstico es MODERADO ({pronostico_str}). Hay factores que se pueden optimizar."
    else:
        evaluacion.pronostico_categoria, evaluacion.pronostico_emoji, evaluacion.pronostico_frase = "BAJO", "🔴", f"Tu pronóstico es BAJO ({pronostico_str}). Se recomienda una evaluación por un especialista."

def generar_comparativa_benchmark(evaluacion):
    """Compara el resultado del usuario con el promedio de su grupo de edad."""
    if evaluacion.otb_factor == 0.0: evaluacion.benchmark_frase = "No aplica por OTB."; return
    if evaluacion.edad < 30: rango_edad = "Menos de 30"
    elif evaluacion.edad <= 34: rango_edad = "30-34"
    elif evaluacion.edad <= 37: rango_edad = "35-37"
    elif evaluacion.edad <= 40: rango_edad = "38-40"
    else: rango_edad = "Más de 40"
    
    benchmark_valor = BENCHMARK_PRONOSTICO_POR_EDAD.get(rango_edad, {}).get("mensual", 0.0)
    diferencia = evaluacion.pronostico_numerico - benchmark_valor
    
    if diferencia > 2: comparativa = "notablemente superior al promedio"
    elif diferencia < -2: comparativa = "notablemente inferior al promedio"
    else: comparativa = "similar al promedio"
    
    evaluacion.benchmark_frase = f"Tu resultado es **{comparativa}** para tu grupo de edad ({rango_edad} años), cuyo pronóstico base es del {benchmark_valor:.1f}%."

def recopilar_insights_clinicos(evaluacion):
    """Recopila recomendaciones y textos de ayuda basados en los hallazgos."""
    if evaluacion.imc_factor != 1.0: evaluacion.recomendaciones_lista.append(RECOMENDACIONES.get("IMC_ANORMAL", "Optimizar el peso puede mejorar la fertilidad."))
    if evaluacion.ciclo_factor != 1.0: evaluacion.recomendaciones_lista.append(RECOMENDACIONES.get("CICLO_IRREGULAR", "Estudiar la causa de los ciclos irregulares es importante."))
    if evaluacion.tiene_sop: evaluacion.recomendaciones_lista.append(RECOMENDACIONES.get("SOP", "El manejo integral del SOP es clave."))
    
    if evaluacion.tiene_sop: evaluacion.insights_clinicos.append(CLINICAL_INSIGHTS.get("SOP", "El SOP es un factor clave en tu perfil."))
    if evaluacion.grado_endometriosis > 0: evaluacion.insights_clinicos.append(CLINICAL_INSIGHTS.get("ENDOMETRIOSIS", "La endometriosis está afectando tu pronóstico."))
    if evaluacion.mioma_submucoso: evaluacion.insights_clinicos.append(CLINICAL_INSIGHTS.get("MIOMA_SUBMUCOSO", "El mioma submucoso requiere atención prioritaria."))
    if evaluacion.amh is not None and evaluacion.amh < 1.0: evaluacion.insights_clinicos.append(CLINICAL_INSIGHTS.get("AMH_BAJA", "La reserva ovárica es un factor a considerar."))
    if evaluacion.male_factor < 1.0: evaluacion.insights_clinicos.append(CLINICAL_INSIGHTS.get("FACTOR_MASCULINO", "El factor masculino juega un rol importante."))