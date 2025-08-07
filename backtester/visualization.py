import pandas as pd
import matplotlib.pyplot as plt

def plot_performance(portfolio: pd.DataFrame, signals: pd.DataFrame, ticker: str):
    """
    Plots the performance of the backtest.

    Args:
    portfolio (pd.DataFrame): The portfolio DataFrame from the backtester.
    signals (pd.DataFrame): The DataFrame with the original signals.
    ticker (str): The name of the traded ticker.
    """
    fig, (ax1, ax2) = plt.subplots(
        2, 1, 
        figsize=(12, 10), 
        gridspec_kw={'height_ratios': [1, 2]},
        sharex=True
    )
    fig.suptitle(f'Backtest Performance for {ticker}', fontsize=16)

    # --- Plot 1: Portfolio-Wert, Cash und Holdings als Linien ---
    ax1.plot(portfolio.index, portfolio['total'], label='Total Portfolio Value', color='g', linewidth=2)
    ax1.plot(portfolio.index, portfolio['cash'], label='Cash', color='b', linestyle='--', alpha=0.7)
    ax1.plot(portfolio.index, portfolio['holdings'], label='Holdings Value', color='orange', linestyle='--', alpha=0.7)
    
    ax1.set_title('Portfolio Value, Cash, and Holdings')
    ax1.set_ylabel('Value ($)')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # --- Plot 2: Preis und Trades (unverändert) ---
    ax2.plot(signals.index, signals['Close'], label='Close Price', color='k', alpha=0.7)
    ax2.plot(signals.index, signals['short_ma'], label='50-Day MA', color='b', linestyle='--')
    ax2.plot(signals.index, signals['long_ma'], label='200-Day MA', color='orange', linestyle='--')
    
    buy_signals = signals[signals['positions'] == 1.0]
    ax2.plot(buy_signals.index, signals['short_ma'][buy_signals.index],
             '^', markersize=10, color='g', label='Buy Signal')
    
    sell_signals = signals[signals['positions'] == -1.0]
    ax2.plot(sell_signals.index, signals['short_ma'][sell_signals.index],
             'v', markersize=10, color='r', label='Sell Signal')

    ax2.set_title('Stock Price, MAs, and Trades')
    ax2.set_ylabel('Price ($)')
    ax2.set_xlabel('Date')
    ax2.legend(loc='upper left')
    ax2.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()