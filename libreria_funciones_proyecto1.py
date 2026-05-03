import math

# =========================================================
# FUNCIONES AUXILIARES (Pueden ser modificadas en caso de que las ecuaciones si acepten valores negativos)
# =========================================================

def validar_positivo(valor: float, nombre: str, permitir_cero: bool = False) -> None:
    if permitir_cero:
        if valor < 0:
            raise ValueError(f"{nombre} no puede ser negativo.")
    else:
        if valor <= 0:
            raise ValueError(f"{nombre} debe ser mayor que cero.")


def validar_porcentaje(valor: float, nombre: str) -> None:
    if valor < 0 or valor > 100:
        raise ValueError(f"{nombre} debe estar entre 0 y 100.")



# =========================================================
# 1) SALUD
# =========================================================

def calcular_imc(peso_kg: float, altura_m: float) -> dict:
    """
    Calcula el Índice de Masa Corporal (IMC).
    Fórmula: IMC = peso / altura²
    """
    validar_positivo(peso_kg, "peso_kg")
    validar_positivo(altura_m, "altura_m")

    imc = peso_kg / (altura_m ** 2)

    if imc < 18.5:
        clasificacion = "Bajo peso"
    elif imc < 25:
        clasificacion = "Peso normal"
    elif imc < 30:
        clasificacion = "Sobrepeso"
    else:
        clasificacion = "Obesidad"

    return {
        "imc": round(imc, 2),
        "clasificacion": clasificacion
    }


def calcular_superficie_corporal(peso_kg: float, altura_cm: float) -> dict:
    """
    Calcula la Superficie Corporal usando la fórmula de Mosteller.
    Fórmula: SC = sqrt((peso * altura) / 3600)
    """
    validar_positivo(peso_kg, "peso_kg")
    validar_positivo(altura_cm, "altura_cm")

    superficie = math.sqrt((peso_kg * altura_cm) / 3600)

    return {
        "superficie_corporal_m2": round(superficie, 3)
    }


# =========================================================
# 2) ENFERMERÍA
# =========================================================

def calcular_goteo_intravenoso(volumen_ml: float, tiempo_horas: float, factor_goteo: float) -> dict:
    """
    Calcula la velocidad de infusión.
    Fórmulas:
    - mL/h = volumen / tiempo
    - gotas/min = (volumen * factor_goteo) / (tiempo_horas * 60)
    """
    validar_positivo(volumen_ml, "volumen_ml")
    validar_positivo(tiempo_horas, "tiempo_horas")
    validar_positivo(factor_goteo, "factor_goteo")

    ml_hora = volumen_ml / tiempo_horas
    gotas_min = (volumen_ml * factor_goteo) / (tiempo_horas * 60)

    return {
        "velocidad_ml_h": round(ml_hora, 2),
        "goteo_gotas_min": round(gotas_min, 2)
    }


# =========================================================
# 3) EDUCACIÓN
# =========================================================

def calcular_nota_final_ponderada(
    actividades: float,
    proyecto: float,
    examen_final: float,
    peso_actividades: float,
    peso_proyecto: float,
    peso_examen_final: float,
    nota_minima_aprobacion: float = 7.0
) -> dict:
    """
    Calcula la nota final ponderada.
    Los pesos pueden ingresarse en porcentaje y deben sumar 100.
    """
    pesos = peso_actividades + peso_proyecto + peso_examen_final

    if round(pesos, 6) != 100:
        raise ValueError("La suma de los pesos debe ser 100.")

    nota_final = (
        actividades * (peso_actividades / 100) +
        proyecto * (peso_proyecto / 100) +
        examen_final * (peso_examen_final / 100)
    )

    estado = "Aprueba" if nota_final >= nota_minima_aprobacion else "No aprueba"

    return {
        "nota_final": round(nota_final, 2),
        "estado": estado
    }


