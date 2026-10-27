# Ship Fuel Efficiency Pipeline

A data engineering project using public EU MRV data to compare fuel efficiency across ship types.

## Data
EU MRV emissions reports from the THETIS-MRV site (EMSA), 2023: 12,829 ships.

## What's done so far
- clean_mrv.py loads the raw Excel file, keeps 10 key columns, fixes text values like "N/A" and "Division by zero!", merges duplicate ship type labels, and flags 200 inactive ships.

## Coming next
Azure storage, Databricks, Azure SQL, Data Factory and a Power BI dashboard.

## Run it
pip install pandas openpyxl
python clean_mrv.py mrv_2023.xlsx mrv_2023_clean.csv
