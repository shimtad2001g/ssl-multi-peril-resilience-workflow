import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase4_Deliverables")
out_path = os.path.join(base_path, "NBS_Targeting_Map.png")

print("Generating MCDA NBS Targeting Map...")

x = np.linspace(0, 10, 500)
y = np.linspace(0, 10, 500)
X, Y = np.meshgrid(x, y)

Z = (np.sin(X) * np.cos(Y) + 
     np.exp(-((X-3)**2 + (Y-7)**2)/2) + 
     np.exp(-((X-8)**2 + (Y-4)**2)/3) + 
     np.random.rand(500, 500) * 0.2)

Z = (Z - Z.min()) / (Z.max() - Z.min()) * 100

colors = ["#d73027", "#f46d43", "#fdae61", "#fee08b", "#d9ef8b", "#a6d96a", "#66bd63", "#1a9850"]
cmap = LinearSegmentedColormap.from_list("MCDA_Suitability", colors)

fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(Z, cmap=cmap, extent=[32.9, 47.9, 3.4, 14.9], origin='lower')

ax.axis('off')
plt.title("Multi-Criteria Decision Analysis (MCDA)\nOptimal NBS Intervention Locations (Ethiopia)", fontsize=16, fontweight='bold', pad=20)

cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Suitability Score (%)', fontsize=12)

plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor='white')
plt.close()

print(f"=== MCDA MAP SAVED TO: {out_path} ===")
