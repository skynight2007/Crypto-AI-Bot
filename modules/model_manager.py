import os
import joblib

from modules.logger import get_logger

logger = get_logger()


MODEL_PATH = "models/model.pkl"


def save_model(model):

    os.makedirs("models", exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    logger.info(f"บันทึกโมเดล -> {MODEL_PATH}")


def load_model():

    if not os.path.exists(MODEL_PATH):

        logger.warning("ยังไม่มีโมเดล")

        return None

    logger.info("โหลดโมเดลสำเร็จ")

    return joblib.load(MODEL_PATH)