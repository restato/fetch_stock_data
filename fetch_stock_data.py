import sys
from datetime import datetime

import pandas as pd
import yfinance as yf
from dateutil.relativedelta import relativedelta


def get_stock_data(stock_code, date_str):
    """
    Fetch historical stock prices for the given stock code and date range (2 months before and after the base date).
    Missing dates will be filled with NaN.
    """
    base_date = datetime.strptime(date_str, "%Y-%m-%d")
    start_date = base_date - relativedelta(months=2)
    end_date = base_date + relativedelta(months=2)

    try:
        ticker = yf.Ticker(stock_code)
        data = ticker.history(period="6mo")  # Fetch data for the past 6 months
        data.reset_index(inplace=True)

        # Convert 'Date' column to datetime and localize time zone
        data["Date"] = pd.to_datetime(data["Date"]).dt.tz_localize(None)

        # Filter data for the 2-month range
        filtered_data = data[(data["Date"] >= start_date) & (data["Date"] <= end_date)]

        # Create a complete date range and reindex to include missing dates
        all_dates = pd.date_range(start=start_date, end=end_date)
        filtered_data.set_index("Date", inplace=True)
        complete_data = filtered_data.reindex(all_dates).reset_index()
        complete_data.rename(columns={"index": "Date"}, inplace=True)

        # Format the date as YYYY-MM-DD
        complete_data["Date"] = complete_data["Date"].dt.strftime("%Y-%m-%d")

        # Return the data with missing dates filled as NaN
        return complete_data[["Date", "Close"]]
    except Exception as e:
        print(f"Error fetching data for {stock_code}: {e}")
        return None


def save_to_excel(data, file_name):
    """
    Save the stock data to an Excel file.
    """
    try:
        data.to_excel(file_name, index=False, engine="openpyxl")
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 fetch_stock_data.py <stock_code> <donation_date>")
        sys.exit(1)

    stock_code = sys.argv[1]
    donation_date = sys.argv[2]

    # Fetch stock data
    stock_data = get_stock_data(stock_code, donation_date)
    if stock_data is not None:
        # Save the data to an Excel file
        file_name = f"{stock_code}_{donation_date}_prices.xlsx"
        save_to_excel(stock_data, file_name)
