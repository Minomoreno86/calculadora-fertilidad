# --- FASE DE INTERACCIÓN (Este es el bloque que faltaba) ---

print("--- Evaluación de Fertilidad de Pareja v15 (con HSG - Motor Completo) ---")

# --- Datos Femeninos ---
print("\n--- Datos Ginecológicos y Anatómicos Femeninos ---")
edad_str = input("Introduce la edad de la paciente: ")
sop_str = input("¿Tiene diagnóstico de SOP? (si/no): ")
ciclo_str = input("Introduce la duración promedio de su ciclo en días (ej: 30): ")
imc_str = input("Introduce el IMC (kg/m²) (deja en blanco si no lo tienes): ")

# --- Bloque para Endometriosis ---
endo_str = input("¿Tiene diagnóstico de endometriosis? (si/no): ")
grado_endo = 0
if endo_str.lower() == 'si':
    grado_str = input("  ↳ ¿Qué grado (1, 2, 3 o 4)?: ")
    grado_endo = int(grado_str) if grado_str in ['1','2','3','4'] else 0

# --- Bloque para Miomatosis ---
tiene_miomas_input = input("¿Tiene diagnóstico de miomatosis uterina? (si/no): ")
miomas_args = {'tiene_miomas': False, 'mioma_submucoso': False, 'mioma_submucoso_multiple': False, 'mioma_intramural_significativo': False, 'mioma_subseroso_grande': False}
if tiene_miomas_input.lower() == 'si':
    miomas_args['tiene_miomas'] = True
    submucoso_input = input("  ↳ ¿Existen miomas SUBMUCOSOS (dentro de la cavidad)? (si/no): ")
    if submucoso_input.lower() == 'si':
        miomas_args['mioma_submucoso'] = True
        multiple_input = input("    ↳ ¿Son múltiples? (si/no): ")
        miomas_args['mioma_submucoso_multiple'] = (multiple_input.lower() == 'si')
    else:
        intramural_input = input("  ↳ ¿Existen miomas INTRAMURALES que deforman la cavidad o miden 4cm o más? (si/no): ")
        miomas_args['mioma_intramural_significativo'] = (intramural_input.lower() == 'si')
        subseroso_input = input("  ↳ ¿Existen miomas SUBSEROSOS grandes (mayores de 6cm)? (si/no): ")
        miomas_args['mioma_subseroso_grande'] = (subseroso_input.lower() == 'si')

# --- Bloque para Adenomiosis ---
adenomiosis_args = {'tipo_adenomiosis': ''}
tiene_adenomiosis_input = input("¿Tiene diagnóstico de adenomiosis? (si/no): ")
if tiene_adenomiosis_input.lower() == 'si':
    tipo_adeno_str = input("  ↳ ¿Qué tipo? (1: Focal, 2: Difusa Leve, 3: Difusa Severa): ")
    if tipo_adeno_str == '1': adenomiosis_args['tipo_adenomiosis'] = 'focal'
    elif tipo_adeno_str == '2': adenomiosis_args['tipo_adenomiosis'] = 'difusa_leve'
    elif tipo_adeno_str == '3': adenomiosis_args['tipo_adenomiosis'] = 'difusa_severa'

# --- Bloque para Pólipos ---
polipo_args = {'tipo_polipo': ''}
tiene_polipo_input = input("¿Tiene diagnóstico de pólipos endometriales? (si/no): ")
if tiene_polipo_input.lower() == 'si':
    tipo_polipo_str = input("  ↳ ¿Qué tipo? (1: Pólipo único < 1cm, 2: Pólipo 1-2cm o múltiples pequeños, 3: Pólipo > 2cm o múltiples grandes): ")
    if tipo_polipo_str == '1': polipo_args['tipo_polipo'] = 'pequeno_unico'
    elif tipo_polipo_str == '2': polipo_args['tipo_polipo'] = 'moderado_multiple'
    elif tipo_polipo_str == '3': polipo_args['tipo_polipo'] = 'grande'

# --- Bloque para HSG ---
hsg_args = {'resultado_hsg': ''}
tiene_hsg_input = input("¿Tiene un resultado de Histerosalpingografía (HSG)? (si/no): ")
if tiene_hsg_input.lower() == 'si':
    tipo_hsg_str = input("  ↳ ¿Cuál fue el resultado? (1: Normal, 2: Obstrucción Unilateral, 3: Obstrucción Bilateral, 4: Defecto Uterino): ")
    if tipo_hsg_str == '1': hsg_args['resultado_hsg'] = 'normal'
    elif tipo_hsg_str == '2': hsg_args['resultado_hsg'] = 'unilateral'
    elif tipo_hsg_str == '3': hsg_args['resultado_hsg'] = 'bilateral'
    elif tipo_hsg_str == '4': hsg_args['resultado_hsg'] = 'defecto_uterino'

# --- Datos Endocrinológicos ---
print("\n--- Datos Endocrinológicos Femeninos ---")
amh_str = input("Nivel de AMH (ng/mL): ")
prl_str = input("Nivel de Prolactina (ng/mL): ")
tsh_str = input("Nivel de TSH (µUI/mL): ")
tpo_str = "no"
if tsh_str and float(tsh_str) > 2.5:
    tpo_str = input("¿Tiene anticuerpos antitiroideos (TPO-Ab) positivos? (si/no): ")
print("\n--- Perfil Metabólico (para Índice HOMA) ---")
insulina_str = input("Insulina en ayunas (μU/mL): ")
glicemia_str = input("Glicemia en ayunas (mg/dL): ")

