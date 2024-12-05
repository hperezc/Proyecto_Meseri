def get_epm_risk_level(p_value):
    if p_value >= 7.0:
        return "Aceptable"
    elif 5.0 <= p_value < 7.0:
        return "Tolerable"
    elif 3.0 <= p_value < 5.0:
        return "Alto"
    else:
        return "Extremo"

def get_epm_risk_color(risk_level):
    colors = {
        "Aceptable": "#28a745",  # Verde
        "Tolerable": "#ffc107",  # Amarillo
        "Alto": "#fd7e14",      # Naranja
        "Extremo": "#dc3545"    # Rojo
    }
    return colors.get(risk_level, "#6c757d")  # Gris por defecto 