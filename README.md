# Business Model Simulator

A Python-based simulation framework for modeling blockchain-related business strategies. This repository supports parameterized operations, cost/revenue calculations, and advanced scenario analysis (including time-based or parameter-sweep simulations).

---

## Contents

- **simulator/**  
  Contains the core classes:
  - `simulator.py`: Main `Simulator` class for orchestrating simulations.
  - `business_model.py`: `BusinessModel` class for specifying model-specific parameters and references to the transaction model.
  - `transaction_model.py`: `TransactionModel` class for managing operations and computing aggregate costs/revenues.
  - `operation.py`: `Operation` class defining individual business activities with cost/revenue logic.

- **scripts/**  
  Includes runnable scripts:
  - `run_simulation.py`: Demonstrates how to perform parameter sweeps or single-run simulations, saving outputs to CSV.
  - `analyze_results.py`: Shows basic methods for processing or visualizing simulation outputs.

- **tests/**  
  Holds unit tests for all core classes:
  - `test_simulator.py`: Tests for the `Simulator` class.
  - `test_business_model.py`: Tests for the `BusinessModel` class.
  - `test_transaction_model.py`: Tests for the `TransactionModel` class.
  - `test_operation.py`: Tests for the `Operation` class.

- **data/**  
  - `input/`: Optional directory for external input/configuration files.
  - `output/`: Default location for generated simulation results (e.g., CSV files).

- Other project files (e.g., `.gitignore`, `requirements.txt`, `setup.py`, `pyproject.toml`) manage dependencies, version control, and Python packaging configuration.

---

## Key Features

- **Modular Design**: Classes for operations, transaction models, business models, and the simulator are loosely coupled, making it easier to adapt or extend to new scenarios.  
- **Parameter Sweeping**: Built-in examples to explore multiple parameter combinations (e.g., transaction volume growth, overhead rates, revenue factors).  
- **Time-Based Updates**: Mechanisms (such as `update_for_time_step`) can be implemented to support dynamic changes in cost and revenue parameters over multiple time steps.  
- **Results Analysis**: Scripts for output aggregation and basic statistical computations on the resulting data.  

---

## Getting Started

1. **Clone or Download** the repository to a local environment.  
2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Review Scripts**  
   - **`scripts/run_simulation.py`**: Demonstrates single-run or parameter-sweep simulations.  
   - **`scripts/analyze_results.py`**: Provides a basic approach to reading and analyzing CSV output.

5. **Run Tests**  
    ```bash
	pytest
	```

---

## Usage Example

1. **Define Operations**  
   Create `Operation` or subclass objects with relevant parameters for costs, revenues, and optional contract complexity.

2. **Build a Transaction Model**  
   Add the operations into a `TransactionModel` and set global parameters (e.g., overhead or tax rates).

3. **Create a Business Model**  
   Wrap the `TransactionModel` in a `BusinessModel`, optionally modifying parameters based on a specific scenario (e.g., private vs. public chain).

4. **Simulate**  
   Use the `Simulator` to run over multiple time steps, optionally applying time-dependent updates or sweeping multiple parameters.

5. **Analyze Results**  
   Export results to a file (e.g., CSV), then process or visualize them using any of the provided scripts.

---

## Further Customization

- **Subclasses**: Extend `Operation` to implement specialized cost or revenue formulas.  
- **Time-Dependent Logic**: Employ methods such as `update_for_time_step` in `TransactionModel` or `Operation` to adjust parameters dynamically.  
- **Advanced Analysis**: Utilize libraries like Pandas or Matplotlib for additional reporting, plotting, or statistical operations in the analysis script.

---

## License

MIT License 

Copyright (c) 2025 University of Manchester 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
---

## Contact

	please contact james.a.cunningham@manchester.ac.uk for any comments or queries 
