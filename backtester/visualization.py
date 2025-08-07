import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_performance(portfolio: pd.DataFrame, signals: pd.DataFrame, ticker: str):
    """
    Plot the performance of the backtest with interactive Plotly charts.
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Portfolio Development', 'Price, MAs & trading signals'),
        row_heights=[0.3, 0.7]
    )

    # --- Plot 1 ---
    fig.add_trace(go.Scatter(
        x=portfolio.index, y=portfolio['total'], name='total value',
        line=dict(color='green', width=2)
    ), row=1, col=1)

    # --- Plot 2 ---
    # Price and MAs
    fig.add_trace(go.Scatter(x=signals.index, y=signals['Close'], name='closing price', line=dict(color='grey')), row=2, col=1)
    fig.add_trace(go.Scatter(x=signals.index, y=signals['short_ma'], name='50-day MA', line=dict(color='#73c7ff', dash='dash')), row=2, col=1)
    fig.add_trace(go.Scatter(x=signals.index, y=signals['long_ma'], name='200-day MA', line=dict(color='orange', dash='dash')), row=2, col=1)

    # buy signals
    buy_signals = signals[signals['positions'] == 1.0]
    fig.add_trace(go.Scatter(
        x=buy_signals.index, y=buy_signals['short_ma'], name='buy signal',
        mode='markers', marker=dict(color='green', size=10, symbol='triangle-up')
    ), row=2, col=1)

    # selling signals
    sell_signals = signals[signals['positions'] == -1.0]
    fig.add_trace(go.Scatter(
        x=sell_signals.index, y=sell_signals['short_ma'], name='selling signals',
        mode='markers', marker=dict(color='red', size=10, symbol='triangle-down')
    ), row=2, col=1)

    # --- Layout adjustments ---
    fig.update_layout(
        title_text=f'Backtest performance for {ticker}',
        height=700,
        showlegend=True,
        legend_traceorder="reversed" 
    )
    fig.update_yaxes(title_text="value ($)", row=1, col=1)
    fig.update_yaxes(title_text="price ($)", row=2, col=1)
    
    return fig
