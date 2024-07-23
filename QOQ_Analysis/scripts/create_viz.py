import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection details
host = 'xxx'
port = 'xxx'
dbname = 'xxx'
user = 'xxx'
password = 'xxx'

# Create an engine
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')

# Load data
site_visits_query = 'SELECT * FROM site_monthly_visits'
category_query = 'SELECT * FROM site_category'
country_query = 'SELECT * FROM country_mapping'

# Load data into DataFrames
site_visits_df = pd.read_sql(site_visits_query, engine)
category_df = pd.read_sql(category_query, engine)
country_df = pd.read_sql(country_query, engine)

# Merge site visits with categories
merged_df = pd.merge(site_visits_df, category_df, on='site', how='left')

# Calculate average monthly visits for each site
merged_df['avg_monthly_visits'] = merged_df.groupby(['site'])['visits'].transform('mean')

# Aggregate the average monthly visits by category and country
agg_avg_monthly_visits = merged_df.groupby(['country', 'category']).agg({'avg_monthly_visits': 'mean'}).reset_index()

# Merge with country names
agg_avg_monthly_visits = pd.merge(agg_avg_monthly_visits, country_df, on='country', how='left')

# Sort by avg_monthly_visits to identify the most failing categories
agg_avg_monthly_visits = agg_avg_monthly_visits.sort_values(by='avg_monthly_visits')

# Identify the top 5 failing categories
failing_categories_df = agg_avg_monthly_visits.groupby('country').head(5)

# Plot the data
plt.figure(figsize=(14, 8))
sns.barplot(data=failing_categories_df, x='country_name', y='avg_monthly_visits', hue='category')
plt.title('Top 5 Most Failing Categories Across Countries by Average Monthly Visits')
plt.xlabel('Country')
plt.ylabel('Average Monthly Visits')
plt.xticks(rotation=45)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()
