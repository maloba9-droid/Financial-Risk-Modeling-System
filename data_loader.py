# data_loader.py
import yfinance as yf
import pandas as pd
import os
from exceptions import DataFetchError
import concurrent.futures

def _download_single(ticker: str, period: str) -> tuple:
    """Helper function to process a single ticker."""
    file_path = f"{ticker}_cache.csv"
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
            return ticker, df['Close']
        else:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)
            
            if df.empty:
                raise DataFetchError(f"No data returned from API for {ticker}.")
            
            df['Close'].to_csv(file_path, header=True)
            return ticker, df['Close']
            
    except Exception as e:
        print(f" [!] ERROR: Failed to load data for {ticker}. Reason: {e}")
        return ticker, None

def fetch_historical_data(tickers: list, period: str = "5y") -> dict:
    """Fetches data concurrently (Multithreading) for massive performance gains."""
    print(f"Fetching {period} of historical data using 10 concurrent threads...")
    data_dict = {}
    
    # SYSTEM SCALING: Using ThreadPoolExecutor to download multiple assets at once
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks to the executor simultaneously
        futures = [executor.submit(_download_single, ticker, period) for ticker in tickers]
        
        # As each thread finishes, collect its data
        for future in concurrent.futures.as_completed(futures):
            ticker, data = future.result()
            if data is not None:
                data_dict[ticker] = data
                
    print("Successfully loaded all data.")
    return data_dict