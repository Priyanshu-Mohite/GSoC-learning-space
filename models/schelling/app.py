# models/schelling/app.py

import solara
from mesa.visualization import (
    SolaraViz,
    Slider,
    make_space_component,
    make_plot_component,
)
from model import SchellingModel


# 1. Agents ka look: Bigger dots (size=85) taaki grid clean bhari hui dikhe
def agent_portrayal(agent):
    return {
        "color": "#1f77b4" if agent.type == 1 else "#d62728",  # Clean Blue & Red
        "size": 85,
    }


# 2. Grid ko saaf karna: Faltu ke decimal numbers aur ticks hatana
def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])  # Saare gande x-axis numbers gayab
    ax.set_yticks([])  # Saare gande y-axis numbers gayab
    ax.set_title("Neighborhood Grid", fontsize=12, fontweight="bold", pad=10)


# 3. Graph ko clean karna: Proper 0% to 100% axis aur gridlines
def post_process_plot(ax):
    ax.set_title("Happiness Trend", fontsize=12, fontweight="bold", pad=10)
    ax.set_xlabel("Simulation Steps", fontsize=10)
    ax.set_ylabel("% Happy", fontsize=10)
    ax.set_ylim(0, 105)
    ax.grid(True, linestyle="--", alpha=0.5)


# 4. Sliders: Short aur clean labels jo sidebar me na katein
model_params = {
    "width": 20,
    "height": 20,
    "density": Slider("Density", 0.8, 0.1, 0.95, 0.05),
    "homophily": Slider("Homophily (Tolerance)", 0.3, 0.0, 1.0, 0.05),
}

# 5. Model create karo
initial_model = SchellingModel(width=20, height=20, density=0.8, homophily=0.3)

# 6. Components with clean styling
SpaceComponent = make_space_component(agent_portrayal, post_process=post_process_space)
HappyPlot = make_plot_component({"percent_happy": "tab:green"}, post_process=post_process_plot)

# 7. Final Clean Page
page = SolaraViz(
    initial_model,
    components=[SpaceComponent, HappyPlot],
    model_params=model_params,
    name="Schelling's Segregation Model",
)