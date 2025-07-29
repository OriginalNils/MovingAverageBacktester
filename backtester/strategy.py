import pandas as pd
import numpy as np

class MovingAverageStrategy:
    def __init__(self, data: pd.DataFrame, short_window: int, long_window: int):
        """
        Initialises the strategy.
        Args:
            data (pd.DataFrame): DataFrame with historical price data.
            short_window (int): The window for the short moving average.
            long_window (int): The window for the long moving average.
        """
        self.data = data
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self) -> pd.DataFrame:
        """
        Calculates the moving averages and generates the trading signals.

        Returns:
            pd.DataFrame: A DataFrame containing the original data as well as the
                          signals and moving averages.
        """
        signals = self.data.copy()

        signals['short_ma'] = signals['Close'].rolling(window=self.short_window).mean()
        signals['long_ma'] = signals['Close'].rolling(window=self.long_window).mean()

        signals['signal'] = 0.0

        signals['signal'] = np.where(signals['short_ma'] > signals['long_ma'], 1.0, 0.0)

        signals['positions'] = signals['signal'].diff()

        return signals