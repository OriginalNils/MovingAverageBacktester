import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_performance(portfolio: pd.DataFrame, signals: pd.DataFrame, ticker: str):
    """
    Plots the backtest performance. This version is now strategy-agnostic.
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Portfolio Performance', 'Price & Trading Signals'),
        row_heights=[0.3, 0.7]
    )

    # --- Plot 1: Portfolio Value (unchanged) ---
    fig.add_trace(go.Scatter(x=portfolio.index, y=portfolio['total'], name='Total Value', line=dict(color='orange', width=2)), row=1, col=1)

    # --- Plot 2: Price and Trading Signals ---
    # Plot the closing price (for all strategies)
    fig.add_trace(go.Scatter(x=signals.index, y=signals['Close'], name='Close Price', line=dict(color='darkgrey')), row=2, col=1)

    # NEW: Plot Moving Averages only if they exist in the data
    if 'short_ma' in signals.columns and 'long_ma' in signals.columns:
        fig.add_trace(go.Scatter(x=signals.index, y=signals['short_ma'], name='Short MA', line=dict(color='#1f77b4', dash='dash')), row=2, col=1)
        fig.add_trace(go.Scatter(x=signals.index, y=signals['long_ma'], name='Long MA', line=dict(color='#ff7f0e', dash='dash')), row=2, col=1)
    
    # NEW: Plot RSI only if it exists in the data
    if 'rsi' in signals.columns:
        # Create a second y-axis for the RSI indicator
        fig.update_layout(yaxis2=dict(title='RSI', overlaying='y', side='right', range=[0, 100]))
        fig.add_trace(go.Scatter(x=signals.index, y=signals['rsi'], name='RSI', line=dict(color='purple', width=1), yaxis='y2'), row=2, col=1)


    # --- Plot Buy and Sell Markers (now on the Close price) ---
    buy_signals = signals[signals['positions'] == 1.0]
    fig.add_trace(go.Scatter(
        x=buy_signals.index, 
        y=signals.loc[buy_signals.index]['Close'], # Plot marker on the closing price
        name='Buy Signal',
        mode='markers', 
        marker=dict(color='#2ca02c', size=11, symbol='triangle-up', line=dict(width=1, color='black'))
    ), row=2, col=1)

    sell_signals = signals[signals['positions'] == -1.0]
    fig.add_trace(go.Scatter(
        x=sell_signals.index, 
        y=signals.loc[sell_signals.index]['Close'], # Plot marker on the closing price
        name='Sell Signal',
        mode='markers', 
        marker=dict(color='#d62728', size=11, symbol='triangle-down', line=dict(width=1, color='black'))
    ), row=2, col=1)

    # --- Layout Updates ---
    fig.update_layout(
        title_text=f'Backtest Performance for {ticker}',
        height=800,
        showlegend=True,
        legend_traceorder="reversed"
    )
    fig.update_yaxes(title_text="Portfolio Value ($)", row=1, col=1)
    fig.update_yaxes(title_text="Stock Price ($)", row=2, col=1)
    
    return fig
