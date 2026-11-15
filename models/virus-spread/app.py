# models/virus_spread/app.py

import solara
from mesa.visualization import (
    SolaraViz,
    Slider,
    make_space_component,
    make_plot_component,
)
from model import VirusModel, State


# 1. Teen rang ke agents (Green, Red, Blue)
def agent_portrayal(agent):
    color_map = {
        State.SUSCEPTIBLE: "#2ca02c",  # Green (Healthy)
        State.INFECTED: "#d62728",     # Red (Bimar)
        State.RECOVERED: "#1f77b4",    # Blue (Immune)
    }
    return {
        "color": color_map[agent.state],
        "size": 75,
    }


# 2. Grid ko clean aur square banana
def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("City Grid (Spread of Infection)", fontsize=12, fontweight="bold", pad=10)


# 3. Triple-Line Graph ko clean karna
def post_process_plot(ax):
    ax.set_title("Epidemic Curve (SIR Dynamics)", fontsize=12, fontweight="bold", pad=10)
    ax.set_xlabel("Days (Steps)", fontsize=10)
    ax.set_ylabel("Number of Citizens", fontsize=10)
    ax.set_ylim(0, 110)
    ax.legend(loc="upper right", framealpha=0.8)
    ax.grid(True, linestyle="--", alpha=0.5)


# 4. Clean Sliders jo sidebar me fit honge
model_params = {
    "width": 15,
    "height": 15,
    "n_agents": Slider("Population", 100, 20, 200, 10),
    "initial_infected": Slider("Initial Infected", 3, 1, 10, 1),
    "infection_rate": Slider("Transmission Rate", 0.3, 0.05, 1.0, 0.05),
    "recovery_days": Slider("Recovery Duration (Days)", 10, 3, 25, 1),
}

# 5. Model create karo
initial_model = VirusModel(n_agents=100, width=15, height=15, 
                           initial_infected=3, infection_rate=0.3, recovery_days=10)

# 6. Components attach karo
SpaceComponent = make_space_component(agent_portrayal, post_process=post_process_space)
EpidemicPlot = make_plot_component(
    {
        "Susceptible": "#2ca02c",  # Green Line
        "Infected": "#d62728",     # Red Line
        "Recovered": "#1f77b4",    # Blue Line
    },
    post_process=post_process_plot,
)

# 7. Solara Viz Page
page = SolaraViz(
    initial_model,
    components=[SpaceComponent, EpidemicPlot],
    model_params=model_params,
    name="Epidemic Outbreak (SIR Model)",
)