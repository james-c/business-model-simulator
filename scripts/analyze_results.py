#!/usr/bin/env python3
"""
Reads a CSV of simulation results from a parameter sweep and performs basic analysis.
"""

import csv
import argparse
import statistics

def analyze_sweep_results(csv_path):
    """
    Loads parameter sweep data from a CSV file and computes aggregate statistics
    for each parameter combination.
    """
    data = []
    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "combo_key": row["combo_key"],
                "business_model": row["business_model"],
                "step": int(row["step"]),
                "costs": float(row["costs"]),
                "revenues": float(row["revenues"])
            })

    # Group by combo_key
    results_by_combo = {}
    for record in data:
        key = record["combo_key"]
        if key not in results_by_combo:
            results_by_combo[key] = []
        results_by_combo[key].append(record)

    # Compute stats per combo
    for combo_key, records in results_by_combo.items():
        cost_values = [r["costs"] for r in records]
        revenue_values = [r["revenues"] for r in records]

        avg_cost = statistics.mean(cost_values)
        avg_revenue = statistics.mean(revenue_values)
        total_cost = sum(cost_values)
        total_revenue = sum(revenue_values)

        print(f"== Combination: {combo_key} ==")
        print(f"  Avg Cost:       {avg_cost:.2f}")
        print(f"  Avg Revenue:    {avg_revenue:.2f}")
        print(f"  Total Cost:     {total_cost:.2f}")
        print(f"  Total Revenue:  {total_revenue:.2f}")
        print("")

def main():
    parser = argparse.ArgumentParser(description="Analyze parameter sweep CSV results.")
    parser.add_argument(
        "--input_csv",
        type=str,
        default="data/output/parameter_sweep_results.csv",
        help="Path to the CSV file containing parameter sweep results."
    )
    args = parser.parse_args()
    analyze_sweep_results(args.input_csv)

if __name__ == "__main__":
    main()
