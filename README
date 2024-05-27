# EDGAR Financial Statement Retrieval and Analysis

This Python script allows you to retrieve financial statements (Income Statement, Balance Sheet, and Cash Flow Statement) from the SEC's EDGAR database for a specified company and filing type (10-K or 10-Q). It provides functionality to export the financial statements as CSV files and combines the exported CSV files into a single JSON file for further analysis.

## Features

- Retrieve financial statements for a given stock ticker and filing type (10-K or 10-Q)
- Export financial statements as CSV files with naming conventions based on company name, statement type, filing year, and quarter (for 10-Q)
- Combine exported CSV files into a single JSON file with the company name included in the file name
- Handle errors and provide informative messages for invalid stock tickers or missing filings
- Interactive command-line interface for easy usage

## Prerequisites

- Python 3.x
- Required Python packages: edgar, pandas

## Usage

1. Set your EDGAR identity by providing your email address in the EDGAR_IDENTITY environment variable.
2. Run the script and follow the prompts to enter the stock ticker and select the filing type (10-K or 10-Q).
3. Choose the desired financial statements to retrieve (Income Statement, Balance Sheet, Cash Flow Statement, or All Statements).
4. Optionally, export the financial statements as CSV files and choose to combine the exported CSV files into a single JSON file.

## Example

```bash
$ python financial_statement_retrieval.py

Enter the stock ticker: AAPL
Select the type of filing you'd like to retrieve:
1. 10-K
2. 10-Q
Enter the number corresponding to your choice: 1
Enter the number of 10-K filings you'd like to retrieve: 3
Would you like the financials as pandas dataframes? (y/n): y

Income Statement DataFrame:
...
Would you like to export the DataFrame as a CSV file? (y/n): y
DataFrame exported as Apple Inc._income_statement_2022.csv

Balance Sheet DataFrame:
...
Would you like to export the DataFrame as a CSV file? (y/n): y
DataFrame exported as Apple Inc._balance_sheet_2022.csv

Cash Flow Statement DataFrame:
...
Would you like to export the DataFrame as a CSV file? (y/n): y
DataFrame exported as Apple Inc._cash_flow_statement_2022.csv

Combined JSON data exported as Apple Inc._combined_financial_data.json
```

##License
This project is licensed under the MIT License.