# Schelling's Segregation Model

## 1. Overview & Objective
This model implements Thomas Schelling's classic 1971 Agent-Based Model of segregation. 
The objective of this simulation is to explore **emergent behavior**: how mild, individual preferences for similar neighbors (micro-motives) unintentionally lead to stark, macroscopic segregation across an entire neighborhood (macro-behavior).

## 2. Core Concepts & Rules
- **Agents:** Residents belonging to one of two distinct groups (`Group 0 / Red` and `Group 1 / Blue`).
- **Space:** A $20 \times 20$ toroidal `SingleGrid` (where each grid cell can house at most one resident, leaving some cells empty for relocation).
- **Decision Rule (`step()`):**
  1. Each agent inspects its 8 Moore neighbors.
  2. The agent calculates the fraction of neighbors belonging to its own group.
  3. If this fraction falls below a threshold (`homophily`, default 30%), the agent becomes **unhappy** and relocates to a random empty cell (`move_to_empty`).
  4. If the fraction meets or exceeds the threshold, the agent remains happy.
- **Termination:** The simulation halts when 100% of the agents are happy (an equilibrium state where no one moves).

## 3. Key Observations & Emergence
- **The Tolerance Paradox:** Even when agents are remarkably tolerant (happy with only 30% similar neighbors and comfortable with 70% different neighbors), the system naturally segregates into polarized Red and Blue clusters.
- **Cascading Relocations:** When an unhappy agent relocates to an empty spot, their arrival alters the neighbor ratio of surrounding agents, sometimes causing previously satisfied neighbors to become unhappy.
- **Convergence:** Under default parameters (density = 0.8, homophily = 0.3), the model converges to 100% happiness within 8–15 steps.

## 4. Engineering Learnings & Friction Points
- **Set Mutation during Iteration (`RuntimeError`):**  
  Initially iterating directly over `self.grid.empties` resulted in `RuntimeError: Set changed size during iteration`. Because placing an agent removes the cell from the internal empty set, wrapping `self.grid.empties` into a static snapshot `list(self.grid.empties)` resolved the issue.
- **Modern Mesa 3.0+ Idioms:**  
  Migrated from legacy scheduler patterns to `self.agents.shuffle_do("step")` and adopted `super().__init__(rng=seed)` instead of the deprecated `seed` keyword.
- **Interactive UI with Solara:**  
  Integrated `SolaraViz` with `make_space_component` and `make_plot_component` for real-time visualization and parameter experimentation.

## 5. How to Run
```bash
# Command line simulation
python run.py

# Interactive Web UI (Localhost)
solara run app.py
```