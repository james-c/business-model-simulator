import numpy as np
from simulator.simulator import Simulator
from simulator.business_model import BusinessModel
from simulator.transaction_model import TransactionModel
from .example_operation import RegistrationOperation

def business_model_factory(combo_params):
    reg_op = RegistrationOperation(
        name="UserRegistration",
        parameters={
            "base_transaction_volume": 50,
            "direct_cost": 2.0,
            "variable_cost": 1.0,
            "kyc_fee": 10.0,
            "base_revenue": 5.0,
            "revenue_per_unit": 1.0,
        },
        contract_complexity="High"
    )
    tx_model = TransactionModel(
        operations=[reg_op],
        parameters={
            "growth_rate": combo_params.get("growth_rate", 0.0),
            "overhead_rate": combo_params.get("overhead_rate", 0.0),
            "revenue_factor": combo_params.get("revenue_factor", 1.0),
            "revenue_tax_rate": 0.02
        }
    )
    bm = BusinessModel(
        name="ParamSweepBusiness",
        transaction_model=tx_model,
        parameters={}
    )
    return bm

def run_parameter_sweep_example():
    # Construct param_grid using numpy's arange for step-based increments
    growth_rates = list(np.arange(0.0, 0.101, 0.01))      # 0.0, 0.01, ... , 0.1
    overhead_rates = list(np.arange(0.0, 0.051, 0.01))    # 0.0, 0.01, ... , 0.05
    revenue_factors = list(np.arange(1.0, 1.21, 0.05))    # 1.0, 1.05, 1.1, 1.15, 1.2

    param_grid = {
        "growth_rate": growth_rates,
        "overhead_rate": overhead_rates,
        "revenue_factor": revenue_factors
    }

    sim = Simulator(simulation_period=5)
    all_results = sim.run_parameter_sweep(param_grid, business_model_factory)

    for combo_key, results_dict in all_results.items():
        print(f"Results for parameter combo: {combo_key}")
        print(results_dict)
        print("------")

if __name__ == "__main__":
    run_parameter_sweep_example()
