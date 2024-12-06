def get_epm_risk_level(p):
    if p >= 8:
        return "Aceptable"     # Para Riesgo Bajo
    elif 5 <= p < 8:
        return "Tolerable"     # Para Riesgo Medio
    elif 3 <= p < 5:
        return "Alto"          # Para Riesgo Alto
    else:
        return "Extremo"       # Para Riesgo Muy Alto

def get_epm_risk_color(risk_level):
    colors = {
        "Aceptable": "#28a745",  # Verde
        "Tolerable": "#ffc107",  # Amarillo
        "Alto": "#fd7e14",      # Naranja
        "Extremo": "#dc3545"    # Rojo
    }
    return colors.get(risk_level, "#6c757d")  # Gris por defecto 