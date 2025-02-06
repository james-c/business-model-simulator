# cdip_initialization.py

from simulator.simulator import Simulator
from simulator.business_model import BusinessModel
from simulator.transaction_model import TransactionModel

# Import each operation subclass
from .operations.registration_operation import RegistrationOperation
from .operations.preference_setting_operation import PreferenceSettingOperation
from .operations.data_exploration_operation import DataExplorationOperation
from .operations.data_purchase_operation import DataPurchaseOperation
from .operations.profit_distribution_operation import ProfitDistributionOperation
from .operations.audit_operation import AuditOperation
from .operations.governance_operation import GovernanceOperation

import itertools

def create_cdip_operations():
    """
    Create and configure CDIP operations with real-world parameters
    based on the scenarios described in the paper.
    """
    reg_op = RegistrationOperation(
        name="Registration",
        parameters={
            # Represents administrative overhead for creating new accounts
            "administrative_cost": 2.0,
            "execution_cost": 1.0
        },
        contract_complexity="Low"
    )

    pref_op = PreferenceSettingOperation(
        name="PreferenceSetting",
        parameters={
            # Minimal cost; mostly storing preference data
            "execution_cost": 1.0
        },
        contract_complexity="Low"
    )

    exploration_op = DataExplorationOperation(
        name="DataExploration",
        parameters={
            # Searching datasets, includes data access cost + execution
            "data_access_cost": 3.0,
            "execution_cost": 2.0
        },
        contract_complexity="Medium"
    )

    purchase_op = DataPurchaseOperation(
        name="DataPurchase",
        parameters={
            # Licensing fees represent revenue from purchasing data
            "licensing_fees": 15.0,
            "execution_cost": 4.0,
            # Overhead for processing each purchase
            "purchase_overhead": 1.0
        },
        contract_complexity="Medium"
    )

    profit_dist_op = ProfitDistributionOperation(
        name="ProfitDistribution",
        parameters={
            # Execution cost + overhead for distributing funds
            "execution_cost": 2.0,
            "distribution_admin_cost": 0.5
        },
        contract_complexity="Medium"
    )

    audit_op = AuditOperation(
        name="Audit",
        parameters={
            "execution_cost": 3.0,
            "legal_cost": 4.0
        },
        contract_complexity="High"
    )

    governance_op = GovernanceOperation(
        name="Governance",
        parameters={
            "execution_cost": 2.5,
            # Represents cost for holding governance meetings, policy updates, etc.
            "governance_cost": 2.0
        },
        contract_complexity="High"
    )

    return [
        reg_op,
        pref_op,
        exploration_op,
        purchase_op,
        profit_dist_op,
        audit_op,
        governance_op
    ]


def init_cdip_simulation():
    """
    Creates a single-run simulation environment for the CDIP model
    with realistic parameters from the paper. Returns a configured Simulator.
    """
    cdip_ops = create_cdip_operations()

    # For example, 'overhead_rate' may represent an extra cost multiplier for all operations
    # 'revenue_tax_rate' might reflect a fee withheld from revenues
    tx_model = TransactionModel(
        operations=cdip_ops,
        parameters={
            "overhead_rate": 0.05,
            "revenue_tax_rate": 0.02
        }
    )

    # E.g., 'user_adoption_rate' to represent growth in new registrations over time
    cdip_bm = BusinessModel(
        name="CDIPBusinessModel",
        transaction_model=tx_model,
        parameters={
            "user_adoption_rate": 0.1,  # 10% adoption growth
            "blockchain_maintenance_cost": 500.0
        }
    )

    sim = Simulator(
        simulation_period=12,  # e.g., 12 time steps (months, quarters, etc.)
        global_parameters={
            # Any global param that might apply to all business models in a multi-model scenario
            "base_gas_price": 0.1
        }
    )

    sim.add_business_model(cdip_bm)
    return sim


def run_param_sweep():
    """
    Example function demonstrating a simple parameter sweep over user adoption rate
    and overhead rate. Creates multiple simulations, runs each, and collects results.
    """
    adoption_rates = [0.05, 0.1, 0.15]       # 5%, 10%, 15%
    overhead_rates = [0.03, 0.05, 0.08]     # 3%, 5%, 8%

    sweep_results = {}

    for (ar, oh) in itertools.product(adoption_rates, overhead_rates):
        # Create operations as usual
        cdip_ops = create_cdip_operations()

        # Adjust the TransactionModel to include the overhead_rate for this sweep
        tx_model = TransactionModel(
            operations=cdip_ops,
            parameters={
                "overhead_rate": oh,
                "revenue_tax_rate": 0.02
            }
        )

        # Create a business model with the user adoption rate set for this scenario
        cdip_bm = BusinessModel(
            name=f"CDIP_BM_AR={ar}_OH={oh}",
            transaction_model=tx_model,
            parameters={
                "user_adoption_rate": ar,
                "blockchain_maintenance_cost": 500.0
            }
        )

        # Initialize simulator with standard global params
        sim = Simulator(
            simulation_period=12,
            global_parameters={
                "base_gas_price": 0.1
            }
        )

        sim.add_business_model(cdip_bm)
        sim.run_simulation()
        results = sim.collect_results()

        # Store the results keyed by (adoption, overhead) combo
        combo_key = f"adoption={ar}_overhead={oh}"
        sweep_results[combo_key] = results

    # Print or store sweep_results in a file
    print("Parameter Sweep Results:")
    for combo, res in sweep_results.items():
        print(f"--- {combo} ---")
        print(res)
        print("")


if __name__ == "__main__":
    # Example single-run usage:
    single_sim = init_cdip_simulation()
    single_sim.run_simulation()
    single_results = single_sim.collect_results()
    print("Single-run Simulation Results:", single_results)

    # Example parameter sweep usage:
    run_param_sweep()
