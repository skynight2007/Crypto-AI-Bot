"""
Crypto AI Bot Configuration
"""

# =====================================
# Market
# =====================================

TICKER = "BTC-USD"

PERIOD = "5y"

INTERVAL = "1d"

# =====================================
# AI
# =====================================

TEST_SIZE = 0.20

RANDOM_STATE = 42

CONFIDENCE_THRESHOLD = 60

# =====================================
# Technical Indicator
# =====================================

RSI_LENGTH = 14

MOM_LENGTH = 10

BB_LENGTH = 20

BB_STD = 2

ATR_LENGTH = 14

# =====================================
# Risk Management
# =====================================

RISK_REWARD_RATIO = 2.0

ATR_MULTIPLIER = 2.0

# =====================================
# Model
# =====================================

MODEL_PATH = "models/model.pkl"

# =====================================
# Discord
# =====================================

DISCORD_USERNAME = "Crypto AI Bot"

DISCORD_AVATAR = ""
# ==========================
# Backtest
# ==========================

INITIAL_BALANCE = 1000

POSITION_SIZE = 0.10

# ==========================
# Backtest Settings
# ==========================

INITIAL_BALANCE = 1000

POSITION_SIZE = 0.10

TRADING_FEE = 0.001