def calcular_asistencia_minima(total_clases: int, clases_asistidas: int, porcentaje_minimo: float = 75) -> dict:
    """
    Calcula si el estudiante cumple el porcentaje mínimo de asistencia.
    """
    validar_positivo(total_clases, "total_clases")
    validar_positivo(clases_asistidas, "clases_asistidas", permitir_cero=True)
    validar_porcentaje(porcentaje_minimo, "porcentaje_minimo")

    if clases_asistidas > total_clases:
        raise ValueError("clases_asistidas no puede ser mayor que total_clases.")

    porcentaje_actual = (clases_asistidas / total_clases) * 100
    clases_minimas = math.ceil(total_clases * (porcentaje_minimo / 100))
    faltan = max(0, clases_minimas - clases_asistidas)

    return {
        "porcentaje_actual": round(porcentaje_actual, 2),
        "clases_minimas_requeridas": clases_minimas,
        "clases_faltantes_para_cumplir": faltan,
        "cumple": porcentaje_actual >= porcentaje_minimo
    }


# =========================================================
# 4) ADMINISTRACIÓN / NEGOCIOS
# =========================================================

def calcular_punto_equilibrio(costos_fijos: float, precio_unitario: float, costo_variable_unitario: float) -> dict:
    """
    Calcula el punto de equilibrio en unidades y en ventas.
    Fórmula:
    - margen de contribución = precio - costo variable
    - punto equilibrio unidades = costos fijos / margen contribución
    """
    validar_positivo(costos_fijos, "costos_fijos")
    validar_positivo(precio_unitario, "precio_unitario")
    validar_positivo(costo_variable_unitario, "costo_variable_unitario", permitir_cero=True)

    margen_contribucion = precio_unitario - costo_variable_unitario

    if margen_contribucion <= 0:
        raise ValueError("El precio_unitario debe ser mayor que el costo_variable_unitario.")

    unidades = costos_fijos / margen_contribucion
    ventas = unidades * precio_unitario

    return {
        "margen_contribucion_unitario": round(margen_contribucion, 2),
        "punto_equilibrio_unidades": round(unidades, 2),
        "punto_equilibrio_ventas": round(ventas, 2)
    }


def calcular_margen_neto(ingresos: float, costos: float, gastos_operativos: float, impuestos: float) -> dict:
    """
    Calcula utilidad bruta, utilidad neta y margen neto.
    Fórmula:
    - utilidad neta = ingresos - costos - gastos operativos - impuestos
    - margen neto = utilidad neta / ingresos
    """
    validar_positivo(ingresos, "ingresos")
    validar_positivo(costos, "costos", permitir_cero=True)
    validar_positivo(gastos_operativos, "gastos_operativos", permitir_cero=True)
    validar_positivo(impuestos, "impuestos", permitir_cero=True)

    utilidad_bruta = ingresos - costos
    utilidad_neta = ingresos - costos - gastos_operativos - impuestos
    margen_neto = (utilidad_neta / ingresos) * 100

    return {
        "utilidad_bruta": round(utilidad_bruta, 2),
        "utilidad_neta": round(utilidad_neta, 2),
        "margen_neto_pct": round(margen_neto, 2)
    }


def calcular_ticket_promedio(ventas_totales: float, numero_clientes: int) -> dict:
    """
    Calcula el ticket promedio por cliente.
    Fórmula:
    ticket_promedio = ventas_totales / numero_clientes
    """
    validar_positivo(ventas_totales, "ventas_totales")
    validar_positivo(numero_clientes, "numero_clientes")

    ticket = ventas_totales / numero_clientes

    return {
        "ticket_promedio": round(ticket, 2)
    }


def calcular_tasa_crecimiento_ventas(ventas_periodo_anterior: float, ventas_periodo_actual: float) -> dict:
    """
    Calcula la tasa de crecimiento de ventas en porcentaje.
    Fórmula:
    crecimiento = ((actual - anterior) / anterior) * 100
    """
    validar_positivo(ventas_periodo_anterior, "ventas_periodo_anterior")
    validar_positivo(ventas_periodo_actual, "ventas_periodo_actual", permitir_cero=True)

    crecimiento = (
        (ventas_periodo_actual - ventas_periodo_anterior) / ventas_periodo_anterior
    ) * 100

    return {
        "tasa_crecimiento_pct": round(crecimiento, 2)
    }


