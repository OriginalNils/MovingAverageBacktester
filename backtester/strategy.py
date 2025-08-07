import pandas as pd
import numpy as np

class Strategy:
    """
    The base class for all trading strategies.

    This class serves as a template (or "interface"). It defines the
    structure that any new strategy class must follow, ensuring it works
    seamlessly with the backtester.
    """
    def __init__(self, data: pd.DataFrame, params: dict):
        """
        Initializes the strategy.

        Args:
            data (pd.DataFrame): The historical price data.
            params (dict): A dictionary of parameters for the strategy
                             (e.g., {'short_window': 50, 'long_window': 200}).
        """
        self.data = data
        self.params = params

    def generate_signals(self) -> pd.DataFrame:
        """
        This method must be implemented by every child strategy.
        
        It should return a DataFrame containing at least a 'positions' column,
        where 1.0 means buy and -1.0 means sell.
        """
        raise NotImplementedError("You must implement the generate_signals() method in your strategy!")

# --- The Moving Average strategy now inherits from the base class ---

class MovingAverageStrategy(Strategy):
    """
    Implements the classic Moving Average Crossover strategy.
    It inherits the structure from the base Strategy class.
    """
    def generate_signals(self) -> pd.DataFrame:
        """
        Calculates moving averages and generates buy/sell signals.
        """
        # Create a copy to avoid modifying the original data
        signals = self.data.copy()
        
        # Get parameters from the params dictionary with default values
        short_window = self.params.get('short_window', 50)
        long_window = self.params.get('long_window', 200)

        # Calculate moving averages
        signals['short_ma'] = signals['Close'].rolling(window=short_window).mean()
        signals['long_ma'] = signals['Close'].rolling(window=long_window).mean()

        # Generate the primary signal (1.0 when short > long, else 0.0)
        signals['signal'] = np.where(signals['short_ma'] > signals['long_ma'], 1.0, 0.0)

        # Generate the actual trade triggers (the crossovers)
        # .diff() calculates the difference from the previous day.
        # A change from 0.0 to 1.0 results in a diff of 1.0 (Buy).
        # A change from 1.0 to 0.0 results in a diff of -1.0 (Sell).
        signals['positions'] = signals['signal'].diff()

        return signals

# --- Strategy 2: Relative Strength Index (RSI) ---
class RSIStrategy(Strategy):
    """Implements a simple RSI-based trading strategy."""
    def generate_signals(self) -> pd.DataFrame:
        signals = self.data.copy()
        rsi_period = self.params.get('rsi_period', 14)
        oversold_threshold = self.params.get('oversold', 30)
        overbought_threshold = self.params.get('overbought', 70)

        # Calculate RSI
        delta = signals['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
        rs = gain / loss
        signals['rsi'] = 100 - (100 / (1 + rs))

        # Generate signals
        signals['signal'] = 0.0
        signals['signal'] = np.where(signals['rsi'] < oversold_threshold, 1.0, signals['signal'])
        signals['signal'] = np.where(signals['rsi'] > overbought_threshold, -1.0, signals['signal'])
        
        # We only want to trade the crossover, not every day it's over/under
        # So we identify where the signal changes from the previous day.
        # This simple example sells when overbought and buys when oversold.
        signals['positions'] = signals['signal'].diff().replace(2.0, 0.0).replace(-2.0, 0.0)

        return signals

# --- Strategy 3: Buy and Hold (for comparison) ---
class BuyAndHoldStrategy(Strategy):
    """Implements a simple Buy and Hold strategy to serve as a benchmark."""
    def generate_signals(self) -> pd.DataFrame:
        signals = self.data.copy()
        # Create a positions column filled with zeros
        signals['positions'] = 0.0
        # Set the first day's position to 1.0 (Buy)
        signals.iloc[0, signals.columns.get_loc('positions')] = 1.0
        return signals