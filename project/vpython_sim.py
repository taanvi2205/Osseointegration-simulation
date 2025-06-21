from vpython import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import sys

# Get parameters from command line
speed = float(sys.argv[1]) if len(sys.argv) > 1 else 0.01
density = int(sys.argv[2]) if len(sys.argv) > 2 else 40


# === SCENE SETUP ===
scene.title = "<b>Osseointegration Simulation</b>"
scene.width = 1100
scene.height = 700
scene.background = color.white
scene.forward = vector(-1, -0.2, -1)

# Custom colors
BONE_COLOR = vector(0.93, 0.79, 0.69)  # Light bone color
IMPLANT_COLOR = color.gray(0.7)
CELL_COLOR = color.green
GROWTH_COLOR = vector(1, 0.84, 0)  # Gold color for new bone

# === GRAPH SETUP WITH MODERN STYLING ===
# Create a styled window for the graphs
graph_window = tk.Tk()
graph_window.title("Simulation Metrics Dashboard")
graph_window.geometry("700x800")
graph_window.configure(bg='#f0f2f5')

# Apply modern style
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#f0f2f5')
style.configure('TLabel', background='#f0f2f5', font=('Helvetica', 10))
style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))

# Create container frame
frame = ttk.Frame(graph_window, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Title label
title_label = ttk.Label(frame, text="Osseointegration Progress Metrics", style='Title.TLabel')
title_label.pack(pady=(0, 10))

# Create figure with custom style
plt.style.use('default')  # Use default style as base
plt.rcParams.update({
    'axes.facecolor': '#f9f9f9',
    'axes.grid': True,
    'grid.linestyle': '--',
    'grid.alpha': 0.6,
    'axes.titleweight': 'bold',
    'axes.titlesize': 12,
    'axes.titlepad': 15,
    'axes.labelpad': 8,
    'lines.linewidth': 2,
    'font.family': 'sans-serif'
})

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 7))
fig.patch.set_facecolor('#f0f2f5')

# Initialize graph data
osteoblasts_time, osteoblasts_count = [], []
bone_time, bone_growth = [], []

