# models/schelling/model.py

from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


class SchellingAgent(Agent):
    """
    Ek resident jo ya toh Red (0) hai ya Blue (1).
    """
    def __init__(self, model, agent_type):
        super().__init__(model)
        self.type = agent_type  # 0 = Red, 1 = Blue

    def step(self):
        # 1. Apne padosi dhundo (Moore = 8 directions)
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True)

        # 2. Agar koi padosi hi nahi hai, toh chupchaap raho
        if len(neighbors) == 0:
            return

        # 3. Count karo: Mere jaise kitne log hain?
        similar_neighbors = sum(1 for neighbor in neighbors if neighbor.type == self.type)

        # 4. Ratio calculate karo
        similarity_ratio = similar_neighbors / len(neighbors)

        # 5. Agar similarity mere threshold se kam hai, toh shift ho jao
        if similarity_ratio < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy_agents += 1


class SchellingModel(Model):
    """
    Colony / Grid jahan log rehte hain.
    """
    def __init__(self, width=20, height=20, density=0.8, homophily=0.3, seed=None):
        # Modern Mesa me seed ko rng ke through pass karte hain
        super().__init__(rng=seed)

        self.width = width
        self.height = height
        self.density = density        # Kitne percent ghar bhare honge
        self.homophily = homophily    # Kitni % similarity chahiye
        self.happy_agents = 0

        # Grid setup
        self.grid = SingleGrid(width, height, torus=True)

        # Munshi (DataCollector)
        self.datacollector = DataCollector(
            model_reporters={
                "happy_agents": lambda m: m.happy_agents,
                "percent_happy": lambda m: (m.happy_agents / len(m.agents)) * 100 if len(m.agents) > 0 else 0
            }
        )

        # FIX: list(...) use kiya taaki iteration ke time size change error na aaye
        for cell in list(self.grid.empties):
            if self.random.random() < self.density:
                agent_type = 0 if self.random.random() < 0.5 else 1
                agent = SchellingAgent(self, agent_type)
                self.grid.place_agent(agent, cell)

    def step(self):
        self.happy_agents = 0

        # Sabhi agents ko unka step() chalane ko bolo
        self.agents.shuffle_do("step")

        # Data collect karo
        self.datacollector.collect(self)

        # Agar sab khush ho gaye toh simulation stop kar do
        if self.happy_agents == len(self.agents):
            self.running = False