# Contenido para: logic/evaluacion_factores.py
from textos_clinicos import RECOMENDACIONES
def evaluar_potencial_por_edad(evaluacion):
    if evaluacion.edad < 30: evaluacion.diagnostico_potencial_edad, evaluacion.probabilidad_base_edad_num = "Fertilidad muy buena", 22.5
    elif evaluacion.edad <= 34: evaluacion.diagnostico_potencial_edad, evaluacion.probabilidad_base_edad_num = "Buena fertilidad", 17.5
    elif evaluacion.edad <= 37: evaluacion.diagnostico_potencial_edad, evaluacion.probabilidad_base_edad_num = "Fecundidad en descenso", 12.5
    elif evaluacion.edad <= 40: evaluacion.diagnostico_potencial_edad, evaluacion.probabilidad_base_edad_num = "Reducción significativa", 7.5
    elif evaluacion.edad <= 42: evaluacion.diagnostico_potencial_edad, evaluacion.probabilidad_base_edad_num = "Baja tasa de embarazo", 3.0
    else: evaluacion.diagnostico_potencial_edad, evaluacion.probabilidad_base_edad_num = "Probabilidad casi nula", 0.1

def evaluar_imc(evaluacion):
    if evaluacion.imc is None: return
    if evaluacion.imc < 18.5: evaluacion.comentario_imc, evaluacion.imc_factor = "Bajo peso", 0.6
    elif evaluacion.imc <= 24.9: evaluacion.comentario_imc, evaluacion.imc_factor = "Peso normal", 1.0
    else: evaluacion.comentario_imc, evaluacion.imc_factor = "Sobrepeso/Obesidad", 0.85

def evaluar_ciclo_menstrual(evaluacion):
    if evaluacion.duracion_ciclo is None: evaluacion.datos_faltantes.append("Duración del ciclo menstrual"); return
    if 21 <= evaluacion.duracion_ciclo <= 35: evaluacion.comentario_ciclo, evaluacion.ciclo_factor = "Ciclo regular", 1.0
    else: evaluacion.comentario_ciclo, evaluacion.ciclo_factor = "Ciclo irregular", 0.6

def evaluar_sop(evaluacion):
    if not evaluacion.tiene_sop: return
    if evaluacion.imc is None or evaluacion.duracion_ciclo is None: evaluacion.severidad_sop, evaluacion.sop_factor = "Indeterminada", 0.6; return
    if evaluacion.imc < 25 and evaluacion.duracion_ciclo <= 45: evaluacion.severidad_sop, evaluacion.sop_factor = "Leve", 0.85
    elif evaluacion.imc <= 30 and evaluacion.duracion_ciclo > 45: evaluacion.severidad_sop, evaluacion.sop_factor = "Moderado", 0.6
    else: evaluacion.severidad_sop, evaluacion.sop_factor = "Severo", 0.4

def evaluar_endometriosis(evaluacion):
    if evaluacion.grado_endometriosis == 0: return
    evaluacion.comentario_endometriosis = f"Grado {evaluacion.grado_endometriosis}"
    if evaluacion.grado_endometriosis <= 2: evaluacion.endometriosis_factor = 0.8
    else: evaluacion.endometriosis_factor = 0.4

def evaluar_miomatosis(evaluacion):
    if not evaluacion.tiene_miomas: return
    if evaluacion.mioma_submucoso: evaluacion.comentario_miomas, evaluacion.mioma_factor = "Submucoso", 0.35
    elif evaluacion.mioma_intramural_significativo: evaluacion.comentario_miomas, evaluacion.mioma_factor = "Intramural significativo", 0.6
    elif evaluacion.mioma_subseroso_grande: evaluacion.comentario_miomas, evaluacion.mioma_factor = "Subseroso grande", 0.85
    else: evaluacion.comentario_miomas, evaluacion.mioma_factor = "Sin impacto cavitario", 1.0

def evaluar_adenomiosis(evaluacion):
    if not evaluacion.tipo_adenomiosis: return
    if evaluacion.tipo_adenomiosis == "focal": evaluacion.comentario_adenomiosis, evaluacion.adenomiosis_factor = "Focal", 0.85
    else: evaluacion.comentario_adenomiosis, evaluacion.adenomiosis_factor = "Difusa", 0.5

def evaluar_polipos(evaluacion):
    if not evaluacion.tipo_polipo: return
    evaluacion.comentario_polipo, evaluacion.polipo_factor = "Pólipo(s) endometrial(es)", 0.7

