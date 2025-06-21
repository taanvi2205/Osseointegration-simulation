from flask import Flask, render_template, request
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os

os.makedirs('static', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

app = Flask(__name__)

# Helper: Map qualitative inputs to numerical scores
def parameter_score(value, mapping):
    return mapping.get(value, 0.5)  # default mid-score

def age_to_score(age):
    if age <= 25:
        return 1.0  # Young adult
    elif age <= 50:
        return 0.7  # Middle-aged
    else:
        return 0.4  # Elderly

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_path = None
    if request.method == 'POST':
        # Retrieve form data
        bone_quality = request.form['bone_quality']
        patient_health = request.form['patient_health']
        age = int(request.form['age'])  
        implant_material = request.form['implant_material']
        surface_energy = request.form['surface_energy']
        osteoblast_activity = request.form['osteoblast_activity']

        # Map to scores between 0 and 1
        scores = {
            'bone_quality': parameter_score(bone_quality, {
                'Poor': 0.3, 'Average': 0.6, 'Good': 1.0
            }),
            'patient_health': parameter_score(patient_health, {
                'Compromised': 0.3, 'Average': 0.6, 'Healthy': 1.0
            }),
            'age': age_to_score(age)
,
            'implant_material': parameter_score(implant_material, {
                'Stainless Steel': 0.5, 'Titanium': 0.9, 'Zirconia': 1.0
            }),
            'surface_energy': parameter_score(surface_energy, {
                'Low': 0.4, 'Moderate': 0.7, 'High': 1.0
            }),
            'osteoblast_activity': parameter_score(osteoblast_activity, {
                'Low': 0.3, 'Moderate': 0.6, 'High': 1.0
            }),
        }

        # Combine all factors to define the remodeling rate (scale to 0.01–0.1)
        combined_factor = np.mean(list(scores.values()))
        remodeling_rate = 0.01 + (0.09 * combined_factor)

        time_steps = 100
        initial_modulus = 1.0  # GPa
        max_modulus = 20.0  # GPa
        strain_energy_density = np.linspace(0, 1, time_steps)

        bone_modulus = np.zeros(time_steps)
        bone_modulus[0] = initial_modulus

        for t in range(1, time_steps):
            stimulus = strain_energy_density[t]
            delta_modulus = remodeling_rate * stimulus * (max_modulus - bone_modulus[t - 1])
            bone_modulus[t] = bone_modulus[t - 1] + delta_modulus
            if bone_modulus[t] > max_modulus:
                bone_modulus[t] = max_modulus

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(range(time_steps), bone_modulus, label="Bone Modulus (GPa)")
        plt.xlabel("Time Step")
        plt.ylabel("Bone Modulus (GPa)")
        plt.title("Simulated Bone Remodeling During Osseointegration")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plot_path = os.path.join('static', 'bone_modulus_plot.png')
        plt.savefig(plot_path)
        plt.close()

    return render_template('index.html', plot_path=plot_path)

if __name__ == '__main__':
    app.run(debug=True)