# --- Datos Masculinos ---
print("\n--- Datos Masculinos ---")
tiene_esperma_str = input("¿La pareja tiene un análisis de espermatograma? (si/no): ")
vol_str, conc_str, mot_str, morf_str, vit_str = [None]*5
if tiene_esperma_str.lower() == 'si':
    print("\n--- Detalle del Espermatograma ---")
    vol_str = input("Volumen (mL): ")
    conc_str = input("Concentración (millones/mL): ")
    mot_str = input("Motilidad progresiva (%): ")
    morf_str = input("Morfología normal (%): ")
    vit_str = input("Vitalidad (%): ")

# --- Bloque de Ejecución y Reporte ---
try:
    # Creamos la instancia de la clase con todos los datos recolectados
    evaluacion = EvaluacionFertilidad(
        edad=int(edad_str) if edad_str else 0,
        duracion_ciclo=int(ciclo_str) if ciclo_str else None,
        imc=float(imc_str) if imc_str else None,
        amh=float(amh_str) if amh_str else None,
        prolactina=float(prl_str) if prl_str else None,
        tsh=float(tsh_str) if tsh_str else None,
        tpo_ab_positivo=(tpo_str.lower() == 'si'),
        insulina_ayunas=float(insulina_str) if insulina_str else None,
        glicemia_ayunas=float(glicemia_str) if glicemia_str else None,
        tiene_sop=(sop_str.lower() == 'si'),
        grado_endometriosis=grado_endo,
        **miomas_args,
        **adenomiosis_args,
        **polipo_args,
        **hsg_args,
        volumen_seminal=float(vol_str) if vol_str else None,
        concentracion_esperm=float(conc_str) if conc_str else None,
        motilidad_progresiva=float(mot_str) if mot_str else None,
        morfologia_normal=float(morf_str) if morf_str else None,
        vitalidad_esperm=float(vit_str) if vit_str else None
    )

    # Le damos la orden de "cocinar"
    evaluacion.ejecutar_evaluacion()
    
    # Imprimimos el resultado
    print("\n" + "="*15 + " INFORME DE FERTILIDAD DE PAREJA " + "="*15)
    print("\n--- 1. Pronóstico de Concepción por Ciclo ---")
    factores_ginecologicos = evaluacion.imc_factor * evaluacion.sop_factor * evaluacion.endometriosis_factor * evaluacion.mioma_factor * evaluacion.adenomiosis_factor * evaluacion.polipo_factor * evaluacion.hsg_factor
    factores_endocrinos = evaluacion.prolactina_factor * evaluacion.tsh_factor * evaluacion.homa_factor
    print(f"Probabilidad basal (por edad femenina): {evaluacion.probabilidad_base_edad_num}%")
    print(f"  x Factores Gineco-Anatómicos (IMC, SOP, Uterinos, HSG): {factores_ginecologicos:.2f}")
    print(f"  x Factores Endocrino-Metabólicos (PRL, TSH, HOMA): {factores_endocrinos:.2f}")
    print(f"  x Factor Masculino: {evaluacion.male_factor:.2f}")
    print("-" * 52)
    print(f"PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO: {evaluacion.probabilidad_ajustada_final}")
    print("-" * 52)

    print("\n--- 2. Análisis Detallado de Factores ---")
    print("Femeninos:")
    print(f"  - Edad ({evaluacion.edad} años): {evaluacion.diagnostico_potencial_edad}")
    if evaluacion.imc: print(f"  - IMC ({evaluacion.imc} kg/m²): {evaluacion.comentario_imc}")
    if evaluacion.tiene_sop: print(f"  - SOP: {evaluacion.severidad_sop}")
    if evaluacion.grado_endometriosis > 0: print(f"  - Endometriosis: {evaluacion.comentario_endometriosis}")
    if evaluacion.tiene_miomas: print(f"  - Miomatosis Uterina: {evaluacion.comentario_miomas}")
    if evaluacion.tipo_adenomiosis: print(f"  - Adenomiosis: {evaluacion.comentario_adenomiosis}")
    if evaluacion.tipo_polipo: print(f"  - Pólipos Endometriales: {evaluacion.comentario_polipo}")
    if evaluacion.resultado_hsg: print(f"  - Histerosalpingografía (HSG): {evaluacion.comentario_hsg}")
    print(f"  - Reserva Ovárica (AMH): {evaluacion.diagnostico_reserva}")
    if evaluacion.prolactina: print(f"  - Prolactina: {evaluacion.comentario_prolactina}")
    if evaluacion.tsh: print(f"  - Función Tiroidea (TSH): {evaluacion.comentario_tsh}")
    if evaluacion.homa_calculado: print(f"  - Resistencia a Insulina (HOMA: {evaluacion.homa_calculado:.2f}): {evaluacion.comentario_homa}")
    
    print("Masculinos:")
    print(f"  - Espermatograma: {evaluacion.diagnostico_masculino_detallado}")

    if evaluacion.datos_faltantes:
        print("\n" + "-"*40)
        print("Para una evaluación más precisa, se recomienda proporcionar:")
        for dato in evaluacion.datos_faltantes: print(f"- {dato}")
    print("\n" + "="*52)

except ValueError:
    print("\nError: Todos los datos numéricos deben ser válidos.")
except Exception as e:
    print(f"\nHa ocurrido un error inesperado: {e}")