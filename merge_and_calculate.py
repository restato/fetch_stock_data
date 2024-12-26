import glob

import pandas as pd


def merge_pivot_and_calculate_average(output_file):
    """
    Merge all Excel files, handle duplicate dates by averaging values, pivot data,
    and calculate average closing prices for each stock.
    """
    # Find all Excel files
    excel_files = glob.glob("*.xlsx")
    if not excel_files:
        print("No Excel files found in the current directory.")
        return

    merged_data = []

    # Read each Excel file
    for file in excel_files:
        # Extract stock code from the file name
        stock_code = file.split("_")[0]

        # Read Excel file
        df = pd.read_excel(file, engine="openpyxl")
        df["Stock"] = stock_code  # Add stock code as a column

        # Append to the merged list
        merged_data.append(df)

    # Concatenate all dataframes
    merged_df = pd.concat(merged_data, ignore_index=True)

    # Handle duplicate entries: calculate average for each Stock and Date
    merged_df = merged_df.groupby(["Date", "Stock"], as_index=False)["Close"].mean()

    # Pivot the data so that Date is the index and Stock codes are columns
    pivot_df = merged_df.pivot(index="Date", columns="Stock", values="Close")

    # Calculate the average closing price for each stock
    stock_averages = pivot_df.mean().reset_index()
    stock_averages.columns = ["Stock", "Average_Close"]

    # Save the pivoted data and stock averages to an Excel file
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        pivot_df.to_excel(writer, sheet_name="Pivoted_Data")
        stock_averages.to_excel(writer, index=False, sheet_name="Averages")

    print(f"Pivoted data and averages saved to {output_file}")


if __name__ == "__main__":
    # Output file name for the merged Excel
    output_file = "pivoted_stock_data_with_averages.xlsx"
    merge_pivot_and_calculate_average(output_file)
