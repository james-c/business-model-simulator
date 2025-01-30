# business_model_simulator/simulator/simulator.py

from .business_model import BusinessModel
import itertools

class Simulator:
    """
    Main controller for running simulations and collecting results.
    Now includes a run_parameter_sweep method for multi-run scenarios.
    """

    def __init__(self, simulation_period, global_parameters=None):
        """
        :param simulation_period: int, total number of discrete time steps for the simulation
        :param global_parameters: dict, global parameters that may affect all business models
        """
        self.simulation_period = simulation_period
        self.global_parameters = global_parameters if global_parameters else {}
        self.business_models = []
        self.results = {}

    def add_business_model(self, business_model):
        """
        Registers a new BusinessModel to be included in the simulation.
        """
        self.business_models.append(business_model)

    def run_simulation(self):
        """
        Runs the simulation for each registered BusinessModel over the specified
        simulation_period. Results are stored in self.results.
        """
        for model in self.business_models:
            # Merge global parameters
            model.transaction_model.parameters.update(self.global_parameters)
            model.adjust_parameters()

            model_results = []
            for step in range(self.simulation_period):
                if hasattr(model.transaction_model, 'update_for_time_step'):
                    model.transaction_model.update_for_time_step(step)

                total_costs = model.transaction_model.calculate_costs()
                total_revenues = model.transaction_model.calculate_revenues()

                model_results.append({
                    "step": step,
                    "costs": total_costs,
                    "revenues": total_revenues
                })

            self.results[model.name] = model_results

    def collect_results(self):
        """
        Returns the recorded results from the simulation runs.
        """
        return self.results

    def run_parameter_sweep(self, param_grid, business_model_factory):
        """
        Iterates over all parameter combinations in param_grid, creates a fresh
        BusinessModel for each combination using business_model_factory, and runs
        a simulation. Returns a dictionary of all sweep results.

        :param param_grid: dict, e.g. {"growth_rate": [0.0, 0.05], "overhead_rate": [0.0, 0.03]}
        :param business_model_factory: callable that accepts a dict of parameter values
                                       and returns a new BusinessModel instance
        :return: dict of results, keyed by a name that includes each parameter combination
        """

        sweep_results = {}
        # Create a list of parameter names and a list of value-lists
        param_names = list(param_grid.keys())
        param_value_lists = [param_grid[name] for name in param_names]

        # Use itertools.product to get every combination of parameter values
        for combo in itertools.product(*param_value_lists):
            # Construct a dict of parameter_name -> chosen_value
            combo_params = dict(zip(param_names, combo))

            # Create a new Simulator instance for this combination
            # so that each run starts fresh
            sim = Simulator(simulation_period=self.simulation_period,
                            global_parameters=self.global_parameters)

            # Use the factory to create a business model for this combo
            bm = business_model_factory(combo_params)
            sim.add_business_model(bm)

            # Run simulation
            sim.run_simulation()
            run_results = sim.collect_results()

            # Generate a key that describes the combination, e.g. "GR=0.05_OH=0.03"
            combo_key_parts = [f"{k}={v}" for k, v in combo_params.items()]
            combo_key = "_".join(combo_key_parts)

            # Store the results in the sweep_results dict
            sweep_results[combo_key] = run_results

        return sweep_results
