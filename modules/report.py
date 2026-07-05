import os

from datetime import datetime

import pandas as pd

from modules.logger import get_logger

logger = get_logger()


def save_report(
    signal,
    confidence,
    strategy
):
    """
    บันทึกผลการวิเคราะห์เป็น CSV
    """

    os.makedirs(
        "reports",
        exist_ok=True
    )

    now = datetime.now()

    filename = now.strftime(
        "%Y%m%d_%H%M%S"
    )

    report = pd.DataFrame([{

        "datetime": now,

        "signal": signal,

        "confidence": round(
            confidence,
            2
        ),

        "entry": strategy["entry"],

        "stop_loss": strategy["stop_loss"],

        "take_profit": strategy["take_profit"],

        "risk": strategy["risk"],

        "rr_ratio": strategy["rr_ratio"]

    }])

    path = f"reports/{filename}.csv"

    report.to_csv(
        path,
        index=False
    )

    logger.info(
        f"บันทึกรายงาน -> {path}"
    )

    return path