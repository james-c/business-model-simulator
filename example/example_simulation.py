from simulator.simulator import Simulator
from simulator.business_model import BusinessModel
from simulator.transaction_model import TransactionModel
from example.example_operation import RegistrationOperation

def run_time_dependent_example():
    reg_operation = RegistrationOperation(
        name="UserRegistration",
        parameters={
            "base_transaction_volume": 50,  # used for growth
            "direct_cost": 2.0,
            "variable_cost": 1.0,
            "kyc_fee": 10.0,
            "base_revenue": 5.0,
            "revenue_per_unit": 1.0
        },
        contract_complexity="High"
    )

    tx_model = TransactionModel(
        operations=[reg_operation],
        parameters={
            "growth_rate": 0.1,         # 10% growth in volume each time step
            "overhead_rate": 0.05,
            "revenue_tax_rate": 0.02
        }
    )

    bm = BusinessModel(
        name="GrowingRegistrationBusiness",
        transaction_model=tx_model,
        parameters={}
    )

    sim = Simulator(simulation_period=5)
    sim.add_business_model(bm)
    sim.run_simulation()

    results = sim.collect_results()
    print("Results with time-dependent transaction volumes:", results)

if __name__ == "__main__":
    run_time_dependent_example()
