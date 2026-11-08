"""Pruebas unitarias de las funciones puras."""

import pytest
from app.preprocessing import clean_text, transform_feature, validate_range


def test_clean_text_normaliza_espacios_y_mayusculas() -> None:
    assert clean_text("  HOLA  \n MUNDO  ") == "hola mundo"


def test_clean_text_vacio() -> None:
    assert clean_text(" \t\n ") == ""


def test_clean_text_preserva_tildes() -> None:
    assert clean_text("  ÁRBOL,   CAFÉ ") == "árbol, café"


def test_clean_text_rechaza_tipo_invalido() -> None:
    with pytest.raises(TypeError, match="texto"):
        clean_text(None)  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [0, 100])
def test_validate_range_acepta_limites(value: int) -> None:
    assert validate_range(value, 0, 100) == value


def test_validate_range_rechaza_fuera_de_rango() -> None:
    with pytest.raises(ValueError, match="fuera del rango"):
        validate_range(101, 0, 100)


def test_validate_range_rechaza_limites_invertidos() -> None:
    with pytest.raises(ValueError, match="superar"):
        validate_range(50, 100, 0)


def test_transform_feature_escala_correctamente() -> None:
    assert transform_feature(25, 0, 100) == pytest.approx(0.25)


def test_transform_feature_rechaza_intervalo_degenerado() -> None:
    with pytest.raises(ValueError, match="distintos"):
        transform_feature(5, 5, 5)


def test_validate_range_rechaza_nan() -> None:
    with pytest.raises(ValueError, match="finito"):
        validate_range(float("nan"), 0, 100)
