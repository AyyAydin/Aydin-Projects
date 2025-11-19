Stock Earnings Fetcher
A Python-based financial data analysis tool that retrieves income statements, revenue, and net income for any publicly traded company using the Yahoo Finance API (`yfinance`).  

---

Features
- Fetches quarterly or annual income statements for any stock ticker.
- Automatically handles updated Yahoo Finance formats (2025+).
- Generates:
  - Financial CSV files
  - Revenue / Net Income time-series plots
  - Summary CSV with company name, sector, industry, and latest price
- Supports multiple tickers at once.
- Clean logging and error handling.
- Organized `output/` folder for saved results.

---

Installation

1. Clone the repo
git clone https://github.com/AyyAydin/aydin-projects.git
cd aydin-projects/stock_earnings_fetcher

2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate

3. Install dependencies
pip install -r requirements.txt

Usage
Run the script with one or more stock tickers:
python main.py --symbols AAPL MSFT TSLA

Analyze many tickers at once:
python main.py --symbols AAPL MSFT NVDA AMZN GOOG META JPM BAC NFLX


Output Structure
You will see:

output/
│
├── AAPL_financials_2025-11-13.csv
├── AAPL_Net Income.png
├── MSFT_financials_2025-11-13.csv
├── MSFT_Total Revenue.png
└── summary_2025-11-13.csv


How It Works
1. Fetch Financials
Pulls quarterly income statement (quarterly_income_stmt)
Falls back to annual (income_stmt)
Rotates DataFrame so rows = dates and columns = metrics

2. Identify financial metrics
Searches for columns containing:
"revenue"
"income"
"sales"

3. Plot results
Generates .png line graphs showing:
Net Income trend
Revenue trend

4. Summary File
Creates a CSV including:
Ticker
Company name
Sector
Industry
Latest stock price

Technologies Used
Python
yFinance
Pandas
Matplotlib
Virtual Environments
Logging
