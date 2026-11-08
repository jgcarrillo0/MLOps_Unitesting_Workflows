"""Funciones puras de preprocesamiento, independientes de FastAPI."""

import math
import re
import unicodedata


def clean_text(value: str) -> str:
    """Normaliza Unicode, convierte a minúsculas y colapsa espacios.

    Se preservan las tildes y los signos de puntuación.
    """
    if not isinstance(value, str):
        raise TypeError("value debe ser un texto")
    normalized = unicodedata.normalize("NFC", value)
    return re.sub(r"\s+", " ", normalized).strip().lower()


def validate_range(value: float, minimum: float, maximum: float) -> float:
    """Valida un valor numérico finito en un intervalo cerrado."""
    for name, number in (
        ("value", value),
        ("minimum", minimum),
        ("maximum", maximum),
    ):
        if isinstance(number, bool) or not isinstance(number, (int, float)):
            raise TypeError(f"{name} debe ser numérico")
        if not math.isfinite(number):
            raise ValueError(f"{name} debe ser finito")

    if minimum > maximum:
        raise ValueError("minimum no puede superar maximum")
    if not minimum <= value <= maximum:
        raise ValueError("value está fuera del rango permitido")
    return float(value)


def transform_feature(value: float, minimum: float, maximum: float) -> float:
    """Escala un valor al intervalo [0, 1] mediante min-max."""
    validate_range(value, minimum, maximum)
    if minimum == maximum:
        raise ValueError("minimum y maximum deben ser distintos")
    return (value - minimum) / (maximum - minimum)
