import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Define paths
base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase4_Deliverables")
img1_path = os.path.join(base_path, "Ethiopia_National_Map.png")
img2_path = os.path.join(base_path, "NBS_Targeting_Map.png")
img3_path = os.path.join(base_path, "SAR_Flood_Risk_Map.png")
out_path = os.path.join(base_path, "Integrated_Master_Map.png")

print("Loading the generated maps...")
# Load the images
img1 = mpimg.imread(img1_path)
img2 = mpimg.imread(img2_path)
img3 = mpimg.imread(img3_path)

print("Assembling the Master Composite Map...")
# Create a figure with 1 row and 3 columns
fig, axes = plt.subplots(1, 3, figsize=(24, 8))

# Plot 1: Base Hazard Map
axes[0].imshow(img1)
axes[0].set_title("A. Sentinel-2 Optical Hazard Map\n(Drought Trigger Zone)", fontsize=16, fontweight='bold')
axes[0].axis('off')

# Plot 2: MCDA Targeting
axes[1].imshow(img2)
axes[1].set_title("B. MCDA NBS Targeting\n(Optimal Intervention Locations)", fontsize=16, fontweight='bold')
axes[1].axis('off')

# Plot 3: SAR Flood Risk
axes[2].imshow(img3)
axes[2].set_title("C. Sentinel-1 SAR Flood Risk\n(Radar Backscatter)", fontsize=16, fontweight='bold')
axes[2].axis('off')

# Add an overall title
fig.suptitle("Integrated Synergistic Multi-Peril Resilience Master Map (Ethiopia)", 
             fontsize=22, fontweight='bold', y=1.05)

# Save the final composite image
plt.tight_layout()
plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print(f"=== MASTER MAP SAVED TO: {out_path} ===")