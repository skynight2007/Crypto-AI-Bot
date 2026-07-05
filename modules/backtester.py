from config import (
    INITIAL_BALANCE,
    POSITION_SIZE,
    TRADING_FEE
)

from modules.logger import get_logger

logger = get_logger()


class Backtester:

    def __init__(self):

        # ==========================
        # Portfolio
        # ==========================

        self.initial_balance = INITIAL_BALANCE
        self.balance = INITIAL_BALANCE

        self.position_size = POSITION_SIZE
        self.trading_fee = TRADING_FEE

        # ==========================
        # Statistics
        # ==========================

        self.total_trades = 0
        self.win = 0
        self.loss = 0

        # ==========================
        # History
        # ==========================

        self.trade_history = []

        self.equity_curve = []

        # ==========================
        # Profit Tracking
        # ==========================

        self.gross_profit = 0.0
        self.gross_loss = 0.0

    # ==========================================================
    # Calculate Profit
    # ==========================================================

    def calculate_profit(
        self,
        entry,
        exit_price,
        signal
    ):

        capital = self.balance * self.position_size

        # BUY
        if signal == 1:

            change = (exit_price - entry) / entry

        # SELL
        else:

            change = (entry - exit_price) / entry

        fee = capital * self.trading_fee * 2

        gross_profit = capital * change

        net_profit = gross_profit - fee

        return net_profit

    # ==========================================================
    # Add Trade
    # ==========================================================

    def add_trade(self, profit):

        self.total_trades += 1

        self.balance += profit

        self.trade_history.append(profit)

        self.equity_curve.append(self.balance)

        if profit > 0:

            self.win += 1

            self.gross_profit += profit

        else:

            self.loss += 1

            self.gross_loss += abs(profit)

    # ==========================================================
    # Profit Factor
    # ==========================================================

    def profit_factor(self):

        if self.gross_loss == 0:

            return 999.0

        return self.gross_profit / self.gross_loss

    # ==========================================================
    # Average Win
    # ==========================================================

    def average_win(self):

        wins = [

            x

            for x in self.trade_history

            if x > 0

        ]

        if len(wins) == 0:

            return 0

        return sum(wins) / len(wins)

    # ==========================================================
    # Average Loss
    # ==========================================================

    def average_loss(self):

        losses = [

            x

            for x in self.trade_history

            if x < 0

        ]

        if len(losses) == 0:

            return 0

        return abs(sum(losses) / len(losses))

    # ==========================================================
    # Maximum Drawdown
    # ==========================================================

    def max_drawdown(self):

        peak = self.initial_balance

        max_dd = 0

        for balance in self.equity_curve:

            if balance > peak:

                peak = balance

            drawdown = (peak - balance) / peak

            if drawdown > max_dd:

                max_dd = drawdown

        return max_dd * 100

    # ==========================================================
    # Summary
    # ==========================================================

    def get_summary(self):

        if self.total_trades == 0:

            win_rate = 0

        else:

            win_rate = (

                self.win / self.total_trades

            ) * 100

        return {

            "initial_balance": self.initial_balance,

            "final_balance": self.balance,

            "profit": self.balance - self.initial_balance,

            "return": (

                (self.balance - self.initial_balance)

                / self.initial_balance

            ) * 100,

            "trades": self.total_trades,

            "wins": self.win,

            "losses": self.loss,

            "win_rate": win_rate,

            "profit_factor": self.profit_factor(),

            "avg_win": self.average_win(),

            "avg_loss": self.average_loss(),

            "max_drawdown": self.max_drawdown()

        }