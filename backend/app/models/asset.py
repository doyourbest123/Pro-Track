# backend/app/models/asset.py
from datetime import datetime
from typing import Dict, Optional
import yfinance as yf
from app.config import settings

class AssetData:
    """Represents the live market data fetched from Yahoo Finance."""
    def __init__(self, ticker_symbol: str):
        self.ticker_symbol: str = ticker_symbol.upper()
        self.long_name: str = ""
        self.current_price: float = 0.0
        self.pe_ratio: Optional[float] = None
        self.forward_pe: Optional[float] = None
        self.peg_ratio: Optional[float] = None
        self.debt_to_equity: Optional[float] = None
        self.profit_margin: Optional[float] = None
        self.dividend_yield: Optional[float] = None
        self.last_updated: Optional[datetime] = None

    def refresh_from_yahoo(self) -> None:
        stock = yf.Ticker(self.ticker_symbol)
        info = stock.info

        self.long_name = info.get("longName", self.ticker_symbol)
        self.current_price = info.get("currentPrice", 0.0)
        self.pe_ratio = info.get("trailingPE")
        self.forward_pe = info.get("forwardPE")
        self.peg_ratio = info.get("pegRatio")
        self.debt_to_equity = info.get("debtToEquity")
        self.profit_margin = info.get("profitMargins")
        self.dividend_yield = info.get("dividendYield")
        self.last_updated = datetime.now()

        hist_df = stock.history(period="1mo")
        formatted_history = []
        for date, row in hist_df.iterrows():
            formatted_history.append({
                "date": date.strftime("%b %d"),
                "price": round(row["Close"], 2)
            })
        self.history = formatted_history

        self.last_updated = datetime.now()

    def to_dict(self) -> Dict:
        """Convert market data into JSON format for UI."""
        data = self.__dict__.copy()
        if isinstance(self.ai_opinion, AiOpinion):
            data["ai_opinion"] = self.ai_opinion.to_dict()
        return data


class AiOpinion:
    """AI-Powered analytical judgement of a specific asset."""
    def __init__(self, ticker_symbol: str):
        self.ticker_symbol: str = ticker_symbol
        self.valuation_verdict: str = "Awaiting analysis..."
        self.risk_view: str = "Awaiting analysis..."
        self.profitability_verdict: str = "Awaiting analysis..."
        self.generated_at: Optional[datetime] = None

    def to_dict(self) -> Dict:
        return self.__dict__

    def generate_opinion(self, market_data: AssetData, model_client=None) -> None:
        """Pass structured AssetData properties to AI model and update verdicts."""
        import os
        from google import genai
        from google.genai import types

        api_key = settings.GEMINI_API_KEY

        if not api_key:
            self.valuation_verdict = "Please provide a GEMINI_API_KEY environment variable."
            self.risk_view = "API Key Missing."
            self.profitability_verdict = "AI engine idle."
            return

        try:
            client = genai.Client(api_key=api_key)

            finance_payload = (
                f"Ticker: {market_data.ticker_symbol}\n"
                f"Company Name: {market_data.long_name}\n"
                f"Price: ${market_data.current_price}\n"
                f"P/E Ratio: {market_data.pe_ratio}\n"
                f"PEG Ratio: {market_data.peg_ratio}\n"
                f"Debt/Equity: {market_data.debt_to_equity}\n"
                f"Profit Margin: {market_data.profit_margin}\n"
            )

            system_prompt = (
                "You are an objective financial analyst. Analyze the provided metrics. Do not give investment advice. "
                "Output exactly three distinct lines of text separated by a newline breakdown. Line 1 must evaluate general valuation. "
                "Line 2 must evaluate debt balance sheet risk. Line 3 must evaluate core profitability margins. Do not number or bullet the lines."
            )

            chat = client.chats.create(
                model='gemini-3.6-flash',
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                )
            )

            response = chat.send_message(
                message=f"Analyze these market metrics:\n{finance_payload}",
            )

            lines = [line.strip() for line in response.text.strip().split("\n") if line.strip()]

            self.valuation_verdict = lines[0] if len(lines) > 0 else "Analysis complete."
            self.risk_view = lines[1] if len(lines) > 1 else "Analysis complete."
            self.profitability_verdict = lines[2] if len(lines) > 2 else "Analysis complete."

            from datetime import datetime
            self.generated_at = datetime.now().isoformat()

        except Exception as e:
            self.valuation_verdict = f"AI Error: Unable to complete audit run ({str(e)})."
