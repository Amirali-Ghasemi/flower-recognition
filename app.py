"""BloomID — Flower Species Classification Web App.

Entry point for the Streamlit application serving the fine-tuned
EfficientNetB0 flower classifier (17 classes).
"""

from __future__ import annotations

import io

import pandas as pd
import streamlit as st
from PIL import Image

from src import config, inference, ui
from src.flower_data import get_info

st.set_page_config(
    page_title="BloomID · Flower Classifier",
    page_icon="🌼",
    layout="wide",
    initial_sidebar_state="expanded",
)

ui.apply_theme()


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("## 🌼 BloomID")
        st.caption(config.APP_TAGLINE)
        st.divider()

        page = st.radio(
            "Navigation",
            ["🔮 Classify", "🗂️ Batch Mode", "🧠 Model Card"],
            label_visibility="collapsed",
        )
        st.divider()

        model_ready = config.MODEL_PATH.is_file()
        if model_ready:
            st.markdown(f"<span style='color:{ui.ACCENT};font-size:0.9em;'>● Model loaded</span>", unsafe_allow_html=True)
        else:
            st.error("Production model not found.")

        st.caption(f"Input · {config.IMG_WIDTH}×{config.IMG_HEIGHT} RGB")
        return page


@st.cache_data
def load_report_text() -> str | None:
    if config.CLASSIFICATION_REPORT_PATH.is_file():
        return config.CLASSIFICATION_REPORT_PATH.read_text(encoding="utf-8")
    return None


