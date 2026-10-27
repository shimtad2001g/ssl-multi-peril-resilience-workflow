# Phase3_Risk_Mitigation.py
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

DATA_DIR = r"C:\Users\SHIMELES_TADESSE\MR-EO-Ethiopia\01_Data_Acquisition"
OUT_DIR = r"C:\Users\SHIMELES_TADESSE\Desktop\ssl-multi-peril-resilience-workflow\03_Risk_Mitigation"
os.makedirs(OUT_DIR, exist_ok=True)

print("Loading data for Risk Mitigation...")
# Load Optical (Sentinel-2) for VCI
with rasterio.open(os.path.join(DATA_DIR, "s2_optical.tif")) as src:
    optical = src.read().astype(float)
    profile = src.profile

# Load SAR for Inundation
with rasterio.open(os.path.join(DATA_DIR, "s1_sar.tif")) as src:
    sar = src.read().astype(float)

# Load DEM for Slope
with rasterio.open(os.path.join(DATA_DIR, "srtm_dem.tif")) as src:
    dem = src.read(1).astype(float)

# --- PILLAR 1: Multi-Peril Parametric Insurance Modeling ---
print("Calculating Dual-Trigger (VCI & SAR)...")
# 1. Calculate Mock VCI (Vegetation Condition Index)
red = optical[0]
nir = optical[1]
ndvi = (nir - red) / (nir + red + 1e-10)
# Mock historical Min/Max NDVI to calculate VCI
ndvi_min = np.percentile(ndvi, 5)
ndvi_max = np.percentile(ndvi, 95)
vci = ((ndvi - ndvi_min) / (ndvi_max - ndvi_min + 1e-10)) * 100

# 2. SAR Inundation (Thresholding VH band - assuming water is < -15dB)
# (Note: Band 2 is VH in our exported file)
sar_vh = sar[1] 
sar_flood = np.where(sar_vh < -15.0, 1, 0)

# 3. Dual-Trigger: VCI < 30% AND SAR Flood == 1
insurance_trigger = np.where((vci < 30) & (sar_flood == 1), 1, 0)

# Save Insurance Trigger
profile.update(dtype=rasterio.uint8, count=1)
with rasterio.open(os.path.join(OUT_DIR, "insurance_trigger.tif"), 'w', **profile) as dst:
    dst.write(insurance_trigger.astype(np.uint8), 1)

# --- PILLAR 2: Synergistic NBS Targeting (MCDA) ---
print("Running MCDA for NBS Zoning...")
# Normalize inputs (0 to 1)
slope = np.abs(np.gradient(dem)[0] + np.gradient(dem)[1]) # Mock slope
slope_norm = (slope - np.min(slope)) / (np.max(slope) - np.min(slope) + 1e-10)

# Mock Land Degradation (using low NDVI as proxy for degradation)
degradation_norm = 1.0 - (ndvi - np.min(ndvi)) / (np.max(ndvi) - np.min(ndvi) + 1e-10)

# MCDA Weights (Flood Risk 40%, Slope 30%, Degradation 30%)
mcda_score = (sar_flood * 0.4) + (slope_norm * 0.3) + (degradation_norm * 0.3)

# Zoning: 0 = Low, 1 = Medium, 2 = High Suitability for NBS
nbs_zones = np.zeros_like(mcda_score)
nbs_zones[mcda_score > 0.4] = 1
nbs_zones[mcda_score > 0.7] = 2

# Save NBS Zoning
profile.update(dtype=rasterio.uint8, count=1)
with rasterio.open(os.path.join(OUT_DIR, "nbs_zoning.tif"), 'w', **profile) as dst:
    dst.write(nbs_zones.astype(np.uint8), 1)

# --- Generate Previews ---
print("Generating Map Previews...")
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Insurance Trigger Map
axes[0].imshow(insurance_trigger, cmap='Reds')
axes[0].set_title('Dual-Trigger Insurance Payouts\n(VCI < 30% & SAR Flood)')
axes[0].axis('off')

# NBS Zoning Map
cmap_nbs = ListedColormap(['lightgreen', 'gold', 'darkorange'])
im = axes[1].imshow(nbs_zones, cmap=cmap_nbs)
axes[1].set_title('NBS Suitability & Flood Mitigation Zoning')
axes[1].axis('off')
cbar = plt.colorbar(im, ax=axes[1], ticks=[0, 1, 2])
cbar.ax.set_yticklabels(['Low', 'Medium', 'High'])

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "Phase3_Maps_Preview.png"), dpi=300)
print(f"Phase 3 Complete! Previews saved to {OUT_DIR}")