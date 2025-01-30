# business_model_simulator/tests/test_business_model.py

import pytest
from simulator.business_model import BusinessModel
from simulator.transaction_model import TransactionModel

def test_no_adjustment():
    """
    A BusinessModel with empty parameters should not change
    the TransactionModel's overhead_rate.
    """
    tm = TransactionModel(parameters={"overhead_rate": 0.05})
    bm = BusinessModel(name="NoAdjustment", transaction_model=tm, parameters={})
    bm.adjust_parameters()

    assert tm.parameters["overhead_rate"] == 0.05, (
        "No parameters in BusinessModel should leave overhead_rate unchanged"
    )

def test_cost_scaling_factor():
    """
    A BusinessModel with a 'cost_scaling_factor' should increase
    the TransactionModel's 'overhead_rate' by that factor.
    """
    tm = TransactionModel(parameters={"overhead_rate": 0.05})
    bm = BusinessModel(
        name="CostScale",
        transaction_model=tm,
        parameters={"cost_scaling_factor": 0.1}
    )

    bm.adjust_parameters()
    # Original overhead_rate=0.05 -> plus 0.1 => 0.15
    expected = 0.15
    actual = tm.parameters["overhead_rate"]
    assert actual == pytest.approx(expected, 0.001), (
        f"Expected overhead_rate to be {expected}, got {actual}"
    )

def test_legal_compliance_fee():
    """
    A BusinessModel with a 'legal_compliance_fee' should add that
    fee to the TransactionModel's 'overhead_rate'.
    """
    tm = TransactionModel(parameters={"overhead_rate": 0.05})
    bm = BusinessModel(
        name="ComplianceFee",
        transaction_model=tm,
        parameters={"legal_compliance_fee": 0.02}
    )

    bm.adjust_parameters()
    # Original overhead_rate=0.05 -> plus 0.02 => 0.07
    expected = 0.07
    actual = tm.parameters["overhead_rate"]
    assert actual == pytest.approx(expected, 0.001), (
        f"Expected overhead_rate to be {expected}, got {actual}"
    )

def test_combined_adjustments():
    """
    A BusinessModel with both a 'cost_scaling_factor' and a
    'legal_compliance_fee' should cumulatively add to overhead_rate.
    Also checks passing extra params that should merge into the transaction model.
    """
    tm = TransactionModel(parameters={
        "overhead_rate": 0.05,
        "some_existing_param": 100
    })
    bm = BusinessModel(
        name="CombinedAdjust",
        transaction_model=tm,
        parameters={
            "cost_scaling_factor": 0.05,
            "legal_compliance_fee": 0.03,
            "new_param": 999  # Should merge into tm.parameters as well
        }
    )

    bm.adjust_parameters()
    # Original overhead_rate=0.05
    # + cost_scaling_factor=0.05 => 0.10
    # + legal_compliance_fee=0.03 => 0.13
    expected_overhead = 0.13
    actual_overhead = tm.parameters["overhead_rate"]
    assert actual_overhead == pytest.approx(expected_overhead, 0.001), (
        f"Expected overhead_rate to be {expected_overhead}, got {actual_overhead}"
    )

    # new_param should now exist in tm.parameters
    assert tm.parameters.get("new_param") == 999, (
        "new_param should be merged into transaction_model.parameters"
    )
