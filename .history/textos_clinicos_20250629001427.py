# textos_clinicos.py
# Este archivo funciona como un 'almacén' central para todos los textos de la aplicación.
# Facilita la modificación de los textos sin tocar la lógica principal.

RECOMENDACIONES = {
    # EDAD
    "EDAD_35": "Edad >35a: No demorar la consulta especializada si no hay embarazo en 6 meses.",
    "EDAD_38": "Edad >38a: Se recomienda una evaluación temprana por un especialista en fertilidad.",
    "EDAD_40": "Edad >40a: Valorar opciones de reproducción asistida como vía principal.",
    "EDAD_43": "Edad >43a: Las opciones con óvulos propios son muy limitadas; considerar seriamente la ovodonación.",

    # IMC
    "IMC_BAJO": "IMC: Optimizar la nutrición para alcanzar un peso saludable (IMC > 18.5) y regularizar la ovulación.",
    "IMC_ALTO": "IMC: Iniciar un plan de dieta y ejercicio. Una pérdida del 5-10% del peso corporal puede mejorar significativamente la fertilidad.",

    # SOP
    "SOP": "SOP: Consultar sobre inducción de la ovulación (ej. Letrozol) como tratamiento de primera línea.",

    # ENDOMETRIOSIS
    "ENDO_LEVE": "Endometriosis Grado I-II: Puede intentarse concepción espontánea/dirigida. Valorar tratamiento si no hay éxito.",
    "ENDO_SEVERA": "Endometriosis Grado III-IV: Se recomienda valoración directa para Fertilización In Vitro (FIV).",

    # MIOMAS
    "MIOMA_SUBMUCOSO": "Mioma Submucoso: Se recomienda resección por histeroscopia para mejorar la implantación.",
    "MIOMA_INTRAMURAL": "Mioma Intramural Significativo: Discutir con su médico la opción de miomectomía según el caso.",
    "MIOMA_SUBSEROSO": "Mioma Subseroso Grande: Generalmente no requiere cirugía para fertilidad, pero se deben vigilar los síntomas.",

    # ADENOMIOSIS
    "ADENO_FOCAL": "Adenomiosis Focal: Valorar tratamiento médico para controlar síntomas y mejorar la receptividad endometrial.",
    "ADENO_DIFUSA": "Adenomiosis Difusa: Se recomienda valoración para FIV, ya que la fertilidad espontánea puede estar muy reducida.",

    # PÓLIPOS
    "POLIPO": "Pólipo Endometrial: Se recomienda resección por histeroscopia (polipectomía) para optimizar la cavidad endometrial.",

    # HSG
    "HSG_UNILATERAL": "HSG - Obstrucción Unilateral: Considerar seguimiento folicular (ecografías) para dirigir las relaciones sexuales al ciclo en que se ovule del lado permeable.",
    "HSG_BILATERAL": "HSG - Obstrucción Bilateral: La concepción espontánea no es viable. Se requiere Fertilización In Vitro (FIV).",
    "HSG_DEFECTO": "HSG - Defecto Uterino: Se requiere histeroscopia para un diagnóstico preciso y posible corrección quirúrgica.",

    # AMH
    "AMH_BAJA": "AMH: Reserva ovárica disminuida detectada. Se recomienda no demorar la consulta y el tratamiento con un especialista.",
    
    # PROLACTINA
    "PRL_ALTA": "Prolactina: Nivel elevado. Requiere tratamiento con agonistas dopaminérgicos (ej. Cabergolina) y estudio completo por un endocrinólogo.",
    
    # TSH
    "TSH_ALTA": "TSH: Nivel fuera del rango óptimo para fertilidad (<2.5 µUI/mL). Se recomienda tratamiento de sustitución y control por endocrinólogo.",
    "TPO_POSITIVO": "TPO-Ab: La autoinmunidad tiroidea aumenta el riesgo de pérdida gestacional. Requiere seguimiento estricto durante el embarazo.",

    # HOMA
    "HOMA_ALTO": "HOMA: Resistencia a la insulina detectada. Priorizar cambios en el estilo de vida (dieta baja en carbohidratos, ejercicio) y valorar el uso de metformina con su médico.",
    
    # FACTOR MASCULINO
    "FACTOR_MASCULINO": "Factor Masculino: Hallazgos alterados en espermatograma. Se recomienda consulta con un Andrólogo/Urólogo."
}