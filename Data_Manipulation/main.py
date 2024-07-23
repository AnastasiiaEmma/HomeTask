from utils import read_data, extract_keywords, count_keywords, display_top_keywords

def main():
    # File path to the CSV file
    file_path = 'xxx/airbnb_clickstream_sample.csv'
    
    # Read data
    df = read_data(file_path)
    
    # Count keywords
    keyword_counter = count_keywords(df)
    
    # Display top keywords
    display_top_keywords(keyword_counter)

if __name__ == "__main__":
    main()