def evaluar_hsg(evaluacion):
    if not evaluacion.resultado_hsg: evaluacion.datos_faltantes.append("Resultado de HSG"); return
    if evaluacion.resultado_hsg == "normal": evaluacion.comentario_hsg, evaluacion.hsg_factor = "Ambas trompas permeables", 1.0
    elif evaluacion.resultado_hsg == "unilateral": evaluacion.comentario_hsg, evaluacion.hsg_factor = "Obstrucción unilateral", 0.7
    elif evaluacion.resultado_hsg == "bilateral": evaluacion.comentario_hsg, evaluacion.hsg_factor = "Obstrucción bilateral", 0.0
    elif evaluacion.resultado_hsg == "defecto_uterino": evaluacion.comentario_hsg, evaluacion.hsg_factor = "Alteración cavidad uterina", 0.3

def evaluar_otb(evaluacion):
    if evaluacion.tiene_otb:
        evaluacion.otb_factor = 0.0

def evaluar_amh(evaluacion):
    if evaluacion.amh is None: evaluacion.datos_faltantes.append("Hormona Antimülleriana (AMH)"); return
    if evaluacion.amh > 4.0: evaluacion.diagnostico_reserva, evaluacion.amh_factor = "Alta (sugestivo de SOP)", 0.9
    elif evaluacion.amh >= 1.5: evaluacion.diagnostico_reserva, evaluacion.amh_factor = "Adecuada", 1.0
    elif evaluacion.amh >= 1.0: evaluacion.diagnostico_reserva, evaluacion.amh_factor = "Levemente disminuida", 0.85
    elif evaluacion.amh >= 0.5: evaluacion.diagnostico_reserva, evaluacion.amh_factor = "Baja", 0.6
    else: evaluacion.diagnostico_reserva, evaluacion.amh_factor = "Muy baja", 0.3

def evaluar_prolactina(evaluacion):
    if evaluacion.prolactina is None: evaluacion.datos_faltantes.append("Nivel de Prolactina"); return
    if evaluacion.prolactina >= 25: evaluacion.comentario_prolactina, evaluacion.prolactina_factor = "Hiperprolactinemia", 0.6

def evaluar_tsh(evaluacion):
    if evaluacion.tsh is None: evaluacion.datos_faltantes.append("Nivel de TSH"); return
    if evaluacion.tsh > 2.5: evaluacion.comentario_tsh, evaluacion.tsh_factor = "No óptima para fertilidad", 0.7

def evaluar_indice_homa(evaluacion):
    if evaluacion.insulina_ayunas is None or evaluacion.glicemia_ayunas is None: evaluacion.datos_faltantes.append("Índice HOMA"); return
    evaluacion.homa_calculado = (evaluacion.insulina_ayunas * evaluacion.glicemia_ayunas) / 405
    if evaluacion.homa_calculado >= 2.5: evaluacion.comentario_homa, evaluacion.homa_factor = "Resistencia a la insulina", 0.8

def evaluar_factor_masculino(evaluacion):
    if all(p is None for p in [evaluacion.volumen_seminal, evaluacion.concentracion_esperm, evaluacion.motilidad_progresiva, evaluacion.morfologia_normal, evaluacion.vitalidad_esperm]): evaluacion.datos_faltantes.append("Espermatograma completo"); return
    alteraciones = []
    if evaluacion.concentracion_esperm == 0: alteraciones.append((0.0, "Azoospermia"))
    else:
        if evaluacion.concentracion_esperm is not None and evaluacion.concentracion_esperm < 15: alteraciones.append((0.7, "Oligozoospermia"))
        if evaluacion.motilidad_progresiva is not None and evaluacion.motilidad_progresiva < 32: alteraciones.append((0.85, "Astenozoospermia"))
        if evaluacion.morfologia_normal is not None and evaluacion.morfologia_normal < 4: alteraciones.append((0.5, "Teratozoospermia"))
        if evaluacion.vitalidad_esperm is not None and evaluacion.vitalidad_esperm < 58: alteraciones.append((0.3, "Necrozoospermia"))
    if evaluacion.volumen_seminal is not None and evaluacion.volumen_seminal < 1.5: alteraciones.append((0.85, "Hipospermia"))
    
    if alteraciones:
        evaluacion.male_factor = min(alteraciones, key=lambda item: item[0])[0]
        evaluacion.diagnostico_masculino_detallado = ", ".join([item[1] for item in alteraciones])
    else:
        evaluacion.diagnostico_masculino_detallado = "Parámetros normales"