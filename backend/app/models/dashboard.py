import json

from typing import Dict, Optional
from datetime import datetime

from app.models.asset import AssetData, AiOpinion # using __init__.py to allow for instantiation
from app.services import loadjson

class Dashboard:
    """
    A read-only watchlist manager.
    Loads static list of stock tickers from a configuration file and binds them to market data tracking classes
    and stores their background AI insight profiles.
    """

    def __init__(self, profile_name: str, config_file_path: str):
        self.profile_name: str = profile_name
        self.config_file_path: str = config_file_path

        self.holdings: Dict[str, AssetData] = {}
        self.last_refresh: Optional[datetime] = None

        self._load_watchlist_config()

    def _load_watchlist_config(self) -> None:
        """
        Reads user's static asset tracking file from local disk.
        """

        try: 
            with open(self.config_file_path, 'r') as file:
                data = loadjson.load_user_portfolio()

                for ticker_symbol in data.get("tracked_tickers", []):
                    ticker = ticker_symbol.upper().strip()

                    asset = AssetData(ticker_symbol=ticker)
                    asset.ai_opinion = AiOpinion(ticker_symbol=ticker)

                    self.holdings[ticker] = asset
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading watchlist JSON blueprint: {e}")
            self.holdings = {}
            