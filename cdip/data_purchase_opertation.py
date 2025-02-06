# data_purchase_operation.py

from simulator.operation import Operation

class DataPurchaseOperation(Operation):
    """
    Manages transactions where data consumers purchase access to datasets.
    Parameters may include:
      - licensing_fees
      - execution_cost
      - contract_complexity (medium)
    """
    def compute_cost(self):
        base_cost = super().compute_cost()
        # If there's any extra overhead per purchase:
        overhead_fee = self.parameters.get("purchase_overhead", 0.0)
        return base_cost + overhead_fee

    def compute_revenue(self):
        # Possibly combine base revenue + licensing fees
        base_rev = super().compute_revenue()
        licensing_fees = self.parameters.get("licensing_fees", 0.0)
        return base_rev + licensing_fees
