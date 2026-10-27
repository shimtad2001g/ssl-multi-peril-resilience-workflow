import os
import numpy as np
import rasterio
from rasterio.transform import from_origin

# Define paths
DATA_DIR = r"C:\Users\SHIMELES_TADESSE\MR-EO-Ethiopia\01_Data_Acquisition"
os.makedirs(DATA_DIR, exist_ok=True)

# Mock spatial dimensions
width, height = 500, 500
transform = from_origin(38.0, 9.0, 0.001, 0.001) # Top-left corner, pixel size

print("Generating Mock Optical (Sentinel-2) Data...")
# Create 3 bands (Red, Green, Blue)
optical_data = np.random.randint(0, 10000, size=(3, height, width), dtype=np.uint16)
with rasterio.open(os.path.join(DATA_DIR, "s2_optical.tif"), 'w', driver='GTiff', height=height, width=width, count=3, dtype=np.uint16, crs='EPSG:4326', transform=transform) as dst:
    dst.write(optical_data)

print("Generating Mock SAR (Sentinel-1) Data...")
# Create 2 bands (VV, VH). Mocking some flood pixels (negative values)
sar_data = np.random.uniform(-25, 0, size=(2, height, width)).astype(np.float32)
sar_data[1, 100:200, 100:200] = -18.0 # Mock water pixels in VH band
with rasterio.open(os.path.join(DATA_DIR, "s1_sar.tif"), 'w', driver='GTiff', height=height, width=width, count=2, dtype=np.float32, crs='EPSG:4326', transform=transform) as dst:
    dst.write(sar_data)

print("Generating Mock DEM (SRTM) Data...")
# Create 1 band for elevation
dem_data = np.random.uniform(1000, 3000, size=(1, height, width)).astype(np.float32)
with rasterio.open(os.path.join(DATA_DIR, "srtm_dem.tif"), 'w', driver='GTiff', height=height, width=width, count=1, dtype=np.float32, crs='EPSG:4326', transform=transform) as dst:
    dst.write(dem_data)

print(f"Mock data successfully generated in {DATA_DIR}")