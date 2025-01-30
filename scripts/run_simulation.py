#!/usr/bin/env python3
"""
Example script for running a parameter sweep using the Simulator
with multiple parameters across several discrete steps.
"""

import os
import csv
import itertools
import numpy as np

from simulator.simulator import Simulator
from simulator.business_model import BusinessModel
from simulator.transaction_model import TransactionModel
from simulator.operation import Operation

def create_business_model(combo_params):
    """
    Factory function that creates a new BusinessModel (and underlying
    TransactionModel/Operations) for the given parameter combination.
    """
    # Example operation
    sample_op = Operation(
        name="SampleOperation",
        parameters={
            "base_transaction_volume": 100,
            "direct_cost": 2.0,
            "variable_cost": 0.8,
            "kyc_fee": 5.0,           # if relevant for contract_complexity
            "base_revenue": 5.0,
            "revenue_per_unit": 2.0
        },
        contract_complexity="High"
    )

    # Attach the operation to a TransactionModel
    tx_model = TransactionModel(
        operations=[sample_op],
        parameters={
            "growth_rate": combo_params.get("growth_rate", 0.0),
            "overhead_rate": combo_params.get("overhead_rate", 0.0),
            "revenue_factor": combo_params.get("revenue_factor", 1.0),
            "revenue_tax_rate": 0.02
        }
    )

    # Create the business model
    bm = BusinessModel(
        name="ParameterSweepModel",
        transaction_model=tx_model,
        parameters={}
    )
    return bm

def run_parameter_sweep(
    simulation_period=5, 
    output_csv="data/output/parameter_sweep_results.csv"
):
    """
    Runs a parameter sweep with multiple parameters each spanning several steps,
    creating multiple simulation runs. Writes results to a CSV.
    """
    # Example parameter ranges (adjust as needed)
    growth_rates = np.arange(0.0, 0.26, 0.05)      # 0.00, 0.05, 0.10, 0.15, 0.20, 0.25
    overhead_rates = np.arange(0.0, 0.12, 0.02)    # 0.00, 0.02, 0.04, 0.06, 0.08, 0.10
    revenue_factors = np.arange(1.0, 1.31, 0.05)   # 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30

    growth_rates = growth_rates.tolist()
    overhead_rates = overhead_rates.tolist()
    revenue_factors = revenue_factors.tolist()

    sweep_results = {}

    # Cartesian product of all parameter combinations
    for gr, oh, rf in itertools.product(growth_rates, overhead_rates, revenue_factors):
        sim = Simulator(simulation_period=simulation_period)

        combo_params = {
            "growth_rate": gr,
            "overhead_rate": oh,
            "revenue_factor": rf
        }
        bm = create_business_model(combo_params)
        sim.add_business_model(bm)

        sim.run_simulation()
        run_results = sim.collect_results()

        combo_key = f"GR={gr:.2f}_OH={oh:.2f}_RF={rf:.2f}"
        sweep_results[combo_key] = run_results

    write_sweep_results_to_csv(sweep_results, output_csv)
    print(f"Parameter sweep complete. Results saved to {output_csv}.")

def write_sweep_results_to_csv(sweep_results, csv_path):
    """
    Writes the sweep results dictionary to a CSV file.
    The dictionary is expected to look like:
    {
      "GR=0.00_OH=0.00_RF=1.00": {
         "ParameterSweepModel": [
           {"step": 0, "costs": X, "revenues": Y}, ...
         ]
      },
      ...
    }
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    fieldnames = ["combo_key", "business_model", "step", "costs", "revenues"]
    with open(csv_path, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for combo_key, model_dict in sweep_results.items():
            for model_name, step_list in model_dict.items():
                for record in step_list:
                    writer.writerow({
                        "combo_key": combo_key,
                        "business_model": model_name,
                        "step": record["step"],
                        "costs": record["costs"],
                        "revenues": record["revenues"]
                    })

def main():
    run_parameter_sweep(
        simulation_period=10, 
        output_csv="data/output/parameter_sweep_results.csv"
    )

if __name__ == "__main__":
    main()
