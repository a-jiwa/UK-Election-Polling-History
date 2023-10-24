import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('monthly_averages.csv')

# Fill missing values in the 'Year' column
df['Year'].fillna(method='ffill', inplace=True)

# Replace 'GE' with NaN in other columns
df.replace('GE', np.nan, inplace=True)

# Convert 'Month' to a standard date format
df['Month'] = pd.to_datetime(df['Month'], format='%b-%y')

# Forward-fill missing values in other columns
df.fillna(method='ffill', inplace=True)

# Remove rows where either 'Month' or 'Year' is NaN
df.dropna(subset=['Month', 'Year'], how='any', inplace=True)

# Remove the 'Year' column
df.drop(columns=['Year'], inplace=True)

# Rename the 'Month' column to 'Date'
df.rename(columns={'Month': 'Date'}, inplace=True)

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_uk_polling_data.csv', index=False)

# Prepare data for JSON output
json_data = []

for _, row in df.iterrows():
    data_entry = {
        'Date': row['Date'].strftime('%Y-%m-%d') if not pd.isna(row['Date']) else None,
        'Conservative': row['Conservative'],
        'Labour': row['Labour'],
        'LD': row['LD'],
        'UKIP': row['UKIP'],
        'SDP': row['SDP'],
        'TIG': row['TIG'],
        'BXP': row['BXP'],
        'Green': row['Green'],
    }
    json_data.append(data_entry)

# Save the data as JSON
import json

with open('uk_polling_data.json', 'w') as json_file:
    json.dump(json_data, json_file)

print(df.head())
