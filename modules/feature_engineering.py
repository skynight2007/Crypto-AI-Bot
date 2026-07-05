import numpy as np
import pandas_ta as ta

from config import (
    RSI_LENGTH,
    MOM_LENGTH,
    BB_LENGTH,
    BB_STD
)


def create_features(df):

    df = df.copy()

    # RSI
    df["RSI"] = ta.rsi(df["Close"], length=RSI_LENGTH)

    # Momentum
    df["MOM"] = ta.mom(df["Close"], length=MOM_LENGTH)

    # MACD
    macd = ta.macd(df["Close"])

    df["MACD"] = macd.iloc[:, 0]
    df["MACD_SIGNAL"] = macd.iloc[:, 1]
    df["MACD_HIST"] = macd.iloc[:, 2]

    # Bollinger
    bb = ta.bbands(
    df["Close"],
    length=BB_LENGTH,
    std=BB_STD
    )

    df["BB_LOWER"] = bb.iloc[:, 0]
    df["BB_MIDDLE"] = bb.iloc[:, 1]
    df["BB_UPPER"] = bb.iloc[:, 2]

    # Moving Average
    df["SMA20"] = ta.sma(df["Close"], length=20)
    df["SMA50"] = ta.sma(df["Close"], length=50)

    df["EMA20"] = ta.ema(df["Close"], length=20)

    # ATR (Average True Range)
    df["ATR"] = ta.atr(
        df["High"],
        df["Low"],
        df["Close"],
        length=14
    )

    # Daily Return
    df["RETURN"] = df["Close"].pct_change()

    # Volatility
    df["VOLATILITY"] = (
        df["RETURN"]
        .rolling(10)
        .std()
    )

    # Volume Change
    df["VOLUME_CHANGE"] = (
        df["Volume"]
        .pct_change()
    )

    # Target
    df["TARGET"] = np.where(
        df["Close"].shift(-1) > df["Close"],
        1,
        0
    )

    df.dropna(inplace=True)

    return df