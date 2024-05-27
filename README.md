# EDGAR Financial Statement Retrieval and Analysis

This Python script enables users to easily retrieve and analyze financial statements (Income Statement, Balance Sheet, and Cash Flow Statement) from the SEC's EDGAR database for a specified company and filing type (10-K or 10-Q). The script offers features for exporting these statements as CSV files and combining them into a single JSON file for streamlined analysis. Ideal for investors, analysts, and researchers, this tool simplifies financial data extraction and organization.

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

```text
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

## Credits

This project utilizes the edgartools package developed by dgunning. Special thanks to [dgunning](https://github.com/dgunning/edgartools) for providing this useful tool for accessing EDGAR data.

## Project Goal

The ultimate goal of this project is to create a Retrieval-Augmented Generation (RAG) solution that pulls relevant company financials in a useful format for similarity search (JSON, CSV). This data will be combined with the business acumen of popular investors, both past and present, to provide insights for inference. The vision is to develop an LLM-driven financial advisor that leverages comprehensive data analysis and expert knowledge. Maybe not the most novel idea at this point, but we learn by doing after all.

## License

This project is licensed under the MIT License.