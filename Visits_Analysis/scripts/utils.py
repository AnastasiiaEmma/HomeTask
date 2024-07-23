import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    """Load the CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def filter_visits_with_upgrade_success(df):
    """Filter visits that contain 'upgradeSuccess' in the 'pages' column."""
    return df[df['pages'].str.contains("upgradeSuccess", na=False)]

def calculate_metrics(filtered_visits):
    """Calculate metrics for the filtered visits."""
    filtered_visits['date'] = pd.to_datetime(filtered_visits['date'], format='%d-%m-%y')

    # Number of visits per day and overall
    visits_per_day = filtered_visits.groupby(filtered_visits['date'].dt.date).size().reset_index(name='num_visits')
    total_visits = filtered_visits.shape[0]

    # Number of unique users per day and overall
    unique_users_per_day = filtered_visits.groupby(filtered_visits['date'].dt.date)['user'].nunique().reset_index(name='unique_users')
    total_unique_users = filtered_visits['user'].nunique()

    # Average number of unique pages viewed within the site between the start of a session to a successful upgrade
    filtered_visits['unique_pages'] = filtered_visits['pages'].apply(lambda x: len(set(x.split(','))))
    average_unique_pages = filtered_visits['unique_pages'].mean()

    # Create a summary table
    summary_table = pd.DataFrame({
        'Metric': ['Total Visits', 'Total Unique Users', 'Average Unique Pages'],
        'Value': [total_visits, total_unique_users, average_unique_pages]
    })

    return visits_per_day, unique_users_per_day, summary_table

def calculate_cohorts(df):
    """Calculate cohorts for visit durations."""
    df['timeonsite_seconds'] = df['timeonsite'] / 1000

    # Define cohorts
    bins = [0, 20, 40, 60, 100, 200, df['timeonsite_seconds'].max()]
    labels = ['0-20', '20-40', '40-60', '60-100', '100-200', '200+']

    # Create cohorts
    df['cohort'] = pd.cut(df['timeonsite_seconds'], bins=bins, labels=labels, right=False)

    # Calculate number of users in each cohort
    cohort_counts = df['cohort'].value_counts().sort_index().reset_index()
    cohort_counts.columns = ['Visit duration cohort', 'Number of users']

    # Calculate the share of users in each cohort
    total_users = df['user'].nunique()
    cohort_counts['Share of users'] = (cohort_counts['Number of users'] / total_users) * 100

    return cohort_counts

def visualize_results(cohort_counts):
    """Visualize the cohort analysis results."""
    plt.figure(figsize=(10, 6))
    plt.bar(cohort_counts['Visit duration cohort'], cohort_counts['Number of users'], color='skyblue')
    plt.xlabel('Visit Duration Cohort (seconds)')
    plt.ylabel('Number of Users')
    plt.title('Cohort Analysis of Visit Durations')
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.pie(cohort_counts['Share of users'], labels=cohort_counts['Visit duration cohort'], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Share of Users in Each Visit Duration Cohort')
    plt.show()
