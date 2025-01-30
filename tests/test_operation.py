# business_model_simulator/tests/test_operation.py

import pytest
from simulator.operation import Operation

@pytest.mark.parametrize(
    "parameters,contract_complexity,expected_cost,expected_revenue",
    [
        # No complexity, minimal cost/revenue
        (
            {"direct_cost": 2.0, "variable_cost": 1.0, "transaction_volume": 5.0, 
             "base_revenue": 5.0, "revenue_per_unit": 2.0},
            None, 
            2.0 + (1.0 * 5.0),   # no multiplier => 2 + 5 = 7
            5.0 + (2.0 * 5.0),   # 5 + 10 = 15
        ),

        # Medium complexity with default multiplier 1.5
        (
            {"direct_cost": 3.0, "variable_cost": 2.0, "transaction_volume": 2.0,
             "base_revenue": 10.0, "revenue_per_unit": 1.0},
            "Medium", 
            (3.0 + (2.0 * 2.0)) * 1.5,   # (3 + 4) * 1.5 = 7 * 1.5 = 10.5
            10.0 + (1.0 * 2.0),          # 10 + 2 = 12
        ),

        # High complexity with default multiplier 2.0
        (
            {"direct_cost": 4.0, "variable_cost": 1.0, "transaction_volume": 10,
             "base_revenue": 0.0, "revenue_per_unit": 1.0},
            "High",
            (4.0 + (1.0 * 10)) * 2.0,  # (4 + 10) * 2 = 14 * 2 = 28
            0.0 + (1.0 * 10),         # 10
        ),
    ]
)
def test_operation_cost_revenue(parameters, contract_complexity, expected_cost, expected_revenue):
    """
    Tests the compute_cost() and compute_revenue() methods of Operation
    under different parameter and contract complexity scenarios.
    """
    op = Operation(
        name="TestOperation",
        parameters=parameters,
        contract_complexity=contract_complexity
    )

    computed_cost = op.compute_cost()
    computed_revenue = op.compute_revenue()

    assert computed_cost == pytest.approx(expected_cost, 0.001), (
        f"Expected cost {expected_cost}, but got {computed_cost}"
    )
    assert computed_revenue == pytest.approx(expected_revenue, 0.001), (
        f"Expected revenue {expected_revenue}, but got {computed_revenue}"
    )


def test_operation_default_values():
    """
    Tests that an Operation with no parameters or complexity
    returns zero cost and zero revenue by default.
    """
    op = Operation(name="NoParamsOperation")
    assert op.compute_cost() == 0.0
    assert op.compute_revenue() == 0.0
