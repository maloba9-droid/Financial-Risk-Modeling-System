# models.py
import pandas as pd
import numpy as np
import json

# --- DESIGN PATTERN 1: STRATEGY PATTERN ---
class RiskStrategy:
    """Interface for risk calculation strategies."""
    def calculate_shock(self, asset, market_drop: float) -> float:
        raise NotImplementedError

class VolatilityRiskStrategy(RiskStrategy):
    """Calculates shock based on real historical volatility."""
    def calculate_shock(self, asset, market_drop: float) -> float:
        # Now uses the asset's helper method
        volatility = asset.calculate_volatility()
        shock_factor = market_drop * (1 + volatility)
        return asset.get_current_price() * (1 - shock_factor)

class DefensiveRiskStrategy(RiskStrategy):
    """Calculates a dampened shock (Used for Bonds/Gold)."""
    def calculate_shock(self, asset, market_drop: float) -> float:
        safe_drop = market_drop * 0.2 
        return asset.get_current_price() * (1 - safe_drop)

# --- REFACTORED ASSET MODEL ---
class Asset:
    def __init__(self, ticker: str, risk_strategy: RiskStrategy):
        self.ticker = ticker
        self._historical_prices = pd.Series(dtype=float)
        self.risk_strategy = risk_strategy

    def load_history(self, price_series: pd.Series):
        self._historical_prices = price_series

    def get_current_price(self) -> float:
        if not self._historical_prices.empty:
            return float(self._historical_prices.iloc[-1])
        return 0.0

    # --- THE FIX: Utility method restored for the Functional Pipeline ---
    def calculate_volatility(self) -> float:
        """Calculates real-world annualized volatility."""
        if self._historical_prices.empty or len(self._historical_prices) < 2:
            return 0.0
        daily_returns = self._historical_prices.pct_change().dropna()
        return float(daily_returns.std() * np.sqrt(252))

    def apply_shock(self, market_drop: float):
        # Delegates the calculation to its injected strategy
        new_price = self.risk_strategy.calculate_shock(self, market_drop)
        print(f"  > {self.ticker} Shocked to ${new_price:.2f}")
        return new_price

class Portfolio:
    def __init__(self, owner_name: str):
        self.owner_name = owner_name
        self.assets = {} 

    def add_asset(self, asset: Asset, quantity: int):
        self.assets[asset.ticker] = {'asset_obj': asset, 'quantity': quantity}

    def calculate_total_value(self) -> float:
        total_value = 0.0
        for item in self.assets.values():
            total_value += item['asset_obj'].get_current_price() * item['quantity']
        return total_value

    def generate_assets(self):
        """A generator that yields one asset at a time."""
        for item in self.assets.values():
            yield item['asset_obj'], item['quantity']
            
    def serialize_to_json(self, filepath="portfolio_state.json"):
        """Saves the current portfolio structure to a JSON file."""
        data = {
            "owner": self.owner_name,
            "holdings": [{"ticker": t, "quantity": d['quantity']} for t, d in self.assets.items()]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\n[System] Portfolio state serialized to {filepath}")