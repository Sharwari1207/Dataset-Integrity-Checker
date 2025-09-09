"""
Automated Data Quality Check Script
Author: Your Name
Year: 2025

This script performs automated data quality checks on a CSV dataset.
It detects:
- Missing values
- Duplicate records
- Anomalies (negative/zero values in numeric columns)

Generates: Excel report in /reports/ folder
"""

import pandas as pd
import os

def data_quality_check(input_file, output_file):
    # Load data
    df = pd.read_csv(input_file)

    # Create dictionary for results
    report = {}

    # Missing values check
    missing_values = df.isnull().sum()
    report["Missing Values"] = missing_values[missing_values > 0].to_dict()

    # Duplicate check
    duplicates = df.duplicated().sum()
    report["Duplicates"] = {"Total Duplicates": int(duplicates)}

    # Anomaly check (negative or zero values in numeric columns)
    anomaly_report = {}
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        negatives = df[df[col] < 0].shape[0]
        zeros = df[df[col] == 0].shape[0]
        if negatives > 0 or zeros > 0:
            anomaly_report[col] = f"{negatives} negative, {zeros} zero values"
    report["Anomalies"] = anomaly_report

    # Save report to Excel
    with pd.ExcelWriter(output_file) as writer:
        for key, value in report.items():
            pd.DataFrame(list(value.items()), columns=["Check", "Result"]).to_excel(writer, sheet_name=key, index=False)

    print(f"✅ Data quality report generated: {output_file}")


if __name__ == "__main__":
    # Define file paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "..", "data", "sample_data.csv")
    output_file = os.path.join(base_dir, "..", "reports", "data_quality_report.xlsx")

    # Run check
    if os.path.exists(input_file):
        data_quality_check(input_file, output_file)
    else:
        print(f"❌ Input file not found: {input_file}")
