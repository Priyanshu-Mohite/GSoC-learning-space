# models/virus_spread/model.py

from enum import Enum
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


# 1. Teen states define ki: S, I, R
class State(Enum):
    SUSCEPTIBLE = 0  # 🟢 Healthy
    INFECTED = 1     # 🔴 Bimar
    RECOVERED = 2    # 🔵 Immune


class VirusAgent(Agent):
    """
    Sheher ka ek nagrik jo ghoomta hai aur bimar ho sakta hai.
    """
    def __init__(self, model, initial_state=State.SUSCEPTIBLE):
        super().__init__(model)
        self.state = initial_state
        self.infection_time = 0  # Kitne din se bimar hai

    def move(self):
        # Aas-paas kisi bhi padosi cell me kadam badhao
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def infect_others(self):
        # 1. Dekho mere cell (jagah) par kaun khada hai
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other in cellmates:
            # Agar samne wala Healthy hai, toh infection ka chance calculate karo
            if other.state == State.SUSCEPTIBLE:
                if self.random.random() < self.model.infection_rate:
                    other.state = State.INFECTED

    def step(self):
        # 1. Pehle move karo
        self.move()

        # 2. Agar mai bimar hoon:
        if self.state == State.INFECTED:
            # Aas-paas ke logon ko bimar karo
            self.infect_others()
            
            # Din count karo
            self.infection_time += 1
            
            # Agar 10 din pure ho gaye, toh theek ho jao!
            if self.infection_time >= self.model.recovery_days:
                self.state = State.RECOVERED


class VirusModel(Model):
    """
    Pura sheher jahan virus failta hai.
    """
    def __init__(self, n_agents=100, width=15, height=15, 
                 initial_infected=3, infection_rate=0.3, recovery_days=10, seed=None):
        super().__init__(rng=seed)

        self.infection_rate = infection_rate
        self.recovery_days = recovery_days

        # MultiGrid: Ek cell me ek se zyada log aa sakte hain
        self.grid = MultiGrid(width, height, torus=True)

        # Munshi: Teenon groups ka alag-alag count note karega
        self.datacollector = DataCollector(
            model_reporters={
                "Susceptible": lambda m: sum(1 for a in m.agents if a.state == State.SUSCEPTIBLE),
                "Infected": lambda m: sum(1 for a in m.agents if a.state == State.INFECTED),
                "Recovered": lambda m: sum(1 for a in m.agents if a.state == State.RECOVERED),
            }
        )

        # 1. Saare agents banao
        for i in range(n_agents):
            # Pehle 'initial_infected' log bimar honge, baaki healthy
            state = State.INFECTED if i < initial_infected else State.SUSCEPTIBLE
            agent = VirusAgent(self, initial_state=state)

            # Random jagah par place karo
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # Shuruat ka data note karo
        self.datacollector.collect(self)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

        # Agar sheher me 0 bimar bache, toh simulation rok do!
        infected_count = sum(1 for a in self.agents if a.state == State.INFECTED)
        if infected_count == 0:
            self.running = False