# business_model_simulator/simulator/transaction_model.py

from .operation import Operation

class TransactionModel:
    def __init__(self, operations=None, parameters=None):
        self.operations = operations if operations else []
        self.parameters = parameters if parameters else {}

    def update_for_time_step(self, step):
        growth_rate = self.parameters.get('growth_rate', 0.0)
        for op in self.operations:
            base_volume = op.parameters.get('base_transaction_volume', 1.0)
            new_volume = base_volume * ((1 + growth_rate) ** step)
            op.parameters['transaction_volume'] = new_volume

    def add_operation(self, operation):
        """
        Adds a new Operation to the list of operations in this transaction model.
        """
        self.operations.append(operation)

    def calculate_costs(self):
        total_cost = 0.0
        for op in self.operations:
            total_cost += op.compute_cost()

        overhead_rate = self.parameters.get('overhead_rate', 0.0)
        if overhead_rate > 0.0:
            total_cost *= (1.0 + overhead_rate)

        return total_cost

    def calculate_revenues(self):
        total_revenue = 0.0
        for op in self.operations:
            total_revenue += op.compute_revenue()

        # Apply an optional revenue factor sweep (e.g., 1.0, 1.1, etc.)
        revenue_factor = self.parameters.get('revenue_factor', 1.0)
        total_revenue *= revenue_factor

        revenue_tax_rate = self.parameters.get('revenue_tax_rate', 0.0)
        if revenue_tax_rate > 0.0:
            total_revenue *= (1.0 - revenue_tax_rate)

        return total_revenue
