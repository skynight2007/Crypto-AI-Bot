from modules.logger import get_logger

logger = get_logger()


def create_strategy(signal, confidence, latest_row):
    """
    สร้างแผนการเข้าเทรด
    """

    strategy = {

        "signal": signal,

        "confidence": confidence,

        "entry": None,

        "sl": None,

        "tp": None,

        "risk": "NO TRADE",

        "rr": 0.0

    }

    # -------------------------
    # Confidence Filter
    # -------------------------

    if signal == "⚪ NO TRADE":

        logger.info("ไม่สร้าง Strategy")

        return strategy

    entry = latest_row["Close"]

    atr = latest_row["ATR"]

    # -------------------------
    # BUY
    # -------------------------

    if signal == "🟢 BUY":

        sl = entry - (atr * 2)

        tp = entry + (atr * 4)

    # -------------------------
    # SELL
    # -------------------------

    else:

        sl = entry + (atr * 2)

        tp = entry - (atr * 4)

    risk = abs(entry - sl)

    reward = abs(tp - entry)

    rr = reward / risk

    strategy["entry"] = entry

    strategy["sl"] = sl

    strategy["tp"] = tp

    strategy["rr"] = rr

    # -------------------------
    # Risk Level
    # -------------------------

    if atr < entry * 0.01:

        strategy["risk"] = "Low"

    elif atr < entry * 0.03:

        strategy["risk"] = "Medium"

    else:

        strategy["risk"] = "High"

    logger.info("สร้าง Strategy สำเร็จ")

    return strategy