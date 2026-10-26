import ee
import geemap
import os

ee.Initialize()
print("GEE Initialized successfully.")

# Define a MUCH SMALLER Area of Interest (0.1 degree box over Ethiopia)
# This keeps the file size well below the 50MB limit.
aoi = ee.Geometry.Rectangle([38.0, 8.0, 38.1, 8.1])

print("Fetching Sentinel-2 Optical Data...")
s2_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                 .filterBounds(aoi)
                 .filterDate('2023-01-01', '2023-12-31')
                 .sort('CLOUDY_PIXEL_PERCENTAGE')
                 .first())

print("Fetching Sentinel-1 SAR Data...")
s1_collection = (ee.ImageCollection('COPERNICUS/S1_GRD')
                 .filterBounds(aoi)
                 .filterDate('2023-01-01', '2023-12-31')
                 .filter(ee.Filter.eq('instrumentMode', 'IW'))
                 .first())

base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase1_Data_Acquisition")
os.makedirs(base_path, exist_ok=True)

s2_path = os.path.join(base_path, "Sentinel2_Optical.tif")
s1_path = os.path.join(base_path, "Sentinel1_SAR.tif")

print(f"Downloading Sentinel-2...")
geemap.ee_export_image(s2_collection.select(['B4', 'B3', 'B2']), filename=s2_path, scale=30, region=aoi, file_per_band=False)

print(f"Downloading Sentinel-1...")
geemap.ee_export_image(s1_collection.select(['VV']), filename=s1_path, scale=30, region=aoi, file_per_band=False)

print("Phase 1 Data Acquisition Complete!")
