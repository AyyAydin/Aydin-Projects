# Stock Earnings Fetcher - Updated for yfinance 2025+
# Author: Aydin Chowdhury
# Description:
#   Fetches financial data (revenue, net income, etc.) for given tickers,
#   saves CSV summaries, and generates basic revenue plots.

import argparse
import datetime
import logging
import os
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

LOG = logging.getLogger('earnings_fetcher')
LOG.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
LOG.addHandler(handler)

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_financials(ticker):
    LOG.info(f'Fetching data for {ticker}')
    t = yf.Ticker(ticker)
    try:
        income = t.quarterly_income_stmt
        if income is None or income.empty:
            income = t.income_stmt

        if income is None or income.empty:
            LOG.warning(f'No income statement for {ticker}')
            return None, {}

        df = pd.DataFrame(income)

        # rotate so rows=dates, columns=financial metrics
        if isinstance(df.columns[0], pd.Timestamp):
            df = df.T

        info = t.get_info() if hasattr(t, "get_info") else t.info
        return df, info

    except Exception as e:
        LOG.error(f'Error fetching data for {ticker}: {e}')
        return None, {}


def save_csv(df, ticker):
    """Save DataFrame to CSV file."""
    fname = os.path.join(OUTPUT_DIR, f'{ticker}_financials_{datetime.date.today().isoformat()}.csv')
    df.to_csv(fname, index=True)
    LOG.info(f'Saved CSV: {fname}')
    return fname

def plot_metric(df, ticker):
    """Plot Net Income or Revenue over time."""

    # Ensure DataFrame is oriented correctly: rows=dates, columns=metrics
    if isinstance(df.columns[0], pd.Timestamp):
        df = df.T

    # Try to find a revenue/income-like column
    col_candidates = [
        c for c in df.columns 
        if isinstance(c, str) and (
            "revenue" in c.lower() or 
            "income" in c.lower() or
            "sales" in c.lower()
        )
    ]

    if not col_candidates:
        LOG.warning(f"No plottable financial metrics found for {ticker}")
        return

    target_col = col_candidates[0]  # choose first match

    # Clean data
    series = df[target_col].dropna().astype(float)

    if series.empty:
        LOG.warning(f"No data available for plotting {target_col} for {ticker}")
        return

    # Plot
    plt.figure(figsize=(6,3))
    series.plot(marker='o')
    plt.title(f'{ticker} - {target_col}')
    plt.xlabel("Date")
    plt.ylabel("Amount (USD)")
    plt.tight_layout()
    
    out = os.path.join(OUTPUT_DIR, f'{ticker}_{target_col}.png')
    plt.savefig(out)
    plt.close()
    LOG.info(f'Saved plot: {out}')


def main():
    parser = argparse.ArgumentParser(description='Stock Earnings Fetcher')
    parser.add_argument('--symbols', nargs='+', required=True, help='List of tickers (e.g., AAPL MSFT TSLA)')
    args = parser.parse_args()

    summary_rows = []
    for symbol in args.symbols:
        df, info = fetch_financials(symbol)
        if df is None or df.empty:
            continue

        save_csv(df, symbol)
        plot_metric(df, symbol)

        summary_rows.append({
            'ticker': symbol,
            'company': info.get('shortName', 'N/A'),
            'last_price': info.get('currentPrice', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A')
        })

    if summary_rows:
        summary = pd.DataFrame(summary_rows)
        summary_file = os.path.join(OUTPUT_DIR, f'summary_{datetime.date.today().isoformat()}.csv')
        summary.to_csv(summary_file, index=False)
        LOG.info(f'Summary saved to {summary_file}')
    else:
        LOG.warning("No valid financial data retrieved. Check ticker symbols or API limits.")

if __name__ == '__main__':
    main()
