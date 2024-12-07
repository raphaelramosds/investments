import tabula
import re
import pandas as pd
import statistics
import os

def get_values_from(column: pd.Series) -> list:
    """
    Extracts and converts values from a Pandas Series that are in Brazilian currency format (BRL).
    
    Args:
        column (pd.Series): A Pandas Series containing string values representing currency.

    Returns:
        list: A list of float values converted from the currency format.
    """
    # Regular expression pattern to match Brazilian currency (e.g., '1.234,56')
    exp = r'^\d{1,3}(\.\d{3})*,\d{2}'
    return list(
        # Map through each matched value, converting to float by replacing '.' and ',' accordingly
        map(lambda x: float(x.replace(".", "").replace(",", ".")), 
            # Match the currency format in each value and extract it
            [re.match(exp, v).group() for v in column])
    )

# List all files in the 'rendimentos' directory
files = os.listdir('rendimentos')

# Filter out only PDF files from the list of files
periods = list(filter(lambda x: re.fullmatch(r'^.*\.pdf$', x), files))

# Initialize an empty list to store the calculated interest rates
rates = []

# Loop through each PDF file (representing a period)
for p in periods:

    print(f"Reading {p} ...")

    # Read all the pages of the PDF using tabula, which extracts tables into dataframes
    data = tabula.read_pdf(f'rendimentos/{p}', pages='all')

    # Concatenate all extracted tables into one dataframe
    settlements = pd.concat([*data], ignore_index=True)

    # Initialize empty lists to store balance and value information
    balances = []
    values = []

    # Filter the dataframe to rows where the 'Histórico' column equals 'CRED JUROS'
    df = settlements[settlements['Histórico'] == 'CRED JUROS']

    # Extract balance values from the 'Saldo' column and value entries from the 'Valor' column
    balances.extend(get_values_from(df['Saldo']))
    values.extend(get_values_from(df['Valor']))

    # Calculate the absolute sum of values for the period (total credited interest)
    rate_abs = sum(values)
    
    # Calculate the average balance
    balances_avg = statistics.mean(balances)

    # Calculate the interest rate as a percentage (interest divided by average balance)
    rates.append(100 * rate_abs / balances_avg)

    print(f"Done.")

# Calculate and print the average interest rate across all periods
print(statistics.mean(rates))
