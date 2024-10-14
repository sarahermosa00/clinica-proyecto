from django import template

register = template.Library()

@register.filter
def formato_guaranies(value):
    """ Formatea los montos con separadores de miles y añade la etiqueta Gs """
    try:
        value = float(value)
        return f"{value:,.0f} Gs".replace(",", ".")  # Usa puntos como separadores de miles
    except (ValueError, TypeError):
        return value
