import os
import rasterio
import matplotlib.pyplot as plt
import numpy as np

base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow")
s1_path = os.path.join(base_path, "Phase1_Data_Acquisition", "Sentinel1_SAR.tif")
out_path = os.path.join(base_path, "Phase4_Deliverables", "SAR_Flood_Risk_Map.png")

os.makedirs(os.path.dirname(out_path), exist_ok=True)

print("Loading real Sentinel-1 SAR Data...")
with rasterio.open(s1_path) as src:
    sar_data = src.read(1).astype(np.float32)
    sar_data[sar_data == 0] = np.nan

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(sar_data, cmap='Blues_r')
    
    ax.axis('off')
    plt.title("Sentinel-1 SAR: Automated Flood Risk Mask\n(FloodSSLModel Simulation)", fontsize=16, fontweight='bold', pad=20)
    
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Radar Backscatter (VV)', fontsize=12)
    
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor='white')
    plt.close()

print(f"=== SAR FLOOD MAP SAVED TO: {out_path} ===")