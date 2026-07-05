import os
import requests

from modules.logger import get_logger

logger = get_logger()

try:
    from google.colab import userdata
    DISCORD_URL = userdata.get("DISCORD_WEBHOOK_URL")
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL")
    print(DISCORD_URL)
def send_discord(embed_data):
    """
    ส่ง Embed ไป Discord
    """

    if not DISCORD_URL:

        logger.warning("ไม่พบ Discord Webhook")

        return False

    payload = {

        "embeds": [
            embed_data
        ]

    }

    try:

        response = requests.post(

            DISCORD_URL,

            json=payload,

            timeout=10

        )
        

        if response.status_code == 204:

            logger.info("ส่ง Discord สำเร็จ")

            return True

        logger.error(
            f"Discord Error : {response.status_code}"
        )

        return False

    except Exception as e:

        logger.error(e)

        return False