# 📈 Interactive Trading Strategy Backtester

An interactive web application built with Python and Streamlit to backtest various trading strategies on historical stock data. This tool allows users to dynamically input parameters and instantly visualize the performance results.



## ✨ Key Features

- **Interactive Web Interface:** A user-friendly UI to easily change the ticker symbol, date range, and strategy parameters.

- **Multiple Strategies:** Test and compare different trading philosophies, including trend-following and mean-reversion.

- **Dynamic Visualizations:** Generates interactive charts with Plotly, allowing users to hover for details, zoom, and pan.

- **Comprehensive Analysis:** The output includes key performance metrics, an equity curve, and a price chart with trade markers.

- **Modular Backend:** Built on a reusable FinancialDataImporter package and a flexible strategy pattern, making it easy to add new strategies.




## 📊 Trading Strategies Explained

This application allows you to test and compare the following strategies:

#### 1. Moving Average (MA) Crossover
This is a classic **trend-following** strategy. The core idea is to identify the start of a new trend by observing the relationship between a short-term and a long-term moving average.

- **Short-Term MA (e.g., 50 days):** Reacts quickly to recent price changes.

- **Long-Term MA (e.g., 200 days):** Represents the established, underlying trend.

**Trading Signals:**

- 📈 **Buy Signal (Golden Cross):** Occurs when the **short-term MA** crosses **above** the **long-term MA**. This suggests that recent positive momentum may be starting a new uptrend.

- 📉 **Sell Signal (Death Cross):** Occurs when the **short-term MA** crosses **below** the **long-term MA**. This indicates that recent negative momentum may be starting a new downtrend.

#### 2. Relative Strength Index (RSI)

This is a **momentum oscillator** used to identify overbought or oversold conditions. The RSI moves between 0 and 100. The strategy implemented here is a form of **mean reversion**.

- **Overbought:** An RSI value above a certain threshold (e.g., 70) suggests the asset might be overvalued and due for a price correction downwards.

- **Oversold:** An RSI value below a certain threshold (e.g., 30) suggests the asset might be undervalued and due for a price rebound upwards.

**Trading Signals:**

- 📈 **Buy Signal:** A buy signal is generated when the RSI crosses **below** the "Oversold" threshold (e.g., 30).

- 📉 **Sell Signal:** A sell signal is generated when the RSI crosses **above** the "Overbought" threshold (e.g., 70).

#### 3. Buy and Hold
This is not an active trading strategy but a crucial **benchmark**. It answers the question: "Did my active strategy perform better than simply buying the stock and holding it for the entire period?"

**Trading Signals:**

- 📈 **Buy Signal:** Buy on the very first day of the selected date range.

- 📉 **Sell Signal:** Never. The position is held until the end of the period.
## 🚀 Installation

To run this application locally, please follow these steps.

#### 1. Clone the repository:

```bash
git clone https://github.com/your_username/MovingAverageBacktester.git
cd MovingAverageBacktester
```

####  Install dependencies:

The `requirements.txt` file contains all necessary packages. Install them with a single command:

```bash
pip install -r requirements.txt
```
## ▶️ Running the App

Once the setup is complete, launch the Streamlit application from your terminal:

```bash
streamlit run app.py
```

Your web browser will automatically open with the running application.


## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

