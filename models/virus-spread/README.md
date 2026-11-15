# Epidemic Outbreak (SIR Model)

## 1. Overview & Objective
This model implements the classic **SIR (Susceptible-Infectious-Recovered)** epidemiology model proposed by Kermack & McKendrick (1927), adapted to an Agent-Based spatial environment.

The objective is to observe how localized interactions between roaming agents cause an infection to spread exponentially, hit an epidemic peak, and eventually burn out as herd immunity develops.

## 2. Core Concepts & State Machine
Each agent is an autonomous individual belonging to one of three states (`Enum`):
- **Susceptible (🟢):** Healthy individuals who are vulnerable to infection.
- **Infected (🔴):** Actively infected individuals capable of transmitting the pathogen.
- **Recovered (🔵):** Individuals who survived the infection and now possess lifelong immunity.

### Agent Lifecycle & Rules (`step()`):
1. **Mobility:** Agents wander randomly across a toroidal `MultiGrid` (8-way Moore neighborhood).
2. **Transmission:** Whenever an Infected agent shares a grid cell with Susceptible agents, each susceptible agent has an independent probability (`infection_rate`, default 30%) of becoming infected.
3. **Recovery:** Infected agents increment an internal counter (`infection_time`). Once `infection_time >= recovery_days` (default 10 steps), they transition to **Recovered**.
4. **Termination:** The simulation concludes when active infections hit zero (`Infected == 0`).

## 3. Key Observations & Emergent Behavior
- **The Epidemic Peak:** In the beginning, infections surge exponentially because susceptible individuals are abundant. 
- **Herd Immunity:** As recovered (immune) agents populate the grid, they act as buffers, effectively shielding remaining susceptible agents from encountering infected ones.
- **Flattening the Curve:** Lowering the transmission rate (simulating masks/social distancing) delays and flattens the infection peak, keeping the system stable.

## 4. Engineering Learnings & Mesa Features Used
- **`MultiGrid` Architecture:** Unlike the Schelling model (where each house was exclusive via `SingleGrid`), an epidemic requires physical co-location in public spaces. `MultiGrid` allows multiple agents to inhabit the same cell and interact via `get_cell_list_contents`.
- **State Machine Integration:** Managed discrete state transitions using Python's `enum.Enum` for type-safe and readable agent states.
- **Multi-Series DataCollection:** Utilized `DataCollector` with multiple simultaneous reporters to generate concurrent S, I, and R time-series plots.
- **Polished Solara Visualizations:** Customized `agent_portrayal` and `post_process` hooks to maintain clean layout formatting and responsive sliders.

## 5. How to Run
```bash
# Headless terminal simulation
python run.py

# Interactive Web Dashboard
solara run app.py
```