def get_epm_risk_level(p):
    if p >= 8:
        return "Baja"     # Para probabilidad Baja
    elif 5 <= p < 8:
        return "Media"     # Para probabilidad Media
    elif 3 <= p < 5:
        return "Alta"          # Para probabilidad Alta
    else:
        return "Muy Alta"       # Para probabilidad Muy Alta

def get_epm_risk_color(risk_level):
    colors = {
        "baja": "#28a745",  # Verde
        "media": "#ffc107",  # Amarillo
        "Alta": "#fd7e14",      # Naranja
        "Muy Alta": "#dc3545"    # Rojo
    }
    return colors.get(risk_level, "#6c757d")  # Gris por defecto 