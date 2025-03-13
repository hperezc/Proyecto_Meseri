def get_construction_coefficient(data):
    coeficientes = {
        'numero_pisos': {
            '1-2': 3,
            '3-5': 2,
            '6-9': 1,
            '10+': 0
        },
        'superficie_mayor_sector': {
            '0-500': 5,
            '501-1500': 4,
            '1501-2500': 3,
            '2501-3500': 2,
            '3501-4500': 1,
            '>4500': 0
        },
        'resistencia_fuego': {
            'hormigon': 10,
            'metalica': 5,
            'madera': 0
        },
        'falsos_techos': {
            'sin': 5,
            'incombustible': 3,
            'combustible': 0
        }
    }
    
    total = 0
    for campo, valores in coeficientes.items():
        if campo in data and data[campo] in valores:
            total += valores[data[campo]]
    
    return total

def calculate_meseri_score(data):
    # Calcular X (factores generadores y agravantes)
    x = (
        get_construction_coefficient(data) +
        get_situation_coefficient(data) +
        get_process_coefficient(data) +
        get_concentration_coefficient(data) +
        get_propagability_coefficient(data) +
        get_destructibility_coefficient(data)
    )
    
    # Calcular Y (factores protectores)
    y = get_protection_coefficient(data)
    
    # Calcular P (valoración del riesgo)
    p = (5/129) * x + (5/30) * y
    
    return {
        'x': x,
        'y': y,
        'p': p,
        'risk_level': get_risk_level(p)
    }

def get_risk_level(p):
    if p <= 3:
        return "Riesgo Muy Alto"
    elif p <= 5:
        return "Riesgo Alto"
    elif p <= 8:
        return "Riesgo Medio"
    else:
        return "Riesgo Bajo"

def get_situation_coefficient(data):
    coeficientes = {
        'distancia_bomberos': {
            'menor5': 10,
            '5-10': 8,
            '10-15': 6,
            '15-25': 2,
            'mayor25': 0
        },
        'accesibilidad_edificio': {
            'buena': 5,
            'media': 3,
            'mala': 1,
            'muy_mala': 0
        }
    }
    
    total = 0
    for campo, valores in coeficientes.items():
        if campo in data and data[campo] in valores:
            total += valores[data[campo]]
    return total

def get_process_coefficient(data):
    coeficientes = {
        'peligro_activacion': {
            'bajo': 10,
            'medio': 5,
            'alto': 0
        },
        'carga_fuego': {
            'baja': 10,
            'media': 5,
            'alta': 0
        },
        'combustibilidad': {
            'baja': 5,
            'media': 3,
            'alta': 0
        },
        'orden_limpieza': {
            'alto': 10,
            'medio': 5,
            'bajo': 0
        },
        'almacenamiento_altura': {
            'menor2': 3,
            '2-6': 2,
            'mayor6': 0
        }
    }
    
    total = 0
    for campo, valores in coeficientes.items():
        if campo in data and data[campo] in valores:
            total += valores[data[campo]]
    return total

def get_concentration_coefficient(data):
    coeficientes = {
        'concentracion_valores': {
            'inferior2.6': 3,
            'entre2.6-6.5': 2,
            'superior6.5': 0
        }
    }
    
    total = 0
    for campo, valores in coeficientes.items():
        if campo in data and data[campo] in valores:
            total += valores[data[campo]]
    return total

def get_propagability_coefficient(data):
    coeficientes = {
        'propagabilidad_vertical': {
            'baja': 5,
            'media': 3,
            'alta': 0
        },
        'propagabilidad_horizontal': {
            'baja': 5,
            'media': 3,
            'alta': 0
        }
    }
    
    total = 0
    for campo, valores in coeficientes.items():
        if campo in data and data[campo] in valores:
            total += valores[data[campo]]
    return total

def get_destructibility_coefficient(data):
    coeficientes = {
        'por_calor': {
            'baja': 10,
            'media': 5,
            'alta': 0
        },
        'por_humo': {
            'baja': 10,
            'media': 5,
            'alta': 0
        },
        'por_corrosion': {
            'baja': 10,
            'media': 5,
            'alta': 0
        },
        'por_agua': {
            'baja': 10,
            'media': 5,
            'alta': 0
        }
    }
    
    total = 0
    for campo, valores in coeficientes.items():
        if campo in data and data[campo] in valores:
            total += valores[data[campo]]
    return total

