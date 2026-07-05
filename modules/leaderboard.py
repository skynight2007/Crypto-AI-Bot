from modules.logger import get_logger

logger = get_logger()


def show_leaderboard(results):
    """
    แสดงอันดับโมเดล
    """

    ranking = sorted(

        results.items(),

        key=lambda x: x[1]["accuracy"],

        reverse=True

    )

    logger.info("")

    logger.info("=" * 45)

    logger.info("🏆 AI Leaderboard")

    logger.info("=" * 45)

    for i, (name, score) in enumerate(

        ranking,

        start=1

    ):

        logger.info(

            f"{i}. {name:20}"

            f"{score['accuracy']:.2%}"

        )

    logger.info("=" * 45)

    return ranking[0][0]