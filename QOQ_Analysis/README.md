
# QoQ Analysis (SQL) - 40%

## Task Description
This project involves a data manipulation exercise using SQL to analyze site visits data on a quarter-over-quarter (QoQ) basis. The main tasks include generating reports and visualizations based on the provided datasets.

## Project Structure

### Directory Layout
- `scripts/`
  - `create_viz.py`: Script for creating visualizations.
  - `wiki_scrapping.py`: Script for scraping country name data from Wikipedia.
- `sql/`
  - `creation/`
    - `country_mapping.sql`: SQL script to create the country mapping table.
    - `site_cat_creation.sql`: SQL script to create the site category table.
    - `site_visits_creation.sql`: SQL script to create the site visits table.
  - `data/`
    - `copy_country_mapping.sql`: SQL script to copy data into the country mapping table.
    - `copy_site_category.sql`: SQL script to copy data into the site category table.
    - `copy_site_visits.sql`: SQL script to copy data into the site visits table.
  - `queries/`
    - `tests.sql`: SQL script for testing queries.
    - `top_qoq_changes.sql`: SQL script for the QoQ analysis.

### Data Files
- `site_category_source.csv`: Source data for site categories.
- `site_monthly_visits.csv`: Source data for site monthly visits.