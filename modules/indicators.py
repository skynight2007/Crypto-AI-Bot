import pandas as pd
import pandas_ta as ta

from config import (
    RSI_LENGTH,
    MOM_LENGTH,
    BB_LENGTH,
    BB_STD
)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    เพิ่ม Technical Indicators ลงใน DataFrame
    """

    # RSI
    df["RSI"] = ta.rsi(df["Close"], length=RSI_LENGTH)

    # Momentum
    df["MOM"] = ta.mom(df["Close"], length=MOM_LENGTH)

    # MACD
    macd = ta.macd(df["Close"])

    df["MACD"] = macd.iloc[:, 0]
    df["MACD_SIGNAL"] = macd.iloc[:, 2]

    # Bollinger Bands
    bb = ta.bbands(
        df["Close"],
        length=BB_LENGTH,
        std=BB_STD
    )

    df["BB_LOWER"] = bb.iloc[:, 0]
    df["BB_UPPER"] = bb.iloc[:, 2]

    return df