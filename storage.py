import json
import os

from config import SAVE_FILE


# ============================================================
# ЗАГРУЗКА
# ============================================================

def load_data():
    if not os.path.exists(SAVE_FILE):
        return [], None

    try:
        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError

        operations = data.get(
            "operations",
            []
        )

        if not isinstance(operations, list):
            operations = []

        goal = data.get(
            "goal",
            None
        )

        return operations, goal

    except Exception:
        return [], None


# ============================================================
# СОХРАНЕНИЕ
# ============================================================

def save_data(operations, goal):
    data = {
        "operations": operations,
        "goal": goal
    }

    try:
        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    except Exception:
        pass