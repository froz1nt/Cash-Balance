import os


# ============================================================
# ПУТЬ СОХРАНЕНИЯ
# ============================================================

if os.name == "nt":
    APP_DIR = os.path.join(
        os.getenv("APPDATA") or os.path.expanduser("~"),
        "CashBalance"
    )

elif __import__("sys").platform == "darwin":
    APP_DIR = os.path.join(
        os.path.expanduser("~"),
        "Library",
        "Application Support",
        "CashBalance"
    )

else:
    APP_DIR = os.path.join(
        os.path.expanduser("~"),
        ".local",
        "share",
        "CashBalance"
    )


os.makedirs(APP_DIR, exist_ok=True)


SAVE_FILE = os.path.join(
    APP_DIR,
    "cash_balance_save.json"
)


# ============================================================
# ЦВЕТА
# ============================================================

BG = "#05070a"

CARD = "#0b1017"
CARD_2 = "#0f1620"
CARD_3 = "#121b26"

BLUE = "#1683ff"
BLUE_DARK = "#0d5fc4"
BLUE_HOVER = "#3195ff"

WHITE = "#ffffff"
TEXT = "#dce5ef"
MUTED = "#718096"

GREEN = "#27d17f"
GREEN_DARK = "#1aaa66"

RED = "#ff4d5f"
RED_DARK = "#d93647"

BORDER = "#182330"
BORDER_LIGHT = "#233242"