def init_graphs():
    ax1.clear()
    ax2.clear()
    
    # Styled cell count graph
    ax1.set_title("Osteoblasts Migration")
    ax1.set_ylabel("Cells Reached")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylim(0, 100)
    
    # Styled bone growth graph
    ax2.set_title("Bone Formation Progress")
    ax2.set_ylabel("Volume (units)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylim(0, 50)
    
    fig.tight_layout(pad=3.0)
    canvas.draw()

canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Status frame
status_frame = ttk.Frame(frame)
status_frame.pack(fill=tk.X, pady=(10, 0))
ttk.Label(status_frame, text="Simulation Status:").pack(side=tk.LEFT)
sim_status = ttk.Label(status_frame, text="Ready", foreground="green")
sim_status.pack(side=tk.LEFT, padx=5)

init_graphs()

# === ENHANCED UI CONTROLS ===
# Custom control styling in VPython
scene.append_to_caption("\n\n<b>Simulation Controls</b>\n\n")

# Slider styling
scene.append_to_caption("<div style='margin-bottom: 10px;'>")
scene.append_to_caption("<b>Growth Speed:</b> ")
def update_speed(s): pass
speed_slider = slider(min=0.005, max=0.05, value=speed, length=300, right=15, bind=update_speed)
scene.append_to_caption("</div>")

scene.append_to_caption("<div style='margin-bottom: 10px;'>")
scene.append_to_caption("<b>Bone Density:</b> ")
def update_density(d): pass
density_slider = slider(min=10, max=80, value=density, step=5, length=300, right=15, bind=update_density)
scene.append_to_caption("</div>")

# Status text with better formatting
scene.append_to_caption("<div style='margin-top: 20px; padding: 10px; background-color: #f5f5f5; border-radius: 5px;'>")
status_text = wtext(text="<b>Status:</b> Click 'Start Simulation' to begin.\n\n")
scene.append_to_caption("</div>")

# === GLOBAL VARIABLES ===
pores = []
osteoblasts = []
bone_growths = []
osteoblasts_reached = 0
bone_formation = 0
sim_running = False
time = 0

def update_graphs():
    osteoblasts_time.append(time)
    osteoblasts_count.append(osteoblasts_reached)
    bone_time.append(time)
    bone_growth.append(bone_formation)

    ax1.clear()
    ax2.clear()
    
    # Update cell count graph with styling
    ax1.plot(osteoblasts_time, osteoblasts_count, color='#2ecc71', marker='o', markersize=4, markevery=5)
    ax1.set_title("Osteoblasts Migration")
    ax1.set_ylabel("Cells Reached")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylim(0, max(100, max(osteoblasts_count)*1.1))
    
    # Update bone growth graph with styling
    ax2.plot(bone_time, bone_growth, color='#e67e22', marker='s', markersize=4, markevery=5)
    ax2.set_title("Bone Formation Progress")
    ax2.set_ylabel("Volume (units)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylim(0, max(50, max(bone_growth)*1.1))
    
    fig.tight_layout(pad=3.0)
    canvas.draw()
    graph_window.update()
    sim_status.config(text="Running" if sim_running else "Completed", 
                    foreground="green" if sim_running else "blue")

def start_simulation():
    global pores, osteoblasts, bone_growths, osteoblasts_reached, bone_formation, sim_running, time
    global osteoblasts_time, osteoblasts_count, bone_time, bone_growth
    
    # Reset data
    osteoblasts_time, osteoblasts_count = [], []
    bone_time, bone_growth = [], []
    
    sim_running = False
    time = 0
    osteoblasts_reached = 0
    bone_formation = 0

    # Clear previous objects
    for obj in scene.objects:
        if obj not in [scene.caption_anchor, scene.title_anchor]:
            obj.visible = False
    pores.clear()
    osteoblasts.clear()
    bone_growths.clear()

    # Create styled labels
    label(pos=vector(0, 2.3, 0), text="<b>Bone Tissue</b>", height=16, box=False, color=color.black)
    label(pos=vector(0, -2.3, 0), text="<b>Implant</b>", height=16, box=False, color=color.black)
    label(pos=vector(1.8, 0, 0), text="<b>Osteoblasts</b>", height=16, box=False, color=CELL_COLOR)

    # Create main objects with better visuals
    bone = cylinder(pos=vector(0, -2, 0), axis=vector(0, 4, 0), radius=2, 
                   color=BONE_COLOR, opacity=0.4, shininess=0.1)
    implant = cylinder(pos=vector(0, -2, 0), axis=vector(0, 4, 0), radius=0.7, 
                      color=IMPLANT_COLOR, opacity=0.9, shininess=0.8)

    # Create pores with better visual style
    num_rings = 12
    pores_per_ring = int(density_slider.value / 3)
    for i in range(num_rings):
        h = -2 + (i * (4 / num_rings))
        for j in range(pores_per_ring):
            angle = j * (2 * np.pi / pores_per_ring)
            x = 0.75 * np.cos(angle)
            z = 0.75 * np.sin(angle)
            p = sphere(pos=vector(x, h, z), radius=0.04, color=color.gray(0.7), 
                      emissive=False, shininess=0.5)
            pores.append(p)

    # Create osteoblasts with better visual style
    for p in pores:
        direction = -p.pos.norm()
        start_pos = p.pos + direction * 1.5
        cell = sphere(pos=start_pos, radius=0.03, color=CELL_COLOR, 
                     emissive=False, make_trail=True, trail_radius=0.01,
                     trail_color=color.green, retain=50)
        osteoblasts.append((cell, p.pos - start_pos))

    status_text.text = "<b>Status:</b> Simulation running...\n"
    sim_running = True
    init_graphs()
    sim_status.config(text="Running", foreground="green")

def run_animation():
    global sim_running, osteoblasts_reached, bone_formation, time
    implant_pos = vector(0, 2, 0)
    bone_radius = 2
    last_update_time = 0

    while True:
        rate(30)
        if not sim_running:
            continue
            
        growth_rate = speed_slider.value
        all_done = True
        time += 0.1

        # Update osteoblasts
        for cell, direction in osteoblasts:
            target = implant_pos
            dist = mag(cell.pos - target)
            if dist > 0.1:
                if mag(cell.pos) < bone_radius:
                    cell.pos += growth_rate * direction.norm()
                else:
                    cell.pos = cell.pos.norm() * bone_radius

                if mag(cell.pos - implant_pos) < 0.5 and cell.color != color.blue:
                    cell.color = color.blue
                    cell.trail_color = color.blue
                    new_bone = cylinder(pos=cell.pos, axis=vector(0, 0.1, 0), 
                                     radius=0.1, color=GROWTH_COLOR, 
                                     opacity=0.8, shininess=0.3)
                    bone_growths.append(new_bone)
                    osteoblasts_reached += 1
                    bone_formation += 0.2

                all_done = False

        # Update graphs periodically
        if time - last_update_time >= 0.5:  # Update twice per second
            update_graphs()
            last_update_time = time

        if all_done:
            sim_running = False
            status_text.text = f"<b>Status:</b> Osseointegration complete!\n\n" \
                             f"<b>Results:</b>\n" \
                             f"- Osteoblasts reached: {osteoblasts_reached}\n" \
                             f"- Bone volume formed: {bone_formation:.1f} units\n" \
                             f"- Time elapsed: {time:.1f} seconds"
            update_graphs()
            
            total_cells = len(osteoblasts)
            percent_reached = (osteoblasts_reached / total_cells) * 100 if total_cells else 0

            # Add result label in the scene
            result_label = label(pos=vector(0, 2.8, 0), 
                               text=f"<b>Analysis</b>\nCells: {total_cells}\nSuccess: {percent_reached:.1f}%\nBone: {bone_formation:.1f}u\nTime: {time:.1f}s", 
                               height=14, box=True, border=10, 
                               color=color.white, background=color.blue,
                               linecolor=color.white, linewidth=2,
                               font='sans', space=0.4)
            break

# Styled button to start simulation
def restart_clicked(b):
    start_simulation()
    run_animation()

scene.append_to_caption("<div style='margin-top: 20px;'>")
restart_button = button(text="<b>Start Simulation</b>", bind=restart_clicked,
                       color=vector(0.2, 0.6, 0.8), background=color.white)
scene.append_to_caption("</div>")

# Start the Tkinter event loop
graph_window.mainloop()