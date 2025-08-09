import streamlit as st
from datetime import date

# Import your classes and functions
from financialdataimporter import YahooFinanceImporter
from backtester.strategy import MovingAverageStrategy, RSIStrategy, BuyAndHoldStrategy
from backtester.backtester import Backtester
from backtester.visualization import plot_performance

# --- A dictionary to map user-friendly names to the strategy classes ---
STRATEGY_MAPPING = {
    "Moving Average Crossover": MovingAverageStrategy,
    "Relative Strength Index (RSI)": RSIStrategy,
    "Buy and Hold": BuyAndHoldStrategy
}

# --- Page Configuration ---
st.set_page_config(page_title="Trading Backtester", layout="wide")
st.title("Interactive Trading Strategy Backtester 📈")

# --- Sidebar for input parameters ---
st.sidebar.header("Backtest Parameters")

# --- General Parameters ---
ticker = st.sidebar.text_input("Ticker Symbol", "AAPL").upper()
start_date = st.sidebar.date_input("Start Date", date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())
initial_capital = st.sidebar.number_input("Initial Capital ($)", min_value=1000, value=10000)

# --- Strategy Selection ---
strategy_name = st.sidebar.selectbox("Choose a Strategy", list(STRATEGY_MAPPING.keys()))
SelectedStrategy = STRATEGY_MAPPING[strategy_name]
strategy_params = {}

# --- Strategy-Specific Parameters ---
st.sidebar.header(f"Parameters for {strategy_name}")
if strategy_name == "Moving Average Crossover":
    strategy_params['short_window'] = st.sidebar.number_input("Short Window (Days)", min_value=5, value=50)
    strategy_params['long_window'] = st.sidebar.number_input("Long Window (Days)", min_value=50, value=200)
elif strategy_name == "Relative Strength Index (RSI)":
    strategy_params['rsi_period'] = st.sidebar.number_input("RSI Period (Days)", min_value=5, value=14)
    strategy_params['oversold'] = st.sidebar.number_input("Oversold Threshold", min_value=10, value=30)
    strategy_params['overbought'] = st.sidebar.number_input("Overbought Threshold", max_value=90, value=70)

# --- Start Button ---
if st.sidebar.button("Run Backtest"):
    with st.spinner("Loading data and running backtest..."):
        try:
            # 1. Load Data
            importer = YahooFinanceImporter()
            stock_data = importer.get_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            
            # 2. Generate Signals (using the selected strategy)
            strategy = SelectedStrategy(stock_data, strategy_params)
            signals = strategy.generate_signals()
            
            # 3. Run Simulation
            backtester = Backtester(signals, initial_capital)
            portfolio = backtester.run_simulation()
            
            # 4. Display Results
            years = (end_date - start_date).days / 365.25
            st.success("Backtest completed successfully!")
            final_value = portfolio['total'].iloc[-1]
            total_return = (final_value - initial_capital) / initial_capital * 100
            cagr = (1 + total_return / 100) ** (1 / years) - 1
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Initial Capital", f"${initial_capital:,.2f}")
            col2.metric("Final Capital", f"${final_value:,.2f}")
            col3.metric("Total Return", f"{total_return:.2f}%")
            col4.metric("Average return per year", f"{cagr*100:.2f}%")

            fig = plot_performance(portfolio, signals, ticker)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")