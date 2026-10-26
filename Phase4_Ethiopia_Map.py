import os
import rasterio
import matplotlib.pyplot as plt
import numpy as np

base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow")
s2_path = os.path.join(base_path, "Phase1_Data_Acquisition", "Ethiopia_Sentinel2_Composite.tif")
out_path = os.path.join(base_path, "Phase4_Deliverables", "Ethiopia_National_Map.png")

os.makedirs(os.path.dirname(out_path), exist_ok=True)

print("Generating Full Ethiopia National Map...")
with rasterio.open(s2_path) as src:
    img = src.read([1, 2, 3]).astype(np.float32)
    
    # Create a mask for valid pixels (where data exists)
    valid_mask = np.any(img > 0, axis=0)
    
    # If there is valid data, calculate the 98th percentile to stretch contrast
    if np.any(valid_mask):
        valid_pixels = img[:, valid_mask]
        p98 = np.percentile(valid_pixels, 98)
    else:
        p98 = 1.0
        
    # Normalize the image
    img_normalized = np.clip(img / p98, 0, 1)
    
    # Set the background (where there is no Ethiopia data) to white
    img_normalized[:, ~valid_mask] = 1.0 
    
    # Transpose to (Height, Width, Channels)
    img_plot = np.transpose(img_normalized, (1, 2, 0))
    
    # Create a large, high-resolution figure
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img_plot)
    
    # Remove axes for a clean map look
    ax.axis('off')
    
    # Add a professional title
    plt.title("Sentinel-2 True Color Composite\nOfficial Boundary of Ethiopia (2023)", fontsize=16, fontweight='bold', pad=20)
    
    # Save the map
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor='white')
    plt.close()

print(f"=== PUBLICATION-READY MAP SAVED TO: {out_path} ===")
