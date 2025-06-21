import numpy as np
import matplotlib.pyplot as plt

# Get user inputs
time_steps = int(input("Enter number of time steps (e.g., 50): "))
initial_modulus = float(input("Enter initial bone modulus in GPa (e.g., 0.5): "))
max_modulus = float(input("Enter max achievable bone modulus in GPa (e.g., 20.0): "))
remodeling_rate = float(input("Enter remodeling rate (e.g., 0.3): "))

# Generate strain energy density linearly from 0 to 1
strain_energy_density = np.linspace(0, 1, time_steps)

# Initialize modulus array
bone_modulus = np.zeros(time_steps)
bone_modulus[0] = initial_modulus

# Bone remodeling simulation
for t in range(1, time_steps):
    stimulus = strain_energy_density[t]
    delta_modulus = remodeling_rate * stimulus * (max_modulus - bone_modulus[t-1])
    bone_modulus[t] = bone_modulus[t-1] + delta_modulus
    if bone_modulus[t] > max_modulus:
        bone_modulus[t] = max_modulus

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(range(time_steps), bone_modulus, label="Bone Modulus (GPa)")
plt.xlabel("Time Step")
plt.ylabel("Bone Modulus (GPa)")
plt.title("Simulated Bone Remodeling During Osseointegration")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