def page_classify() -> None:
    ui.section_title("🔮", "Single Image Classification")

    col_upload, col_result = st.columns([1.05, 1.3], gap="large")

    with col_upload:
        uploaded = st.file_uploader(
            "Drop a flower photo",
            type=config.UPLOAD_TYPE,
            accept_multiple_files=False,
            help=f"Supported formats: {', '.join(config.SUPPORTED_FORMATS).upper()}",
        )

        image = None
        if uploaded is not None:
            try:
                image = Image.open(io.BytesIO(uploaded.getvalue()))
                st.image(image, use_container_width=True, caption=uploaded.name)
                st.caption(f"Original size: {image.size[0]}×{image.size[1]} px")
            except Exception as exc:
                st.error(f"Could not read this image file: {exc}")
        else:
            st.markdown("<div class='upload-hint'>📤 Upload an image to begin<br><br>"
                        "Best results with a clear, centred flower photo</div>",
                        unsafe_allow_html=True)

    with col_result:
        if image is None:
            st.info("👈 Upload a photo to see the prediction panel.")
            return

        with st.spinner("Analysing petals…"):
            model = inference.load_model()
            prediction = inference.predict(model, image)

        info = get_info(prediction.class_name)
        ui.prediction_panel(prediction.class_name, info["emoji"], info["common_name"], prediction.confidence)

        m1, m2, m3 = st.columns(3)
        m1.metric("Confidence", f"{prediction.confidence:.1%}")
        m2.metric("Latency", f"{prediction.latency_ms:.0f} ms")
        m3.metric("Classes", len(inference.load_class_names()))

        st.caption(ui.confidence_badge(prediction.confidence))

    if image is None:
        return

    top_k = st.slider("Top-K species to display", 3, 10, config.DEFAULT_TOP_K)

    tab_ranked, tab_full, tab_about = st.tabs(["📊 Top Predictions", "📈 Full Distribution", "📖 Species Info"])

    with tab_ranked:
        st.altair_chart(ui.probability_chart(prediction.ranked, top_k), use_container_width=True)

    with tab_full:
        with st.expander("Show all 17 class probabilities", expanded=True):
            st.altair_chart(ui.full_distribution_chart(prediction.probabilities), use_container_width=True)

    with tab_about:
        family, desc = st.columns([0.35, 0.65])
        with family:
            ui.flower_card(prediction.class_name.replace("_", " ").title(), info["family"], "")
        with desc:
            st.markdown(
                f"""
                <div class="flower-card">
                    <div class="name">{info["common_name"]}</div>
                    <div class="desc">{info["description"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def page_batch() -> None:
    ui.section_title("🗂️", "Batch Classification")

    files = st.file_uploader(
        "Upload multiple flower photos",
        type=config.UPLOAD_TYPE,
        accept_multiple_files=True,
    )

    if not files:
        st.markdown("<div class='upload-hint'>📤 Select one or more images<br>"
                    "Results will be compiled into a downloadable table</div>",
                    unsafe_allow_html=True)
        return

    threshold = st.slider(
        "Confidence threshold",
        0.0, 1.0, 0.50, 0.05,
        help="Predictions below this confidence are flagged as uncertain.",
    )

    model = inference.load_model()
    rows: list[dict] = []

    progress = st.progress(0.0, text="Classifying…")
    for idx, file in enumerate(files, start=1):
        try:
            image = Image.open(io.BytesIO(file.getvalue()))
            prediction = inference.predict(model, image)
            rows.append(
                {
                    "File": file.name,
                    "Predicted Species": prediction.class_name.replace("_", " ").title(),
                    "Class Key": prediction.class_name,
                    "Confidence": prediction.confidence,
                    "Runner-up": prediction.ranked[1][0].replace("_", " ").title() if len(prediction.ranked) > 1 else "—",
                    "Status": "⚠️ Uncertain" if prediction.confidence < threshold else "✅ Confident",
                }
            )
        except Exception as exc:
            rows.append({"File": file.name, "Predicted Species": f"Error: {exc}", "Confidence": 0.0})
        progress.progress(idx / len(files), text=f"Classifying… ({idx}/{len(files)})")
    progress.empty()

    results = pd.DataFrame(rows)

    c1, c2, c3 = st.columns(3)
    confident_count = int((results["Status"] == "✅ Confident").sum())
    avg_conf = float(results["Confidence"].mean())
    c1.metric("Images processed", len(results))
    c2.metric("Confident predictions", confident_count)
    c3.metric("Average confidence", f"{avg_conf:.1%}")

    st.dataframe(
        results,
        use_container_width=True,
        column_config={
            "Confidence": st.column_config.ProgressColumn(
                "Confidence", format="%.2f", min_value=0.0, max_value=1.0,
            ),
        },
        hide_index=True,
    )

    csv = results.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download results as CSV",
        data=csv,
        file_name="bloomid_predictions.csv",
        mime="text/csv",
        use_container_width=True,
    )


def page_model_card() -> None:
    ui.section_title("🧠", "Model Card")

    metadata = inference.load_metadata()
    metrics = config.TEST_METRICS

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Test Accuracy", f"{metrics['accuracy']:.2%}")
    c2.metric("Top-3 Accuracy", f"{metrics['top_3_accuracy']:.1%}")
    c3.metric("Macro F1", f"{metrics['macro_f1']:.4f}")
    c4.metric("Test Samples", metrics["test_samples"])

    left, right = st.columns([1, 1.6], gap="large")

    with left:
        st.subheader("Architecture")
        st.markdown(
            f"""
            | Property | Value |
            |---|---|
            | Backbone | **{metadata['architecture']}** |
            | Strategy | Transfer learning (2-phase) |
            | Classes | {metadata['num_classes']} |
            | Input | {metadata['input_shape'][0]}×{metadata['input_shape'][1]}×{metadata['input_shape'][2]} |
            | Output | {metadata['output_activation']} |
            | Format | {metadata['artifact_format']} |
            """
        )
        st.caption("Phase 1: frozen-backbone feature extraction → Phase 2: selective fine-tuning of the top 35 layers.")

        st.subheader("Species Coverage")
        cols = st.columns(3)
        names = inference.load_class_names()
        for i, name in enumerate(names):
            info = get_info(name)
            with cols[i % 3]:
                st.markdown(f"{info['emoji']} **{name.replace('_', ' ').title()}**")

    with right:
        st.subheader("Training Dynamics")
        if config.LEARNING_CURVE_PATH.is_file():
            st.image(str(config.LEARNING_CURVE_PATH), use_container_width=True)
        else:
            st.warning("Learning-curve plot not found in artifacts.")

        st.subheader("Test Confusion Matrix")
        if config.CONFUSION_MATRIX_PATH.is_file():
            with st.expander("View normalized confusion matrix", expanded=False):
                st.image(str(config.CONFUSION_MATRIX_PATH), use_container_width=True)

        report = load_report_text()
        if report:
            with st.expander("Full classification report"):
                st.code(report, language=None)


def main() -> None:
    ui.hero()
    page = render_sidebar()

    st.divider()

    if page == "🔮 Classify":
        page_classify()
    elif page == "🗂️ Batch Mode":
        page_batch()
    else:
        page_model_card()

    st.divider()
    st.caption(
        "Built with Streamlit · TensorFlow / Keras EfficientNetB0 · "
        "For research and educational use."
    )


if __name__ == "__main__":
    main()
