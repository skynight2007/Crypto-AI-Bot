from datetime import datetime

from config import TICKER


def create_embed(
    signal,
    confidence,
    strategy
):
    """
    สร้าง Discord Embed
    """

    # ------------------------
    # Embed Color
    # ------------------------

    if signal == "🟢 BUY":

        color = 0x00FF00

    elif signal == "🔴 SELL":

        color = 0xFF0000

    else:

        color = 0x808080

    # ------------------------
    # Embed
    # ------------------------

    embed = {

        "title": "🤖 Crypto AI Bot",

        "color": color,

        "fields": [

            {

                "name": "Coin",

                "value": TICKER,

                "inline": True

            },

            {

                "name": "Signal",

                "value": signal,

                "inline": True

            },

            {

                "name": "Confidence",

                "value": f"{confidence:.2f}%",

                "inline": True

            }

        ],

        "footer": {

            "text": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        }

    }

    # ------------------------
    # Strategy
    # ------------------------

    if signal != "⚪ NO TRADE":

        embed["fields"].extend([

            {

                "name": "Entry",

                "value": f"{strategy['entry']:.2f}",

                "inline": True

            },

            {

                "name": "Stop Loss",

                "value": f"{strategy['sl']:.2f}",

                "inline": True

            },

            {

                "name": "Take Profit",

                "value": f"{strategy['tp']:.2f}",

                "inline": True

            },

            {

                "name": "Risk",

                "value": strategy["risk"],

                "inline": True

            },

            {

                "name": "Reward / Risk",

                "value": f"{strategy['rr']:.2f}",

                "inline": True

            }

        ])

    else:

        embed["fields"].append(

            {

                "name": "Status",

                "value": "Confidence ต่ำกว่า 60%",

                "inline": False

            }

        )

    return embed