from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from modules.evaluator import evaluate_model
from modules.leaderboard import show_leaderboard
from modules.model_manager import save_model
from modules.logger import get_logger

from config import (
    TEST_SIZE,
    RANDOM_STATE
)
logger = get_logger()
def train_all_models(df) :


    logger.info("เริ่ม AI Tournament")

    feature_columns = [

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

    X = df[feature_columns]

    y = df["TARGET"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        shuffle=False

    )

    results = {}

    models = {}

    
    models["Random Forest"] = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=RANDOM_STATE
)

    models["Gradient Boosting"] = GradientBoostingClassifier(
        random_state=RANDOM_STATE
)

    models["XGBoost"] = XGBClassifier(
        random_state=RANDOM_STATE,
        eval_metric="logloss"
)
    best_model = None
    best_model_name = ""
    best_accuracy = 0
    for name, model in models.items():

        logger.info(f"กำลัง Train {name}")

        model.fit(

            X_train,

            y_train

    )

        score = evaluate_model(

            model,

            X_test,

            y_test

    )

        results[name] = score

        if score["accuracy"] > best_accuracy:

            best_accuracy = score["accuracy"]
            best_model = model
            best_model_name = name
    winner = show_leaderboard(results)

    logger.info(f"🏆 Winner : {best_model_name}")
    save_model(best_model)

    return best_model, results