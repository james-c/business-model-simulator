# business_model_simulator/tests/test_transaction_model.py

import pytest
from simulator.transaction_model import TransactionModel
from simulator.operation import Operation

def test_no_operations():
    """
    TransactionModel with no operations should return 0 cost and 0 revenue.
    """
    tx_model = TransactionModel()
    assert tx_model.calculate_costs() == 0.0
    assert tx_model.calculate_revenues() == 0.0

def test_single_operation_no_overhead_no_tax():
    """
    TransactionModel with one Operation, no overhead rate, and no revenue tax.
    """
    op = Operation(
        name="TestOp",
        parameters={
            "direct_cost": 2.0,
            "variable_cost": 1.0,
            "transaction_volume": 5.0,
            "base_revenue": 3.0,
            "revenue_per_unit": 2.0
        },
        contract_complexity=None  # No complexity multiplier
    )
    tx_model = TransactionModel(operations=[op], parameters={})

    assert tx_model.calculate_costs() == pytest.approx(2.0 + (1.0 * 5.0), 0.001) 
    # cost => 2 + 1*5 = 7
    assert tx_model.calculate_revenues() == pytest.approx(3.0 + (2.0 * 5.0), 0.001)
    # revenue => 3 + 2*5 = 13

@pytest.mark.parametrize(
    "overhead_rate, revenue_tax_rate, expected_cost, expected_revenue",
    [
        (0.1, 0.0,  # 10% overhead, no tax
         (2.0 + (1.0 * 5.0)) * 1.1,  # cost => 7 * 1.1 = 7.7
         13.0),                     # revenue => 13, no tax
        (0.0, 0.2,  # no overhead, 20% tax
         7.0,                         # cost => 7
         13.0 * (1.0 - 0.2)),         # revenue => 13 * 0.8 = 10.4
        (0.05, 0.1,  # 5% overhead, 10% tax
         (2.0 + 5.0) * 1.05,  # cost => 7 * 1.05 = 7.35
         13.0 * (1.0 - 0.1))  # revenue => 13 * 0.9 = 11.7
    ]
)
def test_single_operation_with_overhead_and_tax(overhead_rate, revenue_tax_rate, expected_cost, expected_revenue):
    """
    TransactionModel with one Operation, applying different overhead and tax rates.
    """
    op = Operation(
        name="TestOp",
        parameters={
            "direct_cost": 2.0,
            "variable_cost": 1.0,
            "transaction_volume": 5.0,
            "base_revenue": 3.0,
            "revenue_per_unit": 2.0
        },
        contract_complexity=None
    )
    tx_model = TransactionModel(
        operations=[op],
        parameters={"overhead_rate": overhead_rate, "revenue_tax_rate": revenue_tax_rate}
    )

    computed_cost = tx_model.calculate_costs()
    computed_revenue = tx_model.calculate_revenues()

    assert computed_cost == pytest.approx(expected_cost, 0.001), (
        f"Expected cost {expected_cost}, got {computed_cost}"
    )
    assert computed_revenue == pytest.approx(expected_revenue, 0.001), (
        f"Expected revenue {expected_revenue}, got {computed_revenue}"
    )

def test_multiple_operations():
    """
    TransactionModel with multiple Operation objects; costs and revenues should sum.
    """
    op1 = Operation(
        name="Op1",
        parameters={
            "direct_cost": 1.0,
            "variable_cost": 0.5,
            "transaction_volume": 4.0,
            "base_revenue": 2.0,
            "revenue_per_unit": 1.0
        }
    )
    op2 = Operation(
        name="Op2",
        parameters={
            "direct_cost": 2.0,
            "variable_cost": 0.2,
            "transaction_volume": 10.0,
            "base_revenue": 5.0,
            "revenue_per_unit": 0.5
        }
    )

    tx_model = TransactionModel(parameters={"overhead_rate": 0.1, "revenue_tax_rate": 0.1})
    tx_model.add_operation(op1)
    tx_model.add_operation(op2)

    # Calculate cost for each op, then apply overhead
    # op1 cost => 1.0 + (0.5 * 4) = 3.0
    # op2 cost => 2.0 + (0.2 * 10) = 4.0
    # sum = 7.0 -> with overhead_rate=0.1 => 7.0 * 1.1 = 7.7

    # Calculate revenue for each op, then apply 10% tax
    # op1 revenue => 2.0 + (1.0 * 4) = 6.0
    # op2 revenue => 5.0 + (0.5 * 10) = 10.0
    # sum = 16.0 -> with revenue_tax_rate=0.1 => 16.0 * 0.9 = 14.4

    assert tx_model.calculate_costs() == pytest.approx(7.7, 0.001)
    assert tx_model.calculate_revenues() == pytest.approx(14.4, 0.001)
