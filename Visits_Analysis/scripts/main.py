from utils import load_data, filter_visits_with_upgrade_success, calculate_metrics, calculate_cohorts, visualize_results

def main():
    file_path = 'xxx/zoom_us_visits_05_20.csv'
    df = load_data(file_path)

    filtered_visits = filter_visits_with_upgrade_success(df)
    visits_per_day, unique_users_per_day, summary_table = calculate_metrics(filtered_visits)

    print("Visits per day:")
    print(visits_per_day)
    print("\nUnique users per day:")
    print(unique_users_per_day)
    print("\nSummary table:")
    print(summary_table)

    cohort_counts = calculate_cohorts(df)
    print("\nCohort analysis:")
    print(cohort_counts)

    visualize_results(cohort_counts)

if __name__ == "__main__":
    main()
