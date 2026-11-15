# models/virus_spread/run.py

from model import VirusModel

# 100 log, 3 bimar se shuruat, 30% infection rate, 10 din me recovery
model = VirusModel(n_agents=100, width=15, height=15, 
                   initial_infected=3, infection_rate=0.3, recovery_days=10, seed=42)

print(f"{'Day':<5} | {'Healthy 🟢':<12} | {'Infected 🔴':<12} | {'Recovered 🔵':<12}")
print("-" * 50)

day = 0
while model.running and day < 50:
    day += 1
    model.step()
    
    s = sum(1 for a in model.agents if a.state.name == "SUSCEPTIBLE")
    i = sum(1 for a in model.agents if a.state.name == "INFECTED")
    r = sum(1 for a in model.agents if a.state.name == "RECOVERED")
    
    print(f"{day:<5} | {s:<12} | {i:<12} | {r:<12}")

print("\nEpidemic khatam! Virus ke active cases 0 ho gaye.")