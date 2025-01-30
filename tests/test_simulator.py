# business_model_simulator/tests/test_simulator.py

import pytest
from simulator.simulator import Simulator
from simulator.business_model import BusinessModel
from simulator.transaction_model import TransactionModel
from simulator.operation import Operation

def test_no_business_models():
    """
    Simulator with no business models should produce an empty results dict.
    """
    sim = Simulator(simulation_period=5)
    sim.run_simulation()
    results = sim.collect_results()
    assert results == {}, "Expected empty results for no business models"

def test_single_business_model_basic():
    """
    Simulator with a single BusinessModel should produce a results entry 
    matching the model's name.
    """
    # Create an Operation
    op = Operation(
        name="BasicOp",
        parameters={
            "direct_cost": 1.0,
            "variable_cost": 0.5,
            "transaction_volume": 4.0,
            "base_revenue": 2.0,
            "revenue_per_unit": 1.0
        }
    )
    # Create a TransactionModel
    tx_model = TransactionModel(operations=[op], parameters={})
    # Create a BusinessModel
    bm = BusinessModel(name="SingleBM", transaction_model=tx_model, parameters={})
    
    # Run simulation
    sim = Simulator(simulation_period=3)
    sim.add_business_model(bm)
    sim.run_simulation()
    results = sim.collect_results()
    
    # Check we have a results entry with the key 'SingleBM'
    assert "SingleBM" in results, "Expected results entry for 'SingleBM'"
    model_steps = results["SingleBM"]
    
    # We expect one record per time step
    assert len(model_steps) == 3, "Expected 3 steps of results"
    for step_result in model_steps:
        # Each step result should have 'costs' and 'revenues'
        assert "costs" in step_result and "revenues" in step_result, (
            "Each result record should include 'costs' and 'revenues' keys"
        )

def test_multiple_business_models():
    """
    Simulator handling multiple BusinessModels should return multiple result sets.
    """
    # Create two simple business models
    bm1 = BusinessModel(
        name="BM1",
        transaction_model=TransactionModel(
            operations=[Operation("Op1")],
            parameters={}
        )
    )
    bm2 = BusinessModel(
        name="BM2",
        transaction_model=TransactionModel(
            operations=[Operation("Op2")],
            parameters={}
        )
    )

    sim = Simulator(simulation_period=2)
    sim.add_business_model(bm1)
    sim.add_business_model(bm2)
    sim.run_simulation()
    results = sim.collect_results()

    # Check both models exist in results
    assert "BM1" in results, "Results should contain BM1"
    assert "BM2" in results, "Results should contain BM2"
    assert len(results["BM1"]) == 2, "Should have 2 steps for BM1"
    assert len(results["BM2"]) == 2, "Should have 2 steps for BM2"

def test_global_parameters_merge():
    """
    Ensures that simulator merges global parameters into each BusinessModel's 
    transaction model before running.
    """
    # Operation that uses variable_cost
    op = Operation(
        name="GlobalParamOp",
        parameters={
            "direct_cost": 2.0,
            "variable_cost": 1.0,
            "transaction_volume": 2.0
        }
    )
    tx_model = TransactionModel(operations=[op], parameters={})
    bm = BusinessModel(name="GlobalParamModel", transaction_model=tx_model, parameters={})
    
    # Provide a global overhead_rate
    sim = Simulator(simulation_period=1, global_parameters={"overhead_rate": 0.5})
    sim.add_business_model(bm)
    sim.run_simulation()
    results = sim.collect_results()
    
    # Overhead rate should now be in the transaction model’s parameters
    overhead_rate = tx_model.parameters.get("overhead_rate")
    assert overhead_rate == 0.5, f"Expected overhead_rate=0.5, got {overhead_rate}"
    
    # Check that we have a single time step in the results
    model_data = results["GlobalParamModel"]
    assert len(model_data) == 1, "Expected 1 time step of results"
    assert "costs" in model_data[0] and "revenues" in model_data[0], (
        "Each step record should have 'costs' and 'revenues'"
    )
