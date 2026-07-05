from modules.logger import get_logger
from modules.data_loader import load_market_data
from modules.feature_engineering import create_features
from modules.predictor import load_best_model
from modules.backtester import Backtester
import pandas as pd
import matplotlib.pyplot as plt

logger = get_logger()


FEATURE_COLUMNS = [

    "RSI",
    "MOM",

    "MACD",
    "MACD_SIGNAL",
    "MACD_HIST",

    "BB_LOWER",
    "BB_MIDDLE",
    "BB_UPPER",

    "SMA20",
    "SMA50",

    "EMA20",

    "ATR",

    "RETURN",
    "VOLATILITY",

    "VOLUME_CHANGE"

]


def main():

    logger.info("เริ่ม Backtest")

    # =====================================
    # Load Market Data
    # =====================================

    df = load_market_data()

    if df is None:

        logger.error("โหลดข้อมูลไม่สำเร็จ")

        return

    df = create_features(df)

    logger.info(f"ข้อมูลทั้งหมด : {len(df)} แถว")

    # =====================================
    # Load AI Model
    # =====================================

    model = load_best_model()

    if model is None:

        logger.error("โหลดโมเดลไม่สำเร็จ")

        return

    # =====================================
    # Create Backtester
    # =====================================

    tester = Backtester()

    # =====================================
    # Start Backtest
    # =====================================

    for i in range(len(df) - 1):

        current = df.iloc[i]
        next_row = df.iloc[i + 1]

        X = current[FEATURE_COLUMNS].to_frame().T

        prediction = model.predict(X)[0]

        entry = float(current["Close"])
        atr = float(current["ATR"])

        # =====================================
        # BUY
        # =====================================

        if prediction == 1:

            stop_loss = entry - (atr * 2)
            take_profit = entry + (atr * 4)

            if next_row["Low"] <= stop_loss:

                exit_price = stop_loss

            elif next_row["High"] >= take_profit:

                exit_price = take_profit

            else:

                exit_price = float(next_row["Close"])

        # =====================================
        # SELL
        # =====================================

        else:

            stop_loss = entry + (atr * 2)
            take_profit = entry - (atr * 4)

            if next_row["High"] >= stop_loss:

                exit_price = stop_loss

            elif next_row["Low"] <= take_profit:

                exit_price = take_profit

            else:

                exit_price = float(next_row["Close"])

        # =====================================
        # Calculate Profit
        # =====================================

        profit = tester.calculate_profit(

            entry,
            exit_price,
            prediction

        )

        tester.add_trade(profit)

    # =====================================
    # Summary
    # =====================================

    result = tester.get_summary()
    # =====================================
    # Export Trade History
    # =====================================

    trade_df = pd.DataFrame({

        "Trade": range(
            1,
            len(tester.trade_history) + 1
        ),

        "Profit": tester.trade_history,

        "Balance": tester.equity_curve

    })

    trade_df.to_csv(

        "reports/trade_history.csv",

        index=False

)

    logger.info("Export trade_history.csv สำเร็จ")
    # =====================================
    # Equity Curve
    # =====================================

    plt.figure(figsize=(12,6))

    plt.plot(

        tester.equity_curve,

        linewidth=2

    )

    plt.title("Crypto AI Bot Equity Curve")

    plt.xlabel("Trades")

    plt.ylabel("Balance ($)")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(

        "reports/equity_curve.png"

    )

    plt.close()

    logger.info("Export equity_curve.png สำเร็จ")

    print()

    print("========== Backtest ==========")

    print(f"Initial Capital : ${result['initial_balance']:.2f}")
    print(f"Final Capital   : ${result['final_balance']:.2f}")
    print(f"Profit          : ${result['profit']:.2f}")
    print(f"Return          : {result['return']:.2f}%")

    print()

    print(f"Trades          : {result['trades']}")
    print(f"Wins            : {result['wins']}")
    print(f"Losses          : {result['losses']}")
    print(f"Win Rate        : {result['win_rate']:.2f}%")
    print()

    print(f"Profit Factor : {result['profit_factor']:.2f}")

    print(f"Average Win   : ${result['avg_win']:.2f}")

    print(f"Average Loss  : ${result['avg_loss']:.2f}")

    print(f"Max Drawdown  : {result['max_drawdown']:.2f}%")
    print("===============================")


if __name__ == "__main__":

    main()