import ee
import geemap
import os
import rasterio
import matplotlib.pyplot as plt
import numpy as np

ee.Initialize()
print("GEE Initialized.")

# 1. Get the OFFICIAL boundary of Ethiopia
ethiopia = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq('ADM0_NAME', 'Ethiopia'))

# 2. Create a cloud-free median composite
print("Building cloud-free Sentinel-2 composite for Ethiopia...")
s2_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                 .filterBounds(ethiopia)
                 .filterDate('2023-01-01', '2023-12-31')
                 .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)))

s2_composite = s2_collection.median().clip(ethiopia)

# 3. Use a simplified bounding box
download_region = ee.Geometry.Rectangle([32.9, 3.4, 47.9, 14.9])
base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase1_Data_Acquisition")
out_path = os.path.join(base_path, "Ethiopia_Sentinel2_Composite_5km.tif")

if os.path.exists(out_path):
    os.remove(out_path)

print("Downloading Ethiopia Composite at 5km resolution via geedim...")
try:
    # geedim handles the tiling automatically
    geemap.download_ee_image(
        s2_composite.select(['B4', 'B3', 'B2']),
        filename=out_path,
        scale=5000,
        region=download_region,
        crs='EPSG:4326'
    )
    print("Download finished.")
except Exception as e:
    print(f"Download failed: {e}")
    exit(1)

# Verify file
if not os.path.exists(out_path):
    print("ERROR: File does not exist.")
    exit(1)

with open(out_path, 'rb') as f:
    header = f.read(4)
    if header not in [b'II*\x00', b'MM\x00*']:
        print(f"ERROR: File is not a valid GeoTIFF. Header: {header}")
        exit(1)
    else:
        print("Valid GeoTIFF file confirmed.")

# 4. Generate the map
print("Generating Full Ethiopia National Map...")
out_map_path = os.path.join(base_path, "..", "Phase4_Deliverables", "Ethiopia_National_Map.png")
os.makedirs(os.path.dirname(out_map_path), exist_ok=True)

with rasterio.open(out_path) as src:
    img = src.read([1, 2, 3]).astype(np.float32)
    valid_mask = np.any(img > 0, axis=0)
    if np.any(valid_mask):
        valid_pixels = img[:, valid_mask]
        p98 = np.percentile(valid_pixels, 98)
    else:
        p98 = 1.0
    img_normalized = np.clip(img / p98, 0, 1)
    img_normalized[:, ~valid_mask] = 1.0
    img_plot = np.transpose(img_normalized, (1, 2, 0))
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img_plot)
    ax.axis('off')
    plt.title("Sentinel-2 True Color Composite\nOfficial Boundary of Ethiopia (2023)", fontsize=16, fontweight='bold', pad=20)
    plt.savefig(out_map_path, dpi=300, bbox_inches='tight', pad_inches=0.1, facecolor='white')
    plt.close()

print(f"=== PUBLICATION-READY MAP SAVED TO: {out_map_path} ===")
