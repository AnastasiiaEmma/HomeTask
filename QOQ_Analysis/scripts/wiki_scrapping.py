import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/ISO_3166-1"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize a list to store the country data
country_data = []

# Find the specific table with class 'wikitable sortable sticky-header'
table = soup.find('table', {'class': 'wikitable sortable sticky-header'})

if table:
    print("Target table found.")
    
    # Extract the table headers
    headers = [header.text.strip() for header in table.find_all('th')]
    print("Headers found:", headers)
    
    # Extract the table rows
    rows = table.find_all('tr')

    # Loop through the rows and extract the data
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 3:  
            country_name = columns[0].get_text(separator=" ").strip()
            numeric_code = columns[3].get_text(separator=" ").strip()
            country_data.append((country_name, numeric_code))

    # Create a DataFrame from the extracted data
    df_country_codes = pd.DataFrame(country_data, columns=['country_name', 'country'])

    # Display the DataFrame
    print(df_country_codes)

    # Save the DataFrame to a CSV file
    df_country_codes.to_csv('country_codes_mapping.csv', index=False)
else:
    print("Target table not found.")