def calcular_cac(gasto_marketing: float, gasto_ventas: float, nuevos_clientes: int) -> dict:
    """
    Calcula el Costo de Adquisición de Cliente (CAC).
    Fórmula:
    CAC = (gasto_marketing + gasto_ventas) / nuevos_clientes
    """
    validar_positivo(gasto_marketing, "gasto_marketing", permitir_cero=True)
    validar_positivo(gasto_ventas, "gasto_ventas", permitir_cero=True)
    validar_positivo(nuevos_clientes, "nuevos_clientes")

    cac = (gasto_marketing + gasto_ventas) / nuevos_clientes

    return {
        "cac": round(cac, 2)
    }


def calcular_rotacion_personal(numero_bajas: int, empleados_inicio: int, empleados_fin: int) -> dict:
    """
    Calcula la tasa de rotación de personal.
    Fórmula:
    empleados_promedio = (empleados_inicio + empleados_fin) / 2
    rotacion = (numero_bajas / empleados_promedio) * 100
    """
    validar_positivo(numero_bajas, "numero_bajas", permitir_cero=True)
    validar_positivo(empleados_inicio, "empleados_inicio")
    validar_positivo(empleados_fin, "empleados_fin")

    empleados_promedio = (empleados_inicio + empleados_fin) / 2
    rotacion = (numero_bajas / empleados_promedio) * 100

    return {
        "empleados_promedio": round(empleados_promedio, 2),
        "rotacion_personal_pct": round(rotacion, 2)
    }

# =========================================================
# 5) FINANZAS
# =========================================================

def calcular_cuota_prestamo_frances(monto: float, tasa_anual_pct: float, plazo_meses: int) -> dict:
    """
    Calcula la cuota mensual de un préstamo bajo sistema francés.
    """
    validar_positivo(monto, "monto")
    validar_porcentaje(tasa_anual_pct, "tasa_anual_pct")
    validar_positivo(plazo_meses, "plazo_meses")

    tasa_mensual = (tasa_anual_pct / 100) / 12

    if tasa_mensual == 0:
        cuota = monto / plazo_meses
    else:
        cuota = monto * (
            tasa_mensual * (1 + tasa_mensual) ** plazo_meses
        ) / (
            (1 + tasa_mensual) ** plazo_meses - 1
        )

    total_pagado = cuota * plazo_meses
    interes_total = total_pagado - monto

    return {
        "cuota_mensual": round(cuota, 2),
        "total_pagado": round(total_pagado, 2),
        "interes_total": round(interes_total, 2)
    }


def calcular_payback_simple(inversion_inicial: float, flujo_anual: float) -> dict:
    """
    Calcula el período de recuperación simple de la inversión.
    Fórmula:
    payback = inversion_inicial / flujo_anual
    """
    validar_positivo(inversion_inicial, "inversion_inicial")
    validar_positivo(flujo_anual, "flujo_anual")

    payback = inversion_inicial / flujo_anual

    return {
        "payback_anios": round(payback, 2)
    }


def calcular_ratio_endeudamiento(pasivo_total: float, activo_total: float) -> dict:
    """
    Calcula el ratio de endeudamiento.
    Fórmula:
    endeudamiento = pasivo_total / activo_total
    """
    validar_positivo(pasivo_total, "pasivo_total", permitir_cero=True)
    validar_positivo(activo_total, "activo_total")

    ratio = (pasivo_total / activo_total) * 100

    return {
        "ratio_endeudamiento_pct": round(ratio, 2)
    }


def calcular_rentabilidad_esperada(capital_invertido: float, utilidad_esperada: float) -> dict:
    """
    Calcula la rentabilidad esperada sobre una inversión.
    Fórmula:
    rentabilidad = utilidad_esperada / capital_invertido
    """
    validar_positivo(capital_invertido, "capital_invertido")
    validar_positivo(utilidad_esperada, "utilidad_esperada", permitir_cero=True)

    rentabilidad = (utilidad_esperada / capital_invertido) * 100

    return {
        "rentabilidad_esperada_pct": round(rentabilidad, 2)
    }


