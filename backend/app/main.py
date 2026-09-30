import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.dashboard import Dashboard

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "data", "user_portfolio.json")

dashboard = Dashboard(profile_name="Market Watch Center", config_file_path=CONFIG_PATH)

@app.get("/api/dashboard")

def get_watchlist_payload() -> dict:
    """
    Returns the current state of the dashboard.
    Instant load when React mounts its primary page components.
    """

    watchlist_payload = []

    for ticker, asset in dashboard.holdings.items():
        watchlist_payload.append({
            "ticker": ticker,
            "market_metrics": asset.to_dict(),
        })

    return {
        "watchlist_name": dashboard.profile_name,
        "last_refresh": dashboard.last_refresh.isoformat() if dashboard.last_refresh else None,
        "tracked_stocks_count": len(watchlist_payload),
        "stocks": watchlist_payload
    }

@app.get("/api/watchlist")
def read_watchlist():
    """
    Returns the live metric states for all watched stocks.
    """
    return get_watchlist_payload()

@app.post("/api/watchlist/refresh")
def refresh_watchlist_metrics(trigger_ai: bool = False):
    """
    Tells Yahoo Finance to scrape fresh market numbers for stock list.
    Returns updated dictionary structure straight back to React.
    """

    try:
        for asset in dashboard.holdings.values():
            asset.refresh_from_yahoo()

            if trigger_ai:
                asset.ai_opinion.generate_opinion(asset, None)

        from datetime import datetime
        dashboard.last_refresh = datetime.now()

        return {
            "status": "success",
            "payload": get_watchlist_payload()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market data sync failed: {str(e)}")
    