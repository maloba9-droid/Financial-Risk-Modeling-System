# main.py
from models import Asset, Portfolio, VolatilityRiskStrategy, DefensiveRiskStrategy
from engine import RiskEngine
from data_loader import fetch_historical_data
from exceptions import SystemError

def main():
    try:
        # 1. A diverse, real-world portfolio of 20 assets
        tickers = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", # Tech
            "JPM", "V", "GS",                                        # Finance
            "JNJ", "UNH", "PFE",                                     # Healthcare
            "WMT", "KO", "PG",                                       # Consumer
            "XOM", "CVX",                                            # Energy
            "GLD", "TLT"                                             # Safe Havens (Gold, Bonds)
        ]
        
        # 2. Fetch data (Using multithreading for massive speed upgrades)
        historical_df = fetch_historical_data(tickers, period="5y")
        
        fund = Portfolio("Mega Cap Risk Fund")
        
        # 3. Automate the Object Instantiation using a loop
        print("\n[System] Building automated portfolio...")
        for ticker in tickers:
            # Apply the Defensive strategy to Gold and Bonds, Volatility to everything else
            if ticker in ["TLT", "GLD"]:
                strategy = DefensiveRiskStrategy()
            else:
                strategy = VolatilityRiskStrategy()
                
            # Create the Asset
            new_asset = Asset(ticker, strategy)
            
            # Safely inject data and add to portfolio (assuming 100 shares each for testing)
            if ticker in historical_df and not historical_df[ticker].dropna().empty:
                new_asset.load_history(historical_df[ticker].dropna())
                fund.add_asset(new_asset, quantity=100)
            else:
                print(f"  [Warning] Skipping {ticker} due to missing API data.")
        
        # 4. Test Serialization
        fund.serialize_to_json()
        
        # 5. Run Simulation (Capturing the returned values for the chart)
        drop = 0.15
        engine = RiskEngine()
        pre_val, post_val = engine.simulate_market_shock(fund, drop_percentage=drop) 
        
        # 6. Run Visualization (M5 - Generates the Matplotlib bar chart)
        engine.visualize_shock(fund.owner_name, pre_val, post_val, drop)
        
        # 7. Run Machine Learning AI Clustering (M6 - Generates the AI Scatterplot)
        engine.run_ml_clustering(fund)
        
    except SystemError as e:
        print(f"\n[CRITICAL] System Error Encountered: {e}")
    except Exception as e:
        print(f"\n[CRITICAL] Unexpected Python Error: {e}")

if __name__ == "__main__":
    main()