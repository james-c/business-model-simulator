# data_exploration_operation.py

from simulator.operation import Operation

class DataExplorationOperation(Operation):
    """
    Enables data consumers to search available datasets.
    Parameters may include:
      - data_access_cost
      - execution_cost
      - contract_complexity (medium)
    """
    def compute_cost(self):
        base_cost = super().compute_cost()
        data_access_cost = self.parameters.get("data_access_cost", 0.0)
        return base_cost + data_access_cost

    def compute_revenue(self):
        return 0.0  # Exploration does not generate revenue