def calcular_wacc(
    deuda: float,
    patrimonio: float,
    costo_deuda_pct: float,
    costo_patrimonio_pct: float,
    impuesto_pct: float
) -> dict:
    """
    Calcula el costo promedio ponderado de capital (WACC).
    Fórmula:
    WACC = (D/V)*Kd*(1-T) + (E/V)*Ke
    """
    validar_positivo(deuda, "deuda", permitir_cero=True)
    validar_positivo(patrimonio, "patrimonio", permitir_cero=True)
    validar_porcentaje(costo_deuda_pct, "costo_deuda_pct")
    validar_porcentaje(costo_patrimonio_pct, "costo_patrimonio_pct")
    validar_porcentaje(impuesto_pct, "impuesto_pct")

    valor_total = deuda + patrimonio
    if valor_total == 0:
        raise ValueError("La suma de deuda y patrimonio no puede ser cero.")

    kd = costo_deuda_pct / 100
    ke = costo_patrimonio_pct / 100
    t = impuesto_pct / 100

    wacc = ((deuda / valor_total) * kd * (1 - t)) + ((patrimonio / valor_total) * ke)

    return {
        "wacc_pct": round(wacc * 100, 2)
    }

# =========================================================
# 6) CONTABILIDAD
# =========================================================

def calcular_depreciacion_linea_recta(costo_activo: float, valor_residual: float, vida_util_anios: int) -> dict:
    """
    Calcula la depreciación por línea recta.
    Fórmula:
    depreciación anual = (costo - valor residual) / vida útil
    """
    validar_positivo(costo_activo, "costo_activo")
    validar_positivo(valor_residual, "valor_residual", permitir_cero=True)
    validar_positivo(vida_util_anios, "vida_util_anios")

    if valor_residual >= costo_activo:
        raise ValueError("valor_residual debe ser menor que costo_activo.")

    depreciacion_anual = (costo_activo - valor_residual) / vida_util_anios
    depreciacion_mensual = depreciacion_anual / 12

    return {
        "depreciacion_anual": round(depreciacion_anual, 2),
        "depreciacion_mensual": round(depreciacion_mensual, 2)
    }


def calcular_rotacion_inventario(costo_ventas: float, inventario_inicial: float, inventario_final: float) -> dict:
    """
    Calcula la rotación de inventario y días promedio en inventario.
    Fórmulas:
    - inventario promedio = (inicial + final) / 2
    - rotación = costo ventas / inventario promedio
    - días inventario = 365 / rotación
    """
    validar_positivo(costo_ventas, "costo_ventas")
    validar_positivo(inventario_inicial, "inventario_inicial", permitir_cero=True)
    validar_positivo(inventario_final, "inventario_final", permitir_cero=True)

    inventario_promedio = (inventario_inicial + inventario_final) / 2

    if inventario_promedio == 0:
        raise ValueError("El inventario promedio no puede ser cero.")

    rotacion = costo_ventas / inventario_promedio
    dias = 365 / rotacion

    return {
        "inventario_promedio": round(inventario_promedio, 2),
        "rotacion_inventario": round(rotacion, 2),
        "dias_promedio_inventario": round(dias, 2)
    }


def calcular_razon_corriente(activo_corriente: float, pasivo_corriente: float) -> dict:
    """
    Calcula la razón corriente.
    Fórmula:
    razon_corriente = activo_corriente / pasivo_corriente
    """
    validar_positivo(activo_corriente, "activo_corriente", permitir_cero=True)
    validar_positivo(pasivo_corriente, "pasivo_corriente")

    razon = activo_corriente / pasivo_corriente

    return {
        "razon_corriente": round(razon, 2)
    }


def calcular_prueba_acida(activo_corriente: float, inventarios: float, pasivo_corriente: float) -> dict:
    """
    Calcula la prueba ácida.
    Fórmula:
    prueba_acida = (activo_corriente - inventarios) / pasivo_corriente
    """
    validar_positivo(activo_corriente, "activo_corriente")
    validar_positivo(inventarios, "inventarios", permitir_cero=True)
    validar_positivo(pasivo_corriente, "pasivo_corriente")

    if inventarios > activo_corriente:
        raise ValueError("inventarios no puede ser mayor que activo_corriente.")

    prueba = (activo_corriente - inventarios) / pasivo_corriente

    return {
        "prueba_acida": round(prueba, 2)
    }


