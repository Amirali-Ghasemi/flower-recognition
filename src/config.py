"""Central configuration: paths, model constants, and app settings."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
CHECKPOINT_DIR = ARTIFACTS_DIR / "checkpoints"
PRODUCTION_DIR = CHECKPOINT_DIR / "production_artifacts"
METRICS_DIR = ARTIFACTS_DIR / "metrics"
PLOTS_DIR = ARTIFACTS_DIR / "plots"

MODEL_PATH = PRODUCTION_DIR / "flower_efficientnetb0_production.keras"
CLASS_NAMES_PATH = PRODUCTION_DIR / "class_names.json"
METADATA_PATH = PRODUCTION_DIR / "model_metadata.json"

CLASSIFICATION_REPORT_PATH = METRICS_DIR / "final_test_classification_report.txt"
LEARNING_CURVE_PATH = PLOTS_DIR / "learning_dynamics_curve.png"
CONFUSION_MATRIX_PATH = PLOTS_DIR / "normalized_test_confusion_matrix.png"

IMG_HEIGHT = 224
IMG_WIDTH = 224
IMG_SIZE = (IMG_HEIGHT, IMG_WIDTH)

DEFAULT_TOP_K = 5
MAX_TOP_K = 17

SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "bmp", "webp"]
UPLOAD_TYPE = ["jpg", "jpeg", "png", "bmp", "webp"]

APP_TITLE = "BloomID"
APP_TAGLINE = "Flower Species Classifier · EfficientNetB0 Transfer Learning"

TEST_METRICS = {
    "accuracy": 0.8824,
    "top_3_accuracy": 1.0000,
    "macro_f1": 0.8509,
    "test_samples": 85,
}
