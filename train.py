from modules.logger import get_logger
from modules.data_loader import load_market_data
from modules.feature_engineering import create_features
from modules.trainer import train_all_models

logger = get_logger()


def main():

    logger.info("========== TRAIN MODEL ==========")

    # โหลดข้อมูล
    df = load_market_data()

    if df is None:
        logger.error("โหลดข้อมูลไม่สำเร็จ")
        return

    # สร้าง Feature
    df = create_features(df)

    logger.info(f"ข้อมูลทั้งหมด {len(df)} แถว")

    # Train AI
    model, results = train_all_models(df)

    print()
    print("========== AI Result ==========")

    for name, score in results.items():

        print(
            f"{name:20}"
            f"{score['accuracy']:.2%}"
        )

    print()
    print("Training Complete.")
    print("Best model saved -> models/model.pkl")


if __name__ == "__main__":
    main()