def calcular_capital_trabajo(activo_corriente: float, pasivo_corriente: float) -> dict:
    """
    Calcula el capital de trabajo.
    Fórmula:
    capital_trabajo = activo_corriente - pasivo_corriente
    """
    validar_positivo(activo_corriente, "activo_corriente", permitir_cero=True)
    validar_positivo(pasivo_corriente, "pasivo_corriente", permitir_cero=True)

    capital = activo_corriente - pasivo_corriente

    return {
        "capital_trabajo": round(capital, 2)
    }


def calcular_periodo_cobro_promedio(cuentas_por_cobrar: float, ventas_credito_anuales: float) -> dict:
    """
    Calcula el período promedio de cobro.
    Fórmula:
    periodo_cobro = (cuentas_por_cobrar / ventas_credito_anuales) * 360
    """
    validar_positivo(cuentas_por_cobrar, "cuentas_por_cobrar", permitir_cero=True)
    validar_positivo(ventas_credito_anuales, "ventas_credito_anuales")

    periodo = (cuentas_por_cobrar / ventas_credito_anuales) * 360

    return {
        "periodo_cobro_dias": round(periodo, 2)
    }

# =========================================================
# 7) DERECHO / GESTIÓN LEGAL
# =========================================================

def calcular_interes_mora(capital: float, tasa_anual_pct: float, dias_mora: int, base_anual: int = 360) -> dict:
    """
    Calcula interés simple por mora.
    Fórmula:
    interés = capital * tasa * (días / base_anual)

    Nota: esto es referencial. La aplicación legal real depende de la norma local.
    """
    validar_positivo(capital, "capital")
    validar_porcentaje(tasa_anual_pct, "tasa_anual_pct")
    validar_positivo(dias_mora, "dias_mora", permitir_cero=True)
    validar_positivo(base_anual, "base_anual")

    interes = capital * (tasa_anual_pct / 100) * (dias_mora / base_anual)
    total = capital + interes

    return {
        "interes_mora": round(interes, 2),
        "total_con_mora": round(total, 2)
    }


# =========================================================
# 8) MANTENIMIENTO
# =========================================================

def calcular_indicadores_mantenimiento(tiempo_operacion_h: float, numero_fallas: int, tiempo_reparacion_total_h: float) -> dict:
    """
    Calcula MTBF, MTTR y disponibilidad.
    Fórmulas:
    - MTBF = tiempo operación / número fallas
    - MTTR = tiempo reparación total / número fallas
    - disponibilidad = MTBF / (MTBF + MTTR)
    """
    validar_positivo(tiempo_operacion_h, "tiempo_operacion_h")
    validar_positivo(numero_fallas, "numero_fallas")
    validar_positivo(tiempo_reparacion_total_h, "tiempo_reparacion_total_h", permitir_cero=True)

    mtbf = tiempo_operacion_h / numero_fallas
    mttr = tiempo_reparacion_total_h / numero_fallas
    disponibilidad = (mtbf / (mtbf + mttr)) * 100 if (mtbf + mttr) > 0 else 0

    return {
        "mtbf_h": round(mtbf, 2),
        "mttr_h": round(mttr, 2),
        "disponibilidad_pct": round(disponibilidad, 2)
    }


def calcular_oee(disponibilidad_pct: float, rendimiento_pct: float, calidad_pct: float) -> dict:
    """
    Calcula el OEE (Overall Equipment Effectiveness).
    Fórmula:
    OEE = disponibilidad * rendimiento * calidad
    """
    validar_porcentaje(disponibilidad_pct, "disponibilidad_pct")
    validar_porcentaje(rendimiento_pct, "rendimiento_pct")
    validar_porcentaje(calidad_pct, "calidad_pct")

    disponibilidad = disponibilidad_pct / 100
    rendimiento = rendimiento_pct / 100
    calidad = calidad_pct / 100

    oee = disponibilidad * rendimiento * calidad * 100

    return {
        "oee_pct": round(oee, 2)
    }


# =========================================================
# 9) GESTIÓN DE CALIDAD
# =========================================================

