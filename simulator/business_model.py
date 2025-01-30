# business_model_simulator/simulator/business_model.py

from .transaction_model import TransactionModel

class BusinessModel:
    """
    Encapsulates a specific business scenario or strategy, holding a reference
    to a TransactionModel and applying business model-specific parameters.
    """

    def __init__(self, name, transaction_model=None, parameters=None):
        """
        :param name: str, identifier for the business model
        :param transaction_model: TransactionModel instance
        :param parameters: dict, key-value pairs specific to this business model
            Example keys might include:
              - blockchain_type: str, e.g. 'public', 'private', 'hybrid'
              - cost_scaling_factor: float, modifies costs in certain scenarios
              - legal_compliance_fee: float, additional overhead for compliance
        """
        self.name = name
        self.transaction_model = transaction_model if transaction_model else TransactionModel()
        self.parameters = parameters if parameters else {}

    def adjust_parameters(self):
        """
        Adjusts the transaction model's parameters based on the
        business model's specifics. This example merges or overrides
        the transaction model parameters with any relevant data here.
        """
        # Example usage: apply a cost_scaling_factor if present in this business model
        if 'cost_scaling_factor' in self.parameters:
            original_overhead = self.transaction_model.parameters.get('overhead_rate', 0.0)
            scaled_overhead = original_overhead + self.parameters['cost_scaling_factor']
            self.transaction_model.parameters['overhead_rate'] = scaled_overhead

        # Example usage: if a legal_compliance_fee is defined, add it to overhead_rate as well
        if 'legal_compliance_fee' in self.parameters:
            overhead_rate = self.transaction_model.parameters.get('overhead_rate', 0.0)
            overhead_rate += self.parameters['legal_compliance_fee']
            self.transaction_model.parameters['overhead_rate'] = overhead_rate

        # Merging any remaining parameters that should be directly passed through
        for key, value in self.parameters.items():
            # Only update if not already handled above
            if key not in ('cost_scaling_factor', 'legal_compliance_fee'):
                self.transaction_model.parameters[key] = value
