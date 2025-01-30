# Example: Specialized Operation and Simple Simulation

This folder contains an example demonstrating how to extend the base `Operation` class in order to model a concrete business activity with customized cost and revenue calculations. It also shows how to assemble these components in a minimal simulation workflow.

---

## Contents

- **`example_operation.py`**  
  Defines `RegistrationOperation`, a subclass of `Operation` that overrides cost and revenue methods to include parameters such as a KYC fee.  

- **`example_simulation.py`** *(not yet provided)*  
  Illustrates how to create a `TransactionModel`, attach one or more `RegistrationOperation` instances, wrap them in a `BusinessModel`, and execute a simple simulation using the `Simulator`.

---

## Overview

The `RegistrationOperation` class includes a specialized cost model where:
- A base cost calculation is performed by calling the parent’s `compute_cost`.
- If the `contract_complexity` is `"High"`, an additional KYC fee is added to the total cost.
- The revenue is calculated as a flat fee, which is handled by the default logic inherited from `Operation` or configured through parameters.

This setup allows for scenario-based cost and revenue modeling. Additional subclasses can be created for other operations (for example, data purchases, audits, or profit distributions).

---

## Usage

1. **Review the `RegistrationOperation`**  
   The `RegistrationOperation` in `example_operation.py` can be extended with additional parameters or different logic as needed.

2. **Integrate into a Transaction Model**  
   In a transaction model (for example, `TransactionModel` in `transaction_model.py`), the `operations` list can include an instance of `RegistrationOperation`, for example:
   ```python
   from example_operation import RegistrationOperation
   from simulator.transaction_model import TransactionModel

   ops = [
       RegistrationOperation(
           name="UserRegistration",
           parameters={
               "direct_cost": 2.0,
               "variable_cost": 1.0,
               "transaction_volume": 50,
               "kyc_fee": 10.0,
               "base_revenue": 5.0,
               "revenue_per_unit": 1.0
           },
           contract_complexity="High"
       )
   ]

   tx_model = TransactionModel(operations=ops)
   ```
   
3.	**Attach to a Business Model**
A BusinessModel can reference the above transaction model:

   ```python
from simulator.business_model import BusinessModel

business_model = BusinessModel(
    name="RegistrationBusiness",
    transaction_model=tx_model,
    parameters={"some_model_param": 123}
)
```

4.	Run a Simulation
The Simulator can run the scenario for a set period:

```python
from simulator.simulator import Simulator

sim = Simulator(simulation_period=12)
sim.add_business_model(business_model)
sim.run_simulation()
results = sim.collect_results()
print(results)
```

5.	**Extend as Needed**
The same pattern can be applied to create additional specialized operations or more advanced business model logic.

Notes
- This example is designed as a starting point. It can be expanded with more complex financial logic, multiple operations, or additional time-step behaviors.
- Parameter dictionaries are flexible, allowing parameters to be added or removed without modifying the base classes.
- The example_simulation.py script can demonstrate a fully working simulation, including output storage or visualization steps.