def calcular_dpmo(defectos: int, unidades: int, oportunidades_por_unidad: int) -> dict:
    """
    Calcula DPMO (Defectos por Millón de Oportunidades).
    Fórmula:
    DPMO = (defectos / (unidades * oportunidades)) * 1,000,000
    """
    validar_positivo(defectos, "defectos", permitir_cero=True)
    validar_positivo(unidades, "unidades")
    validar_positivo(oportunidades_por_unidad, "oportunidades_por_unidad")

    oportunidades_totales = unidades * oportunidades_por_unidad

    dpmo = (defectos / oportunidades_totales) * 1_000_000
    rendimiento = (1 - (defectos / oportunidades_totales)) * 100

    return {
        "oportunidades_totales": oportunidades_totales,
        "dpmo": round(dpmo, 2),
        "rendimiento_pct": round(rendimiento, 4)
    }


# =========================================================
# 10) TECNOLOGÍA / INFORMÁTICA
# =========================================================

def calcular_metricas_clasificacion(tp: int, fp: int, fn: int) -> dict:
    """
    Calcula precisión, recall y F1-score.
    Fórmulas:
    - precisión = TP / (TP + FP)
    - recall = TP / (TP + FN)
    - F1 = 2 * (precisión * recall) / (precisión + recall)
    """
    validar_positivo(tp, "tp", permitir_cero=True)
    validar_positivo(fp, "fp", permitir_cero=True)
    validar_positivo(fn, "fn", permitir_cero=True)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4)
    }


def calcular_disponibilidad_sistema(tiempo_total_horas: float, tiempo_caida_horas: float) -> dict:
    """
    Calcula la disponibilidad de un sistema.
    Fórmula:
    disponibilidad = ((tiempo_total - tiempo_caida) / tiempo_total) * 100
    """
    validar_positivo(tiempo_total_horas, "tiempo_total_horas")
    validar_positivo(tiempo_caida_horas, "tiempo_caida_horas", permitir_cero=True)

    if tiempo_caida_horas > tiempo_total_horas:
        raise ValueError("tiempo_caida_horas no puede ser mayor que tiempo_total_horas.")

    disponibilidad = (
        (tiempo_total_horas - tiempo_caida_horas) / tiempo_total_horas
    ) * 100

    return {
        "disponibilidad_pct": round(disponibilidad, 4)
    }


def calcular_tiempo_transferencia_archivo(tamano_mb: float, velocidad_mbps: float) -> dict:
    """
    Calcula el tiempo estimado de transferencia de un archivo.
    Conversión:
    1 byte = 8 bits
    Fórmula:
    tiempo_segundos = (tamano_mb * 8) / velocidad_mbps
    """
    validar_positivo(tamano_mb, "tamano_mb")
    validar_positivo(velocidad_mbps, "velocidad_mbps")

    tiempo_segundos = (tamano_mb * 8) / velocidad_mbps
    tiempo_minutos = tiempo_segundos / 60

    return {
        "tiempo_segundos": round(tiempo_segundos, 2),
        "tiempo_minutos": round(tiempo_minutos, 2)
    }


def calcular_tasa_error_transacciones(transacciones_fallidas: int, transacciones_totales: int) -> dict:
    """
    Calcula la tasa de error de transacciones.
    Fórmula:
    tasa_error = (fallidas / totales) * 100
    """
    validar_positivo(transacciones_fallidas, "transacciones_fallidas", permitir_cero=True)
    validar_positivo(transacciones_totales, "transacciones_totales")

    if transacciones_fallidas > transacciones_totales:
        raise ValueError("transacciones_fallidas no puede ser mayor que transacciones_totales.")

    tasa_error = (transacciones_fallidas / transacciones_totales) * 100
    tasa_exito = 100 - tasa_error

    return {
        "tasa_error_pct": round(tasa_error, 4),
        "tasa_exito_pct": round(tasa_exito, 4)
    }


def calcular_almacenamiento_respaldo(
    numero_usuarios: int,
    archivos_por_usuario: int,
    tamano_promedio_mb: float,
    factor_respaldo: float
) -> dict:
    """
    Calcula el almacenamiento estimado necesario para respaldo.
    Fórmula:
    almacenamiento_total = usuarios * archivos_por_usuario * tamano_promedio_mb * factor_respaldo
    """
    validar_positivo(numero_usuarios, "numero_usuarios")
    validar_positivo(archivos_por_usuario, "archivos_por_usuario")
    validar_positivo(tamano_promedio_mb, "tamano_promedio_mb")
    validar_positivo(factor_respaldo, "factor_respaldo")

    almacenamiento_mb = (
        numero_usuarios * archivos_por_usuario * tamano_promedio_mb * factor_respaldo
    )
    almacenamiento_gb = almacenamiento_mb / 1024

    return {
        "almacenamiento_estimado_mb": round(almacenamiento_mb, 2),
        "almacenamiento_estimado_gb": round(almacenamiento_gb, 2)
    }

# =========================================================
# 11) INGENIERÍA CIVIL
# =========================================================

def calcular_material_concreto(
    largo_m: float,
    ancho_m: float,
    espesor_m: float,
    desperdicio_pct: float,
    dosificacion_cemento_kg_m3: float
) -> dict:
    """
    Calcula volumen de concreto, volumen con desperdicio
    y cantidad estimada de cemento.
    """
    validar_positivo(largo_m, "largo_m")
    validar_positivo(ancho_m, "ancho_m")
    validar_positivo(espesor_m, "espesor_m")
    validar_porcentaje(desperdicio_pct, "desperdicio_pct")
    validar_positivo(dosificacion_cemento_kg_m3, "dosificacion_cemento_kg_m3")

    volumen = largo_m * ancho_m * espesor_m
    volumen_ajustado = volumen * (1 + desperdicio_pct / 100)
    cemento_kg = volumen_ajustado * dosificacion_cemento_kg_m3
    sacos_50kg = cemento_kg / 50

    return {
        "volumen_m3": round(volumen, 3),
        "volumen_con_desperdicio_m3": round(volumen_ajustado, 3),
        "cemento_kg": round(cemento_kg, 2),
        "sacos_50kg": round(sacos_50kg, 2)
    }


# =========================================================
# 12) ARQUITECTURA
# =========================================================

def calcular_iluminacion_requerida(
    area_m2: float,
    nivel_lux: float,
    factor_utilizacion: float,
    factor_mantenimiento: float,
    flujo_luminaria_lm: float
) -> dict:
    """
    Calcula lúmenes requeridos y número de luminarias.
    Fórmula:
    lúmenes totales = (lux * área) / (FU * FM)
    """
    validar_positivo(area_m2, "area_m2")
    validar_positivo(nivel_lux, "nivel_lux")
    validar_positivo(flujo_luminaria_lm, "flujo_luminaria_lm")

    if not (0 < factor_utilizacion <= 1):
        raise ValueError("factor_utilizacion debe estar entre 0 y 1.")
    if not (0 < factor_mantenimiento <= 1):
        raise ValueError("factor_mantenimiento debe estar entre 0 y 1.")

    lumenes_totales = (nivel_lux * area_m2) / (factor_utilizacion * factor_mantenimiento)
    numero_luminarias = math.ceil(lumenes_totales / flujo_luminaria_lm)

    return {
        "lumenes_totales_requeridos": round(lumenes_totales, 2),
        "numero_luminarias": numero_luminarias
    }


# =========================================================
# 13) AGRONOMÍA
# =========================================================

def calcular_densidad_siembra(area_hectareas: float, distancia_surcos_m: float, distancia_plantas_m: float, germinacion_pct: float) -> dict:
    """
    Calcula densidad de siembra y semillas ajustadas por germinación.
    """
    validar_positivo(area_hectareas, "area_hectareas")
    validar_positivo(distancia_surcos_m, "distancia_surcos_m")
    validar_positivo(distancia_plantas_m, "distancia_plantas_m")
    validar_porcentaje(germinacion_pct, "germinacion_pct")

    area_m2 = area_hectareas * 10000
    plantas_teoricas = area_m2 / (distancia_surcos_m * distancia_plantas_m)

    if germinacion_pct == 0:
        raise ValueError("germinacion_pct no puede ser cero.")

    semillas_ajustadas = plantas_teoricas / (germinacion_pct / 100)

    return {
        "plantas_teoricas": round(plantas_teoricas, 2),
        "semillas_ajustadas": round(semillas_ajustadas, 2)
    }


