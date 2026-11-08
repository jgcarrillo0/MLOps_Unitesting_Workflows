"""Endpoints HTTP sobre funciones de preprocesamiento."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.preprocessing import clean_text, transform_feature, validate_range

app = FastAPI(title="Preprocessing API", version="0.1.0")


class TextInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str


class NumberInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: float = Field(allow_inf_nan=False)
    minimum: float = Field(allow_inf_nan=False)
    maximum: float = Field(allow_inf_nan=False)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/clean-text")
def clean_text_endpoint(payload: TextInput) -> dict[str, str]:
    return {"result": clean_text(payload.text)}


@app.post("/validate-range")
def validate_range_endpoint(payload: NumberInput) -> dict[str, float]:
    try:
        result = validate_range(
            payload.value, payload.minimum, payload.maximum
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"result": result}


@app.post("/transform-feature")
def transform_feature_endpoint(payload: NumberInput) -> dict[str, float]:
    try:
        result = transform_feature(
            payload.value, payload.minimum, payload.maximum
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"result": result}
