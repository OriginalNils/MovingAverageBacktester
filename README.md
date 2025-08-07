
# 📈 Interactive Moving Average Strategy Backtester

This project is an interactive web application built with Streamlit to backtest the Moving Average Crossover trading strategy on historical stock data. Users can dynamically input parameters and instantly visualize the performance results.



## ✨ Key Features

- **Interactive Web Interface:** A user-friendly web app built entirely in Python using Streamlit.

- **Customizable Parameters:** Easily change the ticker symbol, date range, moving average windows, and initial capital directly in the UI.

- **Dynamic Visualizations:** Generates interactive charts with Plotly, allowing users to hover for details, zoom, and pan.

- **Comprehensive Analysis:** The output includes:

    - Key performance metrics (Initial Capital, Final Capital, Total Return).

    - An equity curve showing portfolio value, cash, and holdings over time.

    - A price chart displaying the moving averages and buy/sell trade markers.

- **Modular Backend:** Built on a reusable `FinancialDataImporter` package with intelligent caching to minimize API calls.


## 🚀 Installation

To run this application locally, please follow these steps.

#### 1. Clone the repository:

```bash
git clone https://github.com/your_username/MovingAverageBacktester.git
cd MovingAverageBacktester
```

#### 2. Install dependencies:

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

