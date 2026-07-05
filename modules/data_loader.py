import os
from datetime import datetime

import pandas as pd
import yfinance as yf

from config import TICKER, PERIOD, INTERVAL
from modules.logger import get_logger

logger = get_logger()


def load_market_data(save_csv=True):
    """
    โหลดข้อมูลจาก Yahoo Finance
    """

    logger.info(f"กำลังโหลดข้อมูล {TICKER}")

    try:

        df = yf.download(
            TICKER,
            period=PERIOD,
            interval=INTERVAL,
            auto_adjust=True,
            progress=False
        )

        if df.empty:
            raise Exception("โหลดข้อมูลไม่ได้")

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        logger.info(f"โหลดสำเร็จ ({len(df)} แถว)")

        if save_csv:

            os.makedirs("data", exist_ok=True)

            filename = datetime.now().strftime("%Y%m%d_%H%M%S")

            df.to_csv(f"data/{filename}.csv")

            logger.info(f"💾 บันทึกข้อมูล -> data/{filename}.csv")

        return df

    except Exception as e:

        logger.error("❌ โหลดข้อมูลไม่สำเร็จ")

        logger.error(e)

        return None