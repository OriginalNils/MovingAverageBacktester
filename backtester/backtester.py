import pandas as pd

class Backtester:
    """
    Performs a trading simulation based on generated signals.
    """
    def __init__(self, signals: pd.DataFrame, initial_capital: float):
        """
        Initialises the backtester.

        Args:
            signals (pd.DataFrame): DataFrame containing the “positions” column.
            initial_capital (float): The starting capital for the simulation.
        """
        self.signals = signals
        self.initial_capital = initial_capital

    def run_simulation(self) -> pd.DataFrame:
        """
        Simulates trading day after day in a loop.
        """
        cash = self.initial_capital
        shares_held = 0
        portfolio_data = []

        for i in range(len(self.signals)):
            row = self.signals.iloc[i]
            trade_signal = row['positions']
            current_price = row['Close']

            # --- trading logic ---
            # BUY: When a buy signal (1.0) is generated and we do not hold any shares
            if trade_signal == 1.0 and shares_held == 0:
                shares_to_buy = cash // current_price
                shares_held += shares_to_buy
                cash -= shares_to_buy * current_price
                print(f"{row.name.date()}: BUY {shares_to_buy} shares at ${current_price:.2f}")

            # SELL: When a sell signal (-1.0) is generated and we hold shares
            elif trade_signal == -1.0 and shares_held > 0:
                cash += shares_held * current_price
                print(f"{row.name.date()}: SELL {shares_held} shares at ${current_price:.2f}")
                shares_held = 0

            total_value = cash + (shares_held * current_price)
            holdings_value = shares_held * current_price

            portfolio_data.append({
                'total': total_value,
                'cash': cash,
                'holdings': holdings_value
            })

        # Create a DataFrame from the list of portfolio values
        portfolio = pd.DataFrame(portfolio_data, index=self.signals.index)
        portfolio['returns'] = portfolio['total'].pct_change()
        
        return portfolio