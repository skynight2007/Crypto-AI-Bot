from modules.logger import get_logger
from modules.data_loader import load_market_data
from modules.feature_engineering import create_features
from modules.trainer import train_all_models
from modules.strategy import create_strategy
from modules.filter import filter_signal
from modules.discord_embed import create_embed
from modules.notifier import send_discord
from modules.predictor import (
    load_best_model,
    predict_latest,
    show_prediction
)

logger = get_logger()


def main():

    logger.info("เริ่มต้นโปรแกรม")

    # ==========================
    # Load Market Data
    # ==========================

    df = load_market_data()

    if df is None:
        logger.error("โหลดข้อมูลไม่สำเร็จ")
        return

    # ==========================
    # Feature Engineering
    # ==========================

    df = create_features(df)

    logger.info(f"จำนวนข้อมูลทั้งหมด {len(df)} แถว")
    logger.info(f"จำนวน Feature ทั้งหมด {len(df.columns)} คอลัมน์")

    # ==========================
    # Train Models
    # ==========================


    # ==========================
    # Load Best Model
    # ==========================

    model = load_best_model()

    if model is None:
        logger.error("โหลดโมเดลไม่สำเร็จ")
        return

    # ==========================
    # Predict Latest Candle
    # ==========================

    prediction, probability = predict_latest(
        model,
        df
    )

    signal, confidence = show_prediction(
        prediction,
        probability
    )

    # ==========================
    # Confidence Filter
    # ==========================

    filter_result = filter_signal(
        signal,
        confidence
    )

    # ==========================
    # Create Strategy
    # ==========================
    latest_row = df.iloc[-1]

    strategy = create_strategy(
    filter_result["action"],
    confidence,
    latest_row
    )
    # ==========================
    # Discord Alert
    # ==========================

    embed = create_embed(
        filter_result["action"],
        confidence,
        strategy
    )
    send_discord(embed)
    # ==========================
    # Result
    # ==========================

    # ==========================
    # AI Signal
    # ==========================

    print()
    print("========== AI Signal ==========")

    print(f"Signal      : {filter_result['action']}")
    print(f"Confidence  : {confidence:.2f}%")
    print(f"Level       : {filter_result['level']}")
    print(f"Status      : {filter_result['message']}")

    print("===============================")

    # ==========================
    # Strategy
    # ==========================

    print()
    print("========== Strategy ==========")

    if strategy["signal"] == "⚪ NO TRADE":

        print("NO TRADE")
        print("Confidence ต่ำเกินไป")

    else:

        print(f"Entry Price : {strategy['entry']:.2f}")
        print(f"Stop Loss   : {strategy['sl']:.2f}")
        print(f"Take Profit : {strategy['tp']:.2f}")
        print(f"Risk Level  : {strategy['risk']}")
        print(f"R/R Ratio   : {strategy['rr']:.2f}")

    print("===============================")

    # ==========================
    # Latest Data
    # ==========================

    print()
    print(df.tail())


if __name__ == "__main__":
    main()