def get_protection_coefficient(data):
    coeficientes = {
        'extintores_portatiles': {
            'sin_vigilancia': 1,
            'con_vigilancia': 2,
            'no': 0
        },
        'bocas_incendio': {
            'sin_vigilancia': 2,
            'con_vigilancia': 4,
            'no': 0
        },
        'hidrantes_exteriores': {
            'sin_vigilancia': 2,
            'con_vigilancia': 4,
            'no': 0
        },
        'deteccion_automatica': {
            'sin_vigilancia_sin_cra': 0,
            'sin_vigilancia_con_cra': 2,
            'con_vigilancia_sin_cra': 3,
            'con_vigilancia_con_cra': 4,
            'no': 0
        },
        'rociadores_automaticos': {
            'sin_vigilancia_sin_cra': 5,
            'sin_vigilancia_con_cra': 6,
            'con_vigilancia_sin_cra': 7,
            'con_vigilancia_con_cra': 8,
            'no': 0
        },
        'equipos_primera_intervencion': {
            'sin_vigilancia': 2,
            'con_vigilancia': 2,
            'no': 0
        },
        'equipos_segunda_intervencion': {
            'sin_vigilancia': 4,
            'con_vigilancia': 4,
            'no': 0
        },
        'planes_emergencia': {
            'sin_vigilancia': 2,
            'con_vigilancia': 4,
            'no': 0
        }
    }
    
    total = 0
    for campo, valores in coeficientes.items():
        if campo in data and data[campo] in valores:
            total += valores[data[campo]]
    return total

def get_construction_weight(factor, value):
    weights = {
        'numero_pisos': {
            '1-2': 3,
            '3-5': 2,
            '6-9': 1,
            '10+': 0
        },
        'superficie_mayor_sector': {
            '0-500': 5,
            '501-1500': 4,
            '1501-2500': 3,
            '2501-3500': 2,
            '3501-4500': 1,
            '>4500': 0
        },
        'resistencia_fuego': {
            'hormigon': 10,
            'metalica': 5,
            'madera': 0
        },
        'falsos_techos': {
            'sin': 5,
            'incombustible': 3,
            'combustible': 0
        }
    }
    return weights.get(factor, {}).get(value, 0)

def get_situation_weight(factor, value):
    weights = {
        'distancia_bomberos': {
            'menor5': 10,
            '5-10': 8,
            '10-15': 6,
            '15-25': 2,
            'mayor25': 0
        },
        'accesibilidad_edificio': {
            'buena': 5,
            'media': 3,
            'mala': 1,
            'muy_mala': 0
        }
    }
    return weights.get(factor, {}).get(value, 0)

def get_process_weight(factor, value):
    weights = {
        'peligro_activacion': {
            'bajo': 10,
            'medio': 5,
            'alto': 0
        },
        'carga_fuego': {
            'baja': 10,
            'media': 5,
            'alta': 0
        },
        'combustibilidad': {
            'baja': 5,
            'media': 3,
            'alta': 0
        },
        'orden_limpieza': {
            'alto': 10,
            'medio': 5,
            'bajo': 0
        },
        'almacenamiento_altura': {
            'menor2': 3,
            '2-6': 2,
            'mayor6': 0
        }
    }
    return weights.get(factor, {}).get(value, 0)

def get_concentration_weight(factor, value):
    weights = {
        'concentracion_valores': {
            'inferior2.6': 3,
            'entre2.6-6.5': 2,
            'superior6.5': 0
        }
    }
    return weights.get(factor, {}).get(value, 0)

def get_propagability_weight(factor, value):
    weights = {
        'propagabilidad_vertical': {
            'baja': 5,
            'media': 3,
            'alta': 0
        },
        'propagabilidad_horizontal': {
            'baja': 5,
            'media': 3,
            'alta': 0
        }
    }
    return weights.get(factor, {}).get(value, 0)

def get_destructibility_weight(factor, value):
    weights = {
        'por_calor': {
            'baja': 10,
            'media': 5,
            'alta': 0
        },
        'por_humo': {
            'baja': 10,
            'media': 5,
            'alta': 0
        },
        'por_corrosion': {
            'baja': 10,
            'media': 5,
            'alta': 0
        },
        'por_agua': {
            'baja': 10,
            'media': 5,
            'alta': 0
        }
    }
    return weights.get(factor, {}).get(value, 0)

def get_protection_weight(factor, value):
    weights = {
        'extintores_portatiles': {
            'sin_vigilancia': 1,
            'con_vigilancia': 2,
            'no': 0
        },
        'bocas_incendio': {
            'sin_vigilancia': 2,
            'con_vigilancia': 4,
            'no': 0
        },
        'hidrantes_exteriores': {
            'sin_vigilancia': 2,
            'con_vigilancia': 4,
            'no': 0
        },
        'deteccion_automatica': {
            'sin_vigilancia_sin_cra': 0,
            'sin_vigilancia_con_cra': 2,
            'con_vigilancia_sin_cra': 3,
            'con_vigilancia_con_cra': 4,
            'no': 0
        },
        'rociadores_automaticos': {
            'sin_vigilancia_sin_cra': 5,
            'sin_vigilancia_con_cra': 6,
            'con_vigilancia_sin_cra': 7,
            'con_vigilancia_con_cra': 8,
            'no': 0
        },
        'equipos_primera_intervencion': {
            'sin_vigilancia': 2,
            'con_vigilancia': 2,
            'no': 0
        },
        'equipos_segunda_intervencion': {
            'sin_vigilancia': 4,
            'con_vigilancia': 4,
            'no': 0
        },
        'planes_emergencia': {
            'sin_vigilancia': 2,
            'con_vigilancia': 4,
            'no': 0
        }
    }
    return weights.get(factor, {}).get(value, 0)