def calcular_requerimiento_fertilizante(
    area_hectareas: float,
    dosis_nutriente_kg_ha: float,
    pureza_fertilizante_pct: float,
    eficiencia_aplicacion_pct: float
) -> dict:
    """
    Calcula la cantidad de fertilizante comercial requerida.
    Fórmula:
    fertilizante = (área * dosis nutriente) / (pureza * eficiencia)
    """
    validar_positivo(area_hectareas, "area_hectareas")
    validar_positivo(dosis_nutriente_kg_ha, "dosis_nutriente_kg_ha")
    validar_porcentaje(pureza_fertilizante_pct, "pureza_fertilizante_pct")
    validar_porcentaje(eficiencia_aplicacion_pct, "eficiencia_aplicacion_pct")

    pureza = pureza_fertilizante_pct / 100
    eficiencia = eficiencia_aplicacion_pct / 100

    if pureza == 0 or eficiencia == 0:
        raise ValueError("La pureza y la eficiencia deben ser mayores que cero.")

    kg_fertilizante = (area_hectareas * dosis_nutriente_kg_ha) / (pureza * eficiencia)
    sacos_50kg = kg_fertilizante / 50

    return {
        "fertilizante_requerido_kg": round(kg_fertilizante, 2),
        "sacos_50kg": round(sacos_50kg, 2)
    }


# =========================================================
# 14) ECONOMÍA / NEGOCIOS
# =========================================================

def calcular_roi(ganancia_neta: float, inversion: float) -> dict:
    """
    Calcula el Retorno sobre la Inversión (ROI).
    Fórmula:
    ROI = ganancia_neta / inversión
    """
    validar_positivo(inversion, "inversion")
    validar_positivo(ganancia_neta, "ganancia_neta", permitir_cero=True)

    roi = (ganancia_neta / inversion) * 100

    return {
        "roi_pct": round(roi, 2)
    }


def calcular_valor_futuro(monto_inicial: float, tasa_anual_pct: float, anios: float, capitalizaciones_por_anio: int = 12) -> dict:
    """
    Calcula valor futuro con interés compuesto.
    Fórmula:
    VF = P * (1 + r/n)^(n*t)
    """
    validar_positivo(monto_inicial, "monto_inicial")
    validar_porcentaje(tasa_anual_pct, "tasa_anual_pct")
    validar_positivo(anios, "anios")
    validar_positivo(capitalizaciones_por_anio, "capitalizaciones_por_anio")

    tasa = tasa_anual_pct / 100
    vf = monto_inicial * (1 + tasa / capitalizaciones_por_anio) ** (capitalizaciones_por_anio * anios)
    interes_ganado = vf - monto_inicial

    return {
        "valor_futuro": round(vf, 2),
        "interes_ganado": round(interes_ganado, 2)
    }


# =========================================================
# 15) PRODUCTIVIDAD / OPERACIONES
# =========================================================

def calcular_productividad_laboral(unidades_producidas: float, horas_trabajadas: float, numero_trabajadores: int) -> dict:
    """
    Calcula productividad por hora y por trabajador.
    """
    validar_positivo(unidades_producidas, "unidades_producidas")
    validar_positivo(horas_trabajadas, "horas_trabajadas")
    validar_positivo(numero_trabajadores, "numero_trabajadores")

    productividad_hora = unidades_producidas / horas_trabajadas
    productividad_trabajador = unidades_producidas / numero_trabajadores

    return {
        "productividad_por_hora": round(productividad_hora, 2),
        "productividad_por_trabajador": round(productividad_trabajador, 2)
    }


def calcular_costo_unitario_total(materiales: float, mano_obra: float, costos_indirectos: float, unidades_producidas: float) -> dict:
    """
    Calcula costo total y costo unitario.
    """
    validar_positivo(materiales, "materiales", permitir_cero=True)
    validar_positivo(mano_obra, "mano_obra", permitir_cero=True)
    validar_positivo(costos_indirectos, "costos_indirectos", permitir_cero=True)
    validar_positivo(unidades_producidas, "unidades_producidas")

    costo_total = materiales + mano_obra + costos_indirectos
    costo_unitario = costo_total / unidades_producidas

    return {
        "costo_total": round(costo_total, 2),
        "costo_unitario": round(costo_unitario, 2)
    }