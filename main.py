import csv
import glob
import json
import os

import pandas as pd
from edgar import Company, set_identity
from edgar.financials import Financials


def get_financial_statement(financials,
                            filing_date,
                            company_name,
                            as_dataframe=False,
                            filing_type=None):
  """
  Prompts the user to select a financial statement and displays the selected statement.

  Args:
      financials (Financials): A Financials object containing the financial statements.
      filing_date (datetime.date): The filing date of the financial statement.
      company_name (str): The name of the company.
      as_dataframe (bool): Whether to return the financial statements as pandas dataframes.
      filing_type (str): The type of filing (10-K or 10-Q).
  """
  print("Which financial statement would you like to retrieve?")
  print("1. Income Statement")
  print("2. Balance Sheet")
  print("3. Cash Flow Statement")
  print("4. All Statements")
  statement_choice = input("Enter the number corresponding to your choice: ")

  statement_map = {
      "1": [("Income Statement", financials.income_statement)],
      "2": [("Balance Sheet", financials.balance_sheet)],
      "3": [("Cash Flow Statement", financials.cash_flow_statement)],
      "4": [("Income Statement", financials.income_statement),
            ("Balance Sheet", financials.balance_sheet),
            ("Cash Flow Statement", financials.cash_flow_statement)]
  }

  statements = statement_map.get(statement_choice)
  if statements is None:
    print("Invalid choice. Please enter either 1, 2, 3, or 4.")
  else:
    for statement_name, statement in statements:
      if as_dataframe:
        try:
          df = statement.to_dataframe()
          print(f"\n{statement_name} DataFrame:")
          print(df)

          export_choice = input(
              "Would you like to export the DataFrame as a CSV file? (y/n): ")
          if export_choice.lower() == 'y':
            filing_year = filing_date.year
            if filing_type == "10-Q":
              quarter = (filing_date.month - 1) // 3 + 1
              csv_filename = f"{company_name}_{statement_name.lower().replace(' ', '_')}_{filing_year}_Q{quarter}.csv"
            else:
              csv_filename = f"{company_name}_{statement_name.lower().replace(' ', '_')}_{filing_year}.csv"
            df.to_csv(csv_filename, index=True)
            print(f"DataFrame exported as {csv_filename}")
        except Exception as e:
          print(f"Error occurred while processing {statement_name}: {e}")
      else:
        print(f"\n{statement_name}:")
        print(statement)


def get_company_filings():
  """
    Prompts the user for a stock ticker and filing type, retrieves the specified filings,
    and displays the financial statements for each filing.
    """
  while True:
    # Allow the caller to enter the stock ticker
    stock_ticker = input("Enter the stock ticker: ")

    try:
      # Create a Company object with the entered ticker
      company = Company(stock_ticker)
      if company is None:
        print(
            f"The stock ticker '{stock_ticker}' does not exist. Please try again."
        )
        continue
      break
    except Exception as e:
      print(f"An error occurred: {e}")
      return

  # Display selection option for filing type
  print("Select the type of filing you'd like to retrieve:")
  print("1. 10-K")
  print("2. 10-Q")
  filing_choice = input("Enter the number corresponding to your choice: ")

  # Map the user's choice to the filing type
  filing_type_map = {"1": "10-K", "2": "10-Q"}
  filing_type = filing_type_map.get(filing_choice)

  if filing_type is None:
    print("Invalid choice. Please enter either 1 for 10-K or 2 for 10-Q.")
    return

  try:
    # Get the company's filings of the chosen type
    company_filings = company.get_filings(form=filing_type)

    # Check if there are any filings available
    if not company_filings:
      print(f"No {filing_type} filings found for {stock_ticker}.")
      return

    # Ask the caller for the number of filings they would like
    num_filings = int(
        input(
            f"Enter the number of {filing_type} filings you'd like to retrieve: "
        ))

    # Check if the requested number of filings is more than available
    available_filings = len(company_filings)
    if num_filings > available_filings:
      print(
          f"Only {available_filings} {filing_type} filings are available for {stock_ticker}. Retrieving all available filings."
      )

    # Ask the caller if they want the financials as pandas dataframes
    dataframe_choice = input(
        "Would you like the financials as pandas dataframes? (y/n): ")
    as_dataframe = dataframe_choice.lower() == 'y'

    # Retrieve and display the requested number of filings
    for i in range(min(num_filings, available_filings)):
      filing = company_filings[i]
      print(f"\n{filing_type} Filing #{i + 1}")
      print(f"Accession Number: {filing.accession_number}")
      print(f"Filing Date: {filing.filing_date}")

      if not as_dataframe:
        print("Filing Text Content:\n")
        print(filing.text)

      try:
        # Get the financial statements from the XBRL data
        financials = Financials.from_xbrl(filing.xbrl())
        if financials:
          get_financial_statement(financials, filing.filing_date, company.name,
                                  as_dataframe, filing_type)
        else:
          print(
              f"No financial statements found in the XBRL data for {filing_type} filing #{i + 1}."
          )
      except Exception as e:
        print(
            f"Error occurred while processing {filing_type} filing #{i + 1}: {e}"
        )
    return company.name
  except Exception as e:
    print(f"An error occurred: {e}")


import re
from datetime import datetime


def combine_csv_to_json(csv_files, company_name):
  """
    Combines the data from multiple CSV files into a single JSON file.

    Args:
        csv_files (list): A list of CSV file names to be combined.
        company_name (str): The name of the company.
    """
  data = []
  for file_name in csv_files:
    if os.path.exists(file_name):
      with open(file_name, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
          fact = row.get('Fact')
          label = row.get('Label')
          existing_entry = next(
              (entry for entry in data
               if entry.get('Fact') == fact and entry.get('Label') == label),
              None)
          if existing_entry:
            existing_entry.update({
                k: v
                for k, v in row.items()
                if k not in ['Fact', 'Label'] and k not in existing_entry
            })
          else:
            data.append(row)
    else:
      print(f"File not found: {file_name}")

  for entry in data:
    date_keys = [k for k in entry.keys() if re.match(r'\d{4}-\d{2}-\d{2}', k)]
    date_keys.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d'),
                   reverse=True)
    entry.update({k: entry.pop(k) for k in date_keys})

  json_data = {"Company": company_name, "Data": data}
  json_data = json.dumps(json_data, indent=2)

  # Export the JSON data to a file with the company name
  json_filename = f"{company_name}_combined_financial_data.json"
  with open(json_filename, 'w') as json_file:
    json_file.write(json_data)

  print(f"Combined JSON data exported as {json_filename}")


def main():
  """
  The main function that sets the EDGAR identity, calls the get_company_filings function,
  and combines the exported CSV files into a JSON file.
  """
  # Set the identity for EDGAR
  set_identity(os.environ['EDGAR_IDENTITY'])

  company_name = get_company_filings()

  # Get the list of exported CSV files
  csv_files = glob.glob("*.csv")

  if csv_files:
    # Combine the exported CSV files into a JSON file
    combine_csv_to_json(csv_files, company_name)
  else:
    print("No exported CSV files found.")


if __name__ == "__main__":
  main()
