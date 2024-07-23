import pandas as pd
import re
from collections import Counter
from urllib.parse import unquote, urlparse, parse_qs

def read_data(file_path):
    """
    Reads a CSV file and returns a DataFrame.

    Args:
        file_path (str): The file path to the CSV file.

    Returns:
        DataFrame: A pandas DataFrame containing the CSV data.
    """
    return pd.read_csv(file_path)

def extract_keywords(url):
    """
    Extracts and formats keywords from a given URL.

    Args:
        url (str): The URL string to extract keywords from.

    Returns:
        str: A formatted keyword string.
    """
    formatted_keyword = ""

    # Extract from /s/ path
    path_pattern = r'/s/([^/?]*)'
    path_matches = re.findall(path_pattern, url)
    if path_matches:
        raw_keyword = path_matches[0]
        keyword_parts = raw_keyword.split('--')
        formatted_keyword = ", ".join(part.replace('-', ' ').title() for part in keyword_parts)
    
    # Extract from query parameters
    if not formatted_keyword:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if 'location' in query_params:
            raw_keyword = query_params['location'][0]
            formatted_keyword = ", ".join(part.strip().title() for part in raw_keyword.split(','))

    return unquote(formatted_keyword)

def is_valid_keyword(keyword):
    """
    Checks if a keyword is valid based on predefined patterns.

    Args:
        keyword (str): The keyword string to validate.

    Returns:
        bool: True if the keyword is valid, False otherwise.
    """
    invalid_patterns = [r'^__.*__$', r'^[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]-[a-z]$']
    for pattern in invalid_patterns:
        if re.match(pattern, keyword):
            return False
    return True

def count_keywords(df):
    """
    Counts the occurrences of keywords in a DataFrame of URLs.

    Args:
        df (DataFrame): A pandas DataFrame containing URL data.

    Returns:
        Counter: A Counter object with keyword frequencies.
    """
    keyword_counter = Counter()
    for url in df['Page']:
        keyword = extract_keywords(url)
        if keyword and is_valid_keyword(keyword):
            keyword_counter.update([keyword])
    return keyword_counter

def display_top_keywords(counter, top_n=20):
    """
    Displays the top N keywords and their frequencies.

    Args:
        counter (Counter): A Counter object with keyword frequencies.
        top_n (int, optional): The number of top keywords to display. Defaults to 20.
    """
    top_keywords = counter.most_common(top_n)
    for keyword, count in top_keywords:
        print(f'{keyword}: {count}')