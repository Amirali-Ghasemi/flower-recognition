"""Presentation layer: custom styling, layout components and charts."""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

ACCENT = "#22c55e"
ACCENT_SOFT = "rgba(34, 197, 94, 0.12)"
TEXT_PRIMARY = "#f1f5f9"
TEXT_MUTED = "#94a3b8"

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(1100px 500px at 85% -10%, rgba(34, 197, 94, 0.10), transparent 60%),
            radial-gradient(900px 450px at -10% 110%, rgba(16, 185, 129, 0.08), transparent 60%),
            #0b1220;
    }

    #MainMenu, footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0e1729 0%, #0b1220 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }
    section[data-testid="stSidebar"] * {color: #e2e8f0 !important;}

    div[data-testid="stMetric"] {
        background: rgba(148, 163, 184, 0.06);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 14px;
        padding: 14px 18px;
    }

    .hero-card {
        background: linear-gradient(135deg, rgba(34,197,94,0.16) 0%, rgba(14,23,41,0.65) 55%);
        border: 1px solid rgba(34, 197, 94, 0.35);
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 8px;
    }
    .hero-card h1 {font-size: 2.4rem; font-weight: 800; color: #ffffff; margin: 0;}
    .hero-card p  {color: #cbd5e1; font-size: 1.05rem; margin: 6px 0 0 0;}

    .prediction-panel {
        background: linear-gradient(135deg, rgba(34,197,94,0.20), rgba(15,23,42,0.70));
        border: 1px solid rgba(34, 197, 94, 0.40);
        border-radius: 18px;
        padding: 24px 28px;
        text-align: center;
    }
    .prediction-panel .emoji   {font-size: 3.6rem; line-height: 1;}
    .prediction-panel .species {font-size: 1.9rem; font-weight: 800; color: #ffffff; margin-top: 8px;}
    .prediction-panel .latin   {color: #a7f3d0; font-size: 0.95rem; text-transform: capitalize; letter-spacing: 0.5px;}
    .prediction-panel .conf    {font-size: 2.6rem; font-weight: 800; color: #22c55e; margin-top: 10px;}
    .prediction-panel .conf-lbl{color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px;}

    .section-title {
        font-size: 1.05rem; font-weight: 700; color: #e2e8f0;
        text-transform: uppercase; letter-spacing: 1.5px;
        margin: 18px 0 4px 0;
        display: flex; align-items: center; gap: 8px;
    }

    .flower-card {
        background: rgba(148, 163, 184, 0.06);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px;
        padding: 16px 18px;
        height: 100%;
    }
    .flower-card .name {font-weight: 700; color: #f1f5f9; font-size: 1rem;}
    .flower-card .meta {color: #94a3b8; font-size: 0.82rem; margin-bottom: 6px;}
    .flower-card .desc {color: #cbd5e1; font-size: 0.88rem;}

    .upload-hint {
        color: #64748b; text-align: center; font-size: 0.92rem; padding: 30px 10px;
        border: 1.5px dashed rgba(148,163,184,0.30); border-radius: 16px;
    }

    div[data-testid="stFileUploaderDropzone"] {
        border: 1.5px dashed rgba(34, 197, 94, 0.45);
        background: rgba(34, 197, 94, 0.04);
        border-radius: 16px;
    }

    .stTabs [data-baseweb="tab-list"] {gap: 6px;}
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
    }
</style>
"""


def apply_theme() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def hero() -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <h1>🌼 BloomID <span style="font-size:1.1rem;font-weight:600;color:{ACCENT};">v1.0</span></h1>
            <p>Deep-learning flower species identification — upload a photo and get instant
            predictions powered by a fine-tuned <b>EfficientNetB0</b> network (17 species).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(icon: str, text: str) -> None:
    st.markdown(f'<div class="section-title">{icon}&nbsp;&nbsp;{text}</div>', unsafe_allow_html=True)


def prediction_panel(class_name: str, emoji: str, common_name: str, confidence: float) -> None:
    st.markdown(
        f"""
        <div class="prediction-panel">
            <div class="emoji">{emoji}</div>
            <div class="species">{common_name}</div>
            <div class="latin">{class_name.replace('_', ' ')}</div>
            <div class="conf">{confidence * 100:.1f}%</div>
            <div class="conf-lbl">Model Confidence</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def flower_card(class_name: str, family: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="flower-card">
            <div class="name">{class_name.replace('_', ' ').title()}</div>
            <div class="meta">{family}</div>
            <div class="desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def probability_chart(ranked: list[tuple[str, float]], top_k: int = 5) -> alt.Chart:
    data = pd.DataFrame(ranked[:top_k], columns=["Species", "Confidence"])
    data["Label"] = data["Species"].str.replace("_", " ").str.title()

    chart = (
        alt.Chart(data)
        .encode(
            x=alt.X("Confidence:Q", axis=alt.Axis(format="%", grid=False), scale=alt.Scale(domain=[0, 1])),
            y=alt.Y(
                "Label:N",
                sort=alt.EncodingSortField(field="Confidence", order="descending"),
                axis=alt.Axis(labelColor="#e2e8f0", title=None),
            ),
            color=alt.condition(
                alt.datum.Label == data.iloc[0]["Label"],
                alt.value(ACCENT),
                alt.value("rgba(148, 163, 184, 0.45)"),
            ),
            tooltip=[alt.Tooltip("Species:N", title="Class"), alt.Tooltip("Confidence:Q", format=".2%")],
        )
        .mark_bar(cornerRadius=4, height=22)
        .properties(height=34 * len(data) + 30)
        .configure(background="transparent")
        .configure_view(stroke=None)
        .configure_axis(labelFontSize=12, gridColor="rgba(148,163,184,0.10)", domainColor="rgba(148,163,184,0.25)")
    )
    return chart


def full_distribution_chart(probabilities: dict[str, float]) -> alt.Chart:
    data = pd.DataFrame(list(probabilities.items()), columns=["Species", "Confidence"])
    data["Label"] = data["Species"].str.replace("_", " ").str.title()

    chart = (
        alt.Chart(data)
        .encode(
            x=alt.X("Confidence:Q", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1])),
            y=alt.Y(
                "Label:N",
                sort=alt.EncodingSortField(field="Confidence", order="descending"),
                axis=alt.Axis(title=None),
            ),
            color=alt.value("rgba(148, 163, 184, 0.55)"),
            tooltip=[alt.Tooltip("Confidence:Q", format=".3%")],
        )
        .mark_bar(cornerRadius=3)
        .properties(height=26 * len(data) + 30)
        .configure(background="transparent")
        .configure_view(stroke=None)
        .configure_axis(labelFontSize=11, gridColor="rgba(148,163,184,0.10)")
    )
    return chart


def confidence_badge(confidence: float) -> str:
    if confidence >= 0.75:
        return "🟢 High confidence"
    if confidence >= 0.45:
        return "🟡 Moderate confidence"
    return "🔴 Low confidence — prediction may be unreliable"
