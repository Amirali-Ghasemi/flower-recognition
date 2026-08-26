"""Model serving layer: cached loading and single/batch inference."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field

import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image

from src import config


@dataclass
class Prediction:
    class_name: str
    confidence: float
    latency_ms: float
    ranked: list[tuple[str, float]] = field(default_factory=list)
    probabilities: dict[str, float] = field(default_factory=dict)


@st.cache_resource(show_spinner=False)
def load_model() -> tf.keras.Model:
    return tf.keras.models.load_model(str(config.MODEL_PATH), compile=False)


@st.cache_data(show_spinner=False)
def load_class_names() -> list[str]:
    return json.loads(config.CLASS_NAMES_PATH.read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_metadata() -> dict:
    return json.loads(config.METADATA_PATH.read_text(encoding="utf-8"))


def preprocess(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB").resize((config.IMG_WIDTH, config.IMG_HEIGHT))
    array = np.asarray(image, dtype=np.float32)
    return np.expand_dims(array, axis=0)


def predict(model: tf.keras.Model, image: Image.Image) -> Prediction:
    class_names = load_class_names()
    batch = preprocess(image)

    start = time.perf_counter()
    probs = model.predict(batch, verbose=0)[0]
    latency_ms = (time.perf_counter() - start) * 1000.0

    order = np.argsort(probs)[::-1]

    return Prediction(
        class_name=class_names[int(order[0])],
        confidence=float(probs[int(order[0])]),
        latency_ms=latency_ms,
        ranked=[(class_names[int(i)], float(probs[int(i)])) for i in order[: config.MAX_TOP_K]],
        probabilities={class_names[int(i)]: float(probs[int(i)]) for i in order},
    )
