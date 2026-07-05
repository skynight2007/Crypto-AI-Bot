from modules.logger import get_logger

logger = get_logger()


def filter_signal(signal, confidence):
    """
    กรองสัญญาณตามระดับความมั่นใจ
    """

    if confidence >= 80:

        level = "★★★★★"

        action = signal

        message = "Strong Signal"

    elif confidence >= 70:

        level = "★★★★"

        action = signal

        message = "Good Signal"

    elif confidence >= 60:

        level = "★★★"

        action = signal

        message = "Weak Signal"

    else:

        level = "✖"

        action = "⚪ NO TRADE"

        message = "Confidence ต่ำเกินไป"

    logger.info(
    f"Confidence Filter : {action} ({confidence:.2f}%)"
    )

    return {

        "action": action,

        "level": level,

        "message": message

    }