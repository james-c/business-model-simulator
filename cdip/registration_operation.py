# registration_operation.py

from simulator.operation import Operation

class RegistrationOperation(Operation):
    """
    Represents the process of onboarding new users to the CDIP platform.
    Parameters may include:
      - administrative_cost
      - execution_cost
      - contract_complexity (low)
    """
    def compute_cost(self):
        base_cost = super().compute_cost()
        admin_cost = self.parameters.get("administrative_cost", 0.0)
        return base_cost + admin_cost

    def compute_revenue(self):
        return 0.0  # No revenue from user registration
