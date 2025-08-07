import streamlit as st
from datetime import date

from financialdataimporter import YahooFinanceImporter
from backtester.strategy import MovingAverageStrategy
from backtester.backtester import Backtester
from backtester.visualization import plot_performance

# --- Page configuration ---
st.set_page_config(page_title="MA Backtester", layout="wide")
st.title("Moving Average Crossover Backtester 📈")

# --- Sidebar for input parameters ---
st.sidebar.header("backtesting parameters")

ticker = st.sidebar.text_input("ticker symbol", "AAPL").upper()
start_date = st.sidebar.date_input("start date", date(2020, 1, 1))
end_date = st.sidebar.date_input("end date", date.today())
short_window = st.sidebar.number_input("short window (days)", min_value=5, max_value=100, value=50, step=1)
long_window = st.sidebar.number_input("long window (days)", min_value=50, max_value=300, value=200, step=1)
initial_capital = st.sidebar.number_input("start-up capital ($)", min_value=1000, value=10000)

# --- Start-Button ---
if st.sidebar.button("Start backtest"):
    if not ticker:
        st.error("Please enter a ticker symbol.")
    elif short_window >= long_window:
        st.error("The short window must be smaller than the long window.")
    else:
        with st.spinner("Load data and perform backtesting..."):
            try:
                # 1. Load data
                importer = YahooFinanceImporter()
                stock_data = importer.get_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                
                # 2. Generate signals
                strategy = MovingAverageStrategy(stock_data, short_window, long_window)
                signals = strategy.generate_signals()
                
                # 3. Run simulation
                backtester = Backtester(signals, initial_capital)
                portfolio = backtester.run_simulation()
                
                # --- Show results ---
                st.success("Backtest successfully completed!")

                # Display key figures
                final_value = portfolio['total'].iloc[-1]
                total_return = (final_value - initial_capital) / initial_capital * 100

                col1, col2, col3 = st.columns(3)
                col1.metric("initial money", f"${initial_capital:,.2f}")
                col2.metric("final capital", f"${final_value:,.2f}")
                col3.metric("total return", f"{total_return:.2f}%")

                # Show visualisation
                fig = plot_performance(portfolio, signals, ticker)
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"An error has occurred: {e}")