from financialdataimporter import YahooFinanceImporter
from backtester.strategy import MovingAverageStrategy
from backtester.backtester import Backtester
from backtester.visualization import plot_performance

def run_backtest():
    # --- 1. Load Data ---
    importer = YahooFinanceImporter()
    ticker = 'AAPL'
    start_date = '2018-01-01'
    end_date = '2025-07-29' 

    print(f"Loading data for {ticker}...")
    stock_data = importer.get_data(ticker, start_date, end_date)

    # --- 2. Generate signals ---
    short_window = 50
    long_window = 200
    
    print("Generate trading signals...")
    strategy = MovingAverageStrategy(stock_data, short_window, long_window)
    signals = strategy.generate_signals()

    # --- 3. Perform backtesting ---
    initial_capital = 10000.0
    print("Conduct trade simulation...")
    backtester = Backtester(signals, initial_capital)
    portfolio = backtester.run_simulation()

    # --- 4. Display and visualise results ---
    final_value = portfolio['total'].iloc[-1]
    print(f"\ninitial capital: ${initial_capital:,.2f}")
    print(f"final capital:   ${final_value:,.2f}")
    
    print("\nCreate performance plot...")
    plot_performance(portfolio, signals, ticker)
    print("Backtest completed.")


if __name__ == "__main__":
    run_backtest()