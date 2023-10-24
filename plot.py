import matplotlib.pyplot as plt
import pandas as pd
import json
import os

# Load cleaned polling data
polling_data = pd.read_csv('cleaned_uk_polling_data.csv')
polling_data['Date'] = pd.to_datetime(polling_data['Date'])

# Load elections data
elections = pd.read_csv('elections.csv')
elections['Date'] = pd.to_datetime(elections['Date'])

# Check if directories exist, if not, create them
if not os.path.exists('json_files'):
    os.makedirs('json_files')

if not os.path.exists('charts'):
    os.makedirs('charts')


# Define a function to create individual JSON files for each general election
def create_election_json(election_date, current_election_row, polling_data, elections):
    # Filter polling data for the 3-year period leading up to the election
    start_date = election_date - pd.DateOffset(years=3)
    end_date = election_date
    filtered_polling_data = polling_data[(polling_data['Date'] >= start_date) & (polling_data['Date'] <= end_date)].copy()  # Creating a copy here

    # Convert Date to string so it's JSON serializable, you might want to adjust the format
    filtered_polling_data['Date'] = filtered_polling_data['Date'].dt.strftime('%Y-%m-%d')

    # Create a data structure for D3, consisting of a list of dictionaries
    d3_json = {
        'electionYear': current_election_row["Year"],
        'data': filtered_polling_data.to_dict('records')
    }

    # Save the data to a JSON file
    filename = f'json_files/election_data_{current_election_row["Year"]}.json'
    with open(filename, 'w') as json_file:
        json.dump(d3_json, json_file)

# Define a function to create individual charts for each general election
def create_election_chart(election_date, current_election_row, polling_data, elections):
    # Filter polling data for the 3-year period leading up to the election
    start_date = election_date - pd.DateOffset(years=3)
    end_date = election_date
    filtered_polling_data = polling_data[(polling_data['Date'] >= start_date) & (polling_data['Date'] <= end_date)].copy()  # Creating a copy here

    # Create a new figure and axis for the chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot polling data for each party
    ax.plot(filtered_polling_data['Date'], filtered_polling_data['Conservative'], label='Conservative', color='#0087DC')
    ax.plot(filtered_polling_data['Date'], filtered_polling_data['Labour'], label='Labour', color='#DC241f')
    ax.plot(filtered_polling_data['Date'], filtered_polling_data['LD'], label='Lib Dem', color='#FDBB30')

    # Set the title using the correct election_row passed to the function
    ax.set_title(
        f'UK Polling Data Leading to {current_election_row["Year"]} General Election ({current_election_row["Party leader(s)"]})')

    # Add vertical lines for the election and previous elections (faintly)
    for idx, past_election_row in elections.iterrows():
        election_year = past_election_row['Year']
        election_date = past_election_row['Date']

        if start_date <= election_date <= end_date:
            ax.axvline(election_date, color='k', linestyle='--', label=f'{election_year} Election')
        elif start_date < election_date < end_date:
            ax.axvline(election_date, color='k', linestyle='--', alpha=0.2)

    # Set labels and legend
    ax.set_xlabel('Date')
    ax.set_ylabel('Percentage')

    ax.legend()

    # Show the plot
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()

    # Save the plot
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = f'charts/election_chart_{current_election_row["Year"]}.png'
    plt.savefig(filename)  # you can specify the directory path as well; ensure it exists
    plt.close()  # Close the figure

# Create individual JSON files for each general election
for idx, election_row in elections.iterrows():
    election_date = election_row['Date']
    create_election_json(election_date, election_row, polling_data, elections)
    create_election_chart(election_date, election_row, polling_data, elections)
