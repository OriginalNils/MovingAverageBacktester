from financialdataimporter import YahooFinanceImporter
from backtester.strategy import MovingAverageStrategy

def run_backtest():
    # --- 1. Load Data ---
    importer = YahooFinanceImporter()
    ticker = 'TSLA'
    start_date = '2020-01-01'
    end_date = '2025-07-29' 

    print(f"Loading data for {ticker}...")
    stock_data = importer.get_data(ticker, start_date, end_date)

    # --- 2. Generate signals ---
    short_window = 50
    long_window = 200
    
    print("Generate trading signals...")
    strategy = MovingAverageStrategy(stock_data, short_window, long_window)
    signals = strategy.generate_signals()

    print("\nData with trading signals (1.0 = buy, -1.0 = sell):")
    print(signals.tail(10))


if __name__ == "__main__":
    run_backtest()