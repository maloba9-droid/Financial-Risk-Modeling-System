# engine.py
from models import Portfolio
import time
from exceptions import InvalidRiskParameterError
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

def performance_logger(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[LOG] {func.__name__} completed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

class RiskEngine:
    
    @performance_logger
    def simulate_market_shock(self, portfolio: Portfolio, drop_percentage: float) -> tuple:
        if drop_percentage < 0 or drop_percentage > 1:
            raise InvalidRiskParameterError("Drop percentage must be between 0.0 and 1.0")
            
        print(f"\n--- Simulating a {drop_percentage*100}% market shock ---")
        post_shock_value = 0.0
        
        for asset, qty in portfolio.generate_assets():
            shocked_price = asset.apply_shock(drop_percentage) 
            post_shock_value += (shocked_price * qty)
            
        pre_shock_value = portfolio.calculate_total_value()
        print(f"\nPre-Shock Value:  ${pre_shock_value:.2f}")
        print(f"Post-Shock Value: ${post_shock_value:.2f}")
        return pre_shock_value, post_shock_value

    def visualize_shock(self, portfolio_name: str, pre_shock: float, post_shock: float, drop_pct: float):
        print("\n[System] Generating risk visualization chart...")
        labels = ['Pre-Shock Value', 'Post-Shock Value']
        values = [pre_shock, post_shock]
        plt.figure(figsize=(8, 6))
        bars = plt.bar(labels, values, color=['#2ca02c', '#d62728'], width=0.6)
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + (pre_shock * 0.01), 
                     f"${yval:,.0f}", ha='center', va='bottom', fontweight='bold')
        plt.title(f"{portfolio_name}: Impact of {drop_pct*100}% Market Drop", fontsize=14)
        plt.ylabel("Portfolio Value ($)")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show() 

    # --- NEW: MILESTONE 6 MACHINE LEARNING INTEGRATION ---
    @performance_logger
    def run_ml_clustering(self, portfolio: Portfolio):
        """Uses K-Means Clustering to group assets by risk profiles."""
        print("\n--- Running AI Risk Clustering (K-Means) ---")
        
        tickers = []
        volatilities = []
        returns = []
        
        # 1. Extract features for ML model
        for asset, qty in portfolio.generate_assets():
            if len(asset._historical_prices) > 2:
                daily_rets = asset._historical_prices.pct_change().dropna()
                ann_return = float(daily_rets.mean() * 252)
                ann_volatility = asset.calculate_volatility()
                
                tickers.append(asset.ticker)
                volatilities.append(ann_volatility)
                returns.append(ann_return)
                
        if len(tickers) < 3:
            print("[Warning] Not enough data for clustering.")
            return
            
        # 2. Prepare Data and Train K-Means Model (k=3 for Low, Med, High Risk)
        X = np.column_stack((volatilities, returns))
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        
        # 3. Visualize the AI Clusters
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(volatilities, returns, c=labels, cmap='viridis', s=100, alpha=0.8)
        
        # Annotate tickers
        for i, txt in enumerate(tickers):
            plt.annotate(txt, (volatilities[i], returns[i]), xytext=(5, 5), textcoords='offset points')
            
        plt.title("AI-Driven Asset Clustering (Risk vs. Return)", fontsize=14)
        plt.xlabel("Annualized Volatility (Risk)")
        plt.ylabel("Annualized Expected Return")
        plt.colorbar(scatter, label="Risk Cluster ID")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()