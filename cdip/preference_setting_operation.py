# preference_setting_operation.py

from simulator.operation import Operation

class PreferenceSettingOperation(Operation):
    """
    Represents user preference setting for data sharing.
    Parameters may include:
      - execution_cost
      - contract_complexity (low)
    """
    def compute_cost(self):
        base_cost = super().compute_cost()
        return base_cost

    def compute_revenue(self):
        return 0.0  # No revenue from setting preferences
