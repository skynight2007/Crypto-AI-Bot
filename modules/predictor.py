import joblib

from modules.logger import get_logger

logger = get_logger()


def load_best_model():
    """
    โหลดโมเดลที่ดีที่สุด
    """

    try:

        model = joblib.load("models/model.pkl")

        logger.info("โหลดโมเดลสำเร็จ")

        return model

    except Exception as e:

        logger.error(e)

        return None


def predict_latest(model, df):
    """
    ทำนายข้อมูลล่าสุด
    """

    feature_columns = [

        "RSI",
        "MOM",

        "MACD",
        "MACD_SIGNAL",
        "MACD_HIST",

        "BB_LOWER",
        "BB_MIDDLE",
        "BB_UPPER",

        "SMA20",
        "SMA50",

        "EMA20",

        "ATR",

        "RETURN",
        "VOLATILITY",

        "VOLUME_CHANGE"

    ]

    latest = df[feature_columns].tail(1)

    prediction = model.predict(latest)[0]

    probability = model.predict_proba(latest)[0]

    return prediction, probability


def show_prediction(prediction, probability):
    """
    แสดงผลการทำนาย
    """

    if prediction == 1:

        signal = "🟢 BUY"

        confidence = probability[1] * 100

    else:

        signal = "🔴 SELL"

        confidence = probability[0] * 100

    logger.info("")
    logger.info("========== Prediction ==========")
    logger.info(f"Signal      : {signal}")
    logger.info(f"Confidence  : {confidence:.2f}%")
    logger.info("===============================")

    return signal, confidence