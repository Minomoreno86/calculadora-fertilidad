# calculadora_fertilidad.py
from textos_clinicos import RECOMENDACIONES

class EvaluacionFertilidad:
    def __init__(self, edad, duracion_ciclo=None, imc=None, amh=None, prolactina=None, tsh=None, tpo_ab_positivo=False, 
                 insulina_ayunas=None, glicemia_ayunas=None, 
                 tiene_sop=False, grado_endometriosis=0, 
                 tiene_miomas=False, mioma_submucoso=False, mioma_submucoso_multiple=False, 
                 mioma_intramural_significativo=False, mioma_subseroso_grande=False,
                 tipo_adenomiosis="", tipo_polipo="", resultado_hsg="",
                 volumen_seminal=None, concentracion_esperm=None, motilidad_progresiva=None, morfologia_normal=None, vitalidad_esperm=None):
        
        self.edad, self.duracion_ciclo, self.imc, self.amh, self.prolactina, self.tsh, self.tpo_ab_positivo, self.insulina_ayunas, self.glicemia_ayunas, self.tiene_sop, self.grado_endometriosis, self.tipo_adenomiosis, self.tipo_polipo, self.resultado_hsg = edad, duracion_ciclo, imc, amh, prolactina, tsh, tpo_ab_positivo, insulina_ayunas, glicemia_ayunas, tiene_sop, grado_endometriosis, tipo_adenomiosis, tipo_polipo, resultado_hsg
        self.tiene_miomas, self.mioma_submucoso, self.mioma_submucoso_multiple, self.mioma_intramural_significativo, self.mioma_subseroso_grande = tiene_miomas, mioma_submucoso, mioma_submucoso_multiple, mioma_intramural_significativo, mioma_subseroso_grande
        self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm = volumen_seminal, concentracion_esperm, motilidad_progresiva, morfologia_normal, vitalidad_esperm

        self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, self.probabilidad_base_edad_num, self.comentario_imc, self.imc_factor, self.severidad_sop, self.comentario_sop, self.sop_factor, self.comentario_endometriosis, self.endometriosis_factor, self.comentario_miomas, self.mioma_factor, self.comentario_adenomiosis, self.adenomiosis_factor, self.comentario_polipo, self.polipo_factor, self.comentario_hsg, self.hsg_factor, self.diagnostico_reserva, self.recomendacion_reserva, self.amh_factor, self.diagnostico_masculino_detallado, self.male_factor, self.comentario_prolactina, self.prolactina_factor, self.comentario_tsh, self.tsh_factor, self.homa_calculado, self.comentario_homa, self.homa_factor = "", "", 0.0, "", 1.0, "No aplica", "", 1.0, "", 1.0, "", 1.0, "", 1.0, "", 1.0, "", 1.0, "Evaluación no realizada.", "", 1.0, "Normal o sin datos", 1.0, "", 1.0, "", 1.0, None, "", 1.0
        
        self.probabilidad_ajustada_final, self.datos_faltantes, self.recomendaciones_lista = "", [], []

    def _evaluar_potencial_por_edad(self):
        prob_num=0.0
        if self.edad >= 35 and self.edad <= 37: self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_35"])
        elif self.edad >= 38 and self.edad <= 40: self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_38"])
        elif self.edad >= 41 and self.edad <=42: self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_40"])
        elif self.edad >= 43: self.recomendaciones_lista.append(RECOMENDACIONES["EDAD_43"])
        if self.edad < 25: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Alta fertilidad", "25-30%", 27.5
        elif self.edad <= 29: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Fertilidad muy buena", "20-25%", 22.5
        elif self.edad <= 34: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Buena fertilidad", "15-20%", 17.5
        elif self.edad <= 37: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Fecundidad en descenso", "10-15%", 12.5
        elif self.edad <= 40: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Reducción significativa", "5-10%", 7.5
        elif self.edad <= 42: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Baja tasa de embarazo", "1-5%", 3.0
        else: self.diagnostico_potencial_edad, self.probabilidad_base_edad_str, prob_num = "Muy baja probabilidad", "<1%", 0.5
        self.probabilidad_base_edad_num = prob_num

    def _evaluar_imc(self):
        if self.imc is None: return
        if self.imc < 18.5: self.comentario_imc, self.imc_factor = "Bajo peso", 0.6; self.recomendaciones_lista.append(RECOMENDACIONES["IMC_BAJO"])
        elif self.imc <= 24.9: self.comentario_imc, self.imc_factor = "Peso normal", 1.0
        elif self.imc > 24.9: self.comentario_imc, self.imc_factor = "Sobrepeso/Obesidad", 0.85; self.recomendaciones_lista.append(RECOMENDACIONES["IMC_ALTO"])

    def _evaluar_sop(self):
        if not self.tiene_sop: return
        self.recomendaciones_lista.append(RECOMENDACIONES["SOP"])
        if self.imc is None or self.duracion_ciclo is None: self.severidad_sop, self.sop_factor = "Indeterminada", 0.6; return
        if self.imc < 25 and self.duracion_ciclo <= 45: self.severidad_sop, self.sop_factor = "Leve", 0.85
        elif self.imc <= 30 and self.duracion_ciclo > 45: self.severidad_sop, self.sop_factor = "Moderado", 0.6
        else: self.severidad_sop, self.sop_factor = "Severo", 0.4

    def _evaluar_endometriosis(self):
        if self.grado_endometriosis == 0: return
        if self.grado_endometriosis <= 2: self.comentario_endometriosis, self.endometriosis_factor = f"Grado {self.grado_endometriosis}", 0.8; self.recomendaciones_lista.append(RECOMENDACIONES["ENDO_LEVE"])
        else: self.comentario_endometriosis, self.endometriosis_factor = f"Grado {self.grado_endometriosis}", 0.4; self.recomendaciones_lista.append(RECOMENDACIONES["ENDO_SEVERA"])

    def _evaluar_miomatosis(self):
        if not self.tiene_miomas: return
        if self.mioma_submucoso: self.comentario_miomas, self.mioma_factor = "Miomatosis submucosa", 0.35; self.recomendaciones_lista.append(RECOMENDACIONES["MIOMA_SUBMUCOSO"])
        elif self.mioma_intramural_significativo: self.comentario_miomas, self.mioma_factor = "Miomatosis intramural significativa", 0.6; self.recomendaciones_lista.append(RECOMENDACIONES["MIOMA_INTRAMURAL"])
        elif self.mioma_subseroso_grande: self.comentario_miomas, self.mioma_factor = "Miomatosis subserosa grande", 0.85; self.recomendaciones_lista.append(RECOMENDACIONES["MIOMA_SUBSEROSO"])
        else: self.comentario_miomas, self.mioma_factor = "Miomatosis sin impacto cavitario", 1.0

    def _evaluar_adenomiosis(self):
        if not self.tipo_adenomiosis: return
        if self.tipo_adenomiosis == "focal": self.comentario_adenomiosis, self.adenomiosis_factor = "Adenomiosis Focal", 0.85; self.recomendaciones_lista.append(RECOMENDACIONES["ADENO_FOCAL"])
        else: self.comentario_adenomiosis, self.adenomiosis_factor = "Adenomiosis Difusa", 0.5; self.recomendaciones_lista.append(RECOMENDACIONES["ADENO_DIFUSA"])

    def _evaluar_polipos(self):
        if not self.tipo_polipo: return
        self.comentario_polipo, self.polipo_factor = "Pólipo(s) endometrial(es)", 0.7; self.recomendaciones_lista.append(RECOMENDACIONES["POLIPO"])

    def _evaluar_hsg(self):
        if not self.resultado_hsg: self.datos_faltantes.append("Resultado de Histerosalpingografía (HSG)"); return
        if self.resultado_hsg == "normal": self.comentario_hsg, self.hsg_factor = "Ambas trompas permeables", 1.0
        elif self.resultado_hsg == "unilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción tubárica unilateral", 0.7; self.recomendaciones_lista.append(RECOMENDACIONES["HSG_UNILATERAL"])
        elif self.resultado_hsg == "bilateral": self.comentario_hsg, self.hsg_factor = "Obstrucción tubárica bilateral", 0.0; self.recomendaciones_lista.append(RECOMENDACIONES["HSG_BILATERAL"])
        elif self.resultado_hsg == "defecto_uterino": self.comentario_hsg, self.hsg_factor = "Alteración de la cavidad uterina", 0.3; self.recomendaciones_lista.append(RECOMENDACIONES["HSG_DEFECTO"])

    def _evaluar_amh(self):
        """Evalúa la reserva ovárica y asigna un diagnóstico Y un factor de pronóstico."""
        if self.amh is None: 
            self.datos_faltantes.append("Hormona Antimülleriana (AMH)")
            return
        if self.amh > 4.0:
            self.diagnostico_reserva = "Alta Reserva Ovárica (sugestivo de SOP)"
            self.amh_factor = 0.9
        elif self.amh >= 1.5:
            self.diagnostico_reserva = "Reserva Ovárica Adecuada"
            self.amh_factor = 1.0
        elif self.amh >= 1.0:
            self.diagnostico_reserva = "Reserva Ovárica Levemente Disminuida"
            self.amh_factor = 0.85
            self.recomendaciones_lista.append(RECOMENDACIONES["AMH_BAJA"])
        elif self.amh >= 0.5:
            self.diagnostico_reserva = "Baja Reserva Ovárica"
            self.amh_factor = 0.6
            self.recomendaciones_lista.append(RECOMENDACIONES["AMH_BAJA"])
        else:
            self.diagnostico_reserva = "Reserva Ovárica Muy Baja"
            self.amh_factor = 0.3
            self.recomendaciones_lista.append(RECOMENDACIONES["AMH_BAJA"])
    
    def _evaluar_prolactina(self):
        if self.prolactina is None: self.datos_faltantes.append("Nivel de Prolactina"); return
        if self.prolactina >= 25: self.comentario_prolactina, self.prolactina_factor = "Hiperprolactinemia", 0.6; self.recomendaciones_lista.append(RECOMENDACIONES["PRL_ALTA"])
    
    def _evaluar_tsh(self):
        if self.tsh is None: self.datos_faltantes.append("Nivel de TSH"); return
        if self.tsh > 2.5: self.comentario_tsh, self.tsh_factor = "Función tiroidea no óptima", 0.7; self.recomendaciones_lista.append(RECOMENDACIONES["TSH_ALTA"])
        if self.tpo_ab_positivo: self.recomendaciones_lista.append(RECOMENDACIONES["TPO_POSITIVO"])
    
    def _evaluar_indice_homa(self):
        if self.insulina_ayunas is None or self.glicemia_ayunas is None: self.datos_faltantes.append("Índice HOMA"); return
        self.homa_calculado = (self.insulina_ayunas * self.glicemia_ayunas) / 405
        if self.homa_calculado >= 2.5: self.comentario_homa, self.homa_factor = "Resistencia a la insulina", 0.8; self.recomendaciones_lista.append(RECOMENDACIONES["HOMA_ALTO"])
    
    def _evaluar_factor_masculino(self):
        alteraciones = []
        if all(p is None for p in [self.volumen_seminal, self.concentracion_esperm, self.motilidad_progresiva, self.morfologia_normal, self.vitalidad_esperm]): self.datos_faltantes.append("Espermatograma completo"); return
        if self.concentracion_esperm == 0: alteraciones.append((0.1, "Azoospermia"))
        else:
            if self.concentracion_esperm is not None and self.concentracion_esperm < 15: alteraciones.append((0.7, "Oligozoospermia"))
            if self.motilidad_progresiva is not None and self.motilidad_progresiva < 32: alteraciones.append((0.85, "Astenozoospermia"))
            if self.morfologia_normal is not None and self.morfologia_normal < 4: alteraciones.append((0.5, "Teratozoospermia"))
            if self.vitalidad_esperm is not None and self.vitalidad_esperm < 58: alteraciones.append((0.3, "Necrozoospermia"))
        if self.volumen_seminal is not None and self.volumen_seminal < 1.5: alteraciones.append((0.85, "Hipospermia"))
        if alteraciones:
            alteracion_principal = min(alteraciones, key=lambda item: item[0])
            self.male_factor = alteracion_principal[0]
            self.diagnostico_masculino_detallado = ", ".join([item[1] for item in alteraciones])
            self.recomendaciones_lista.append(RECOMENDACIONES["FACTOR_MASCULINO"])
        else: self.diagnostico_masculino_detallado = "Parámetros dentro de la normalidad."

    def ejecutar_evaluacion(self):
        metodos_evaluacion = [self._evaluar_potencial_por_edad, self._evaluar_imc, self._evaluar_sop, self._evaluar_endometriosis, self._evaluar_miomatosis, self._evaluar_adenomiosis, self._evaluar_polipos, self._evaluar_hsg, self._evaluar_amh, self._evaluar_prolactina, self._evaluar_tsh, self._evaluar_indice_homa, self._evaluar_factor_masculino]
        for metodo in metodos_evaluacion:
            metodo()
        
        prob_ajustada = (self.probabilidad_base_edad_num * self.imc_factor * self.sop_factor * self.endometriosis_factor * self.mioma_factor * self.adenomiosis_factor * self.polipo_factor * self.hsg_factor *
                         self.amh_factor *
                         self.prolactina_factor * self.tsh_factor * self.homa_factor * self.male_factor)
                         
        self.probabilidad_ajustada_final = f"{prob_ajustada:.1f}%"


if __name__ == "__main__":
    print("--- Evaluación de Fertilidad de Pareja v16 (Refactorizado con Recomendaciones) ---")
    print("\n--- Datos Femeninos ---")
    edad_str = input("Introduce la edad de la paciente: ")
    sop_str = input("¿Tiene diagnóstico de SOP? (si/no): ")
    ciclo_str = input("Introduce la duración promedio de su ciclo en días (ej: 30): ")
    imc_str = input("Introduce el IMC (kg/m²) (deja en blanco si no lo tienes): ")

    print("\n--- Datos Ginecológicos y Anatómicos Femeninos ---")
    endo_str = input("¿Tiene diagnóstico de endometriosis? (si/no): ")
    grado_endo = 0
    if endo_str.lower() == 'si':
        grado_str = input(" 	↳ ¿Qué grado (1, 2, 3 o 4)?: ")
        grado_endo = int(grado_str) if grado_str in ['1','2','3','4'] else 0

    tiene_miomas_input = input("¿Tiene diagnóstico de miomatosis uterina? (si/no): ")
    miomas_args = {'tiene_miomas': False, 'mioma_submucoso': False, 'mioma_submucoso_multiple': False, 'mioma_intramural_significativo': False, 'mioma_subseroso_grande': False}
    if tiene_miomas_input.lower() == 'si':
        miomas_args['tiene_miomas'] = True
        submucoso_input = input(" 	↳ ¿Existen miomas SUBMUCOSOS (dentro de la cavidad)? (si/no): ")
        if submucoso_input.lower() == 'si':
            miomas_args['mioma_submucoso'] = True
            multiple_input = input(" 	 	↳ ¿Son múltiples? (si/no): ")
            miomas_args['mioma_submucoso_multiple'] = (multiple_input.lower() == 'si')
        else:
            intramural_input = input(" 	↳ ¿Existen miomas INTRAMURALES que deforman la cavidad o miden 4cm o más? (si/no): ")
            miomas_args['mioma_intramural_significativo'] = (intramural_input.lower() == 'si')
            subseroso_input = input(" 	↳ ¿Existen miomas SUBSEROSOS grandes (mayores de 6cm)? (si/no): ")
            miomas_args['mioma_subseroso_grande'] = (subseroso_input.lower() == 'si')

    adenomiosis_args = {'tipo_adenomiosis': ''}
    tiene_adenomiosis_input = input("¿Tiene diagnóstico de adenomiosis? (si/no): ")
    if tiene_adenomiosis_input.lower() == 'si':
        tipo_adeno_str = input(" 	↳ ¿Qué tipo? (1: Focal, 2: Difusa Leve, 3: Difusa Severa): ")
        if tipo_adeno_str == '1': adenomiosis_args['tipo_adenomiosis'] = 'focal'
        elif tipo_adeno_str == '2': adenomiosis_args['tipo_adenomiosis'] = 'difusa_leve'
        elif tipo_adeno_str == '3': adenomiosis_args['tipo_adenomiosis'] = 'difusa_severa'

    polipo_args = {'tipo_polipo': ''}
    tiene_polipo_input = input("¿Tiene diagnóstico de pólipos endometriales? (si/no): ")
    if tiene_polipo_input.lower() == 'si':
        tipo_polipo_str = input(" 	↳ ¿Qué tipo? (1: Pólipo único < 1cm, 2: Pólipo 1-2cm o múltiples pequeños, 3: Pólipo > 2cm o múltiples grandes): ")
        if tipo_polipo_str == '1': polipo_args['tipo_polipo'] = 'pequeno_unico'
        elif tipo_polipo_str == '2': polipo_args['tipo_polipo'] = 'moderado_multiple'
        elif tipo_polipo_str == '3': polipo_args['tipo_polipo'] = 'grande'

    hsg_args = {'resultado_hsg': ''}
    tiene_hsg_input = input("¿Tiene un resultado de Histerosalpingografía (HSG)? (si/no): ")
    if tiene_hsg_input.lower() == 'si':
        tipo_hsg_str = input(" 	↳ ¿Cuál fue el resultado? (1: Normal, 2: Obstrucción Unilateral, 3: Obstrucción Bilateral, 4: Defecto Uterino): ")
        if tipo_hsg_str == '1': hsg_args['resultado_hsg'] = 'normal'
        elif tipo_hsg_str == '2': hsg_args['resultado_hsg'] = 'unilateral'
        elif tipo_hsg_str == '3': hsg_args['resultado_hsg'] = 'bilateral'
        elif tipo_hsg_str == '4': hsg_args['resultado_hsg'] = 'defecto_uterino'

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

    try:
        evaluacion = EvaluacionFertilidad(
            edad=int(edad_str) if edad_str else 30,
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
        evaluacion.ejecutar_evaluacion()
        
        print("\n" + "="*15 + " INFORME DE FERTILIDAD DE PAREJA " + "="*15)
        print("\n--- 1. Pronóstico de Concepción por Ciclo ---")
        factores_ginecologicos = evaluacion.imc_factor * evaluacion.sop_factor * evaluacion.endometriosis_factor * evaluacion.mioma_factor * evaluacion.adenomiosis_factor * evaluacion.polipo_factor * evaluacion.hsg_factor
        factores_endocrinos = evaluacion.prolactina_factor * evaluacion.tsh_factor * evaluacion.homa_factor * evaluacion.amh_factor
        print(f"Probabilidad basal (por edad femenina): {evaluacion.probabilidad_base_edad_num}%")
        print(f" 	x Factores Gineco-Anatómicos (IMC, SOP, Uterinos, HSG): {factores_ginecologicos:.2f}")
        print(f" 	x Factores Endocrino-Metabólicos (PRL, TSH, HOMA, AMH): {factores_endocrinos:.2f}")
        print(f" 	x Factor Masculino: {evaluacion.male_factor:.2f}")
        print("-" * 52)
        print(f"PRONÓSTICO DE PAREJA AJUSTADO PARA ESTE CICLO: {evaluacion.probabilidad_ajustada_final}")
        print("-" * 52)

        print("\n--- 2. Análisis Detallado de Factores ---")
        print("Femeninos:")
        print(f" 	- Edad ({evaluacion.edad} años): {evaluacion.diagnostico_potencial_edad}")
        if evaluacion.imc: print(f" 	- IMC ({evaluacion.imc} kg/m²): {evaluacion.comentario_imc}")
        if evaluacion.tiene_sop: print(f" 	- SOP: {evaluacion.severidad_sop}")
        if evaluacion.grado_endometriosis > 0: print(f" 	- Endometriosis: {evaluacion.comentario_endometriosis}")
        if evaluacion.tiene_miomas: print(f" 	- Miomatosis Uterina: {evaluacion.comentario_miomas}")
        if evaluacion.tipo_adenomiosis: print(f" 	- Adenomiosis: {evaluacion.comentario_adenomiosis}")
        if evaluacion.tipo_polipo: print(f" 	- Pólipos Endometriales: {evaluacion.comentario_polipo}")
        if evaluacion.resultado_hsg: print(f" 	- Histerosalpingografía (HSG): {evaluacion.comentario_hsg}")
        if evaluacion.amh: print(f" 	- Reserva Ovárica (AMH): {evaluacion.diagnostico_reserva}")
        if evaluacion.prolactina: print(f" 	- Prolactina: {evaluacion.comentario_prolactina}")
        if evaluacion.tsh: print(f" 	- Función Tiroidea (TSH): {evaluacion.comentario_tsh}")
        if evaluacion.homa_calculado: print(f" 	- Resistencia a Insulina (HOMA: {evaluacion.homa_calculado:.2f}): {evaluacion.comentario_homa}")
        
        print("Masculinos:")
        print(f" 	- Espermatograma: {evaluacion.diagnostico_masculino_detallado}")

        if evaluacion.datos_faltantes:
            print("\n" + "-"*40)
            print("Para una evaluación más precisa, se recomienda proporcionar:")
            for dato in evaluacion.datos_faltantes: print(f"- {dato}")

        if evaluacion.recomendaciones_lista:
            recomendaciones_unicas = list(set(evaluacion.recomendaciones_lista))
            print("\n--- 3. PLAN DE ACCIÓN Y RECOMENDACIONES ---")
            for i, rec in enumerate(recomendaciones_unicas, 1):
                print(f" 	{i}. {rec}")

        print("\n" + "="*52)

    except ValueError:
        print("\nError: Todos los datos numéricos deben ser válidos.")
    except Exception as e:
        print(f"\nHa ocurrido un error inesperado: {e}")