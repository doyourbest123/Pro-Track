import json
from app.config import settings

def load_user_portfolio():
    if not settings.PORTFOLIO_FILE_PATH.exists():
        return {}

    with open(settings.PORTFOLIO_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)