# models/schelling/run.py

from model import SchellingModel

# 1. 20x20 ka colony banaya jisme 80% ghar bhare hain aur 30% similarity rule hai
model = SchellingModel(width=20, height=20, density=0.8, homophily=0.3, seed=42)

print(f"Total Agents: {len(model.agents)}")
print("Simulation start ho rahi hai...\n")

step_count = 0
while model.running and step_count < 50:
    step_count += 1
    model.step()
    percent_happy = (model.happy_agents / len(model.agents)) * 100
    print(f"Step {step_count:02d}: {percent_happy:.1f}% log khush hain")

print(f"\nSimulation Complete! Total steps taken: {step_count}")