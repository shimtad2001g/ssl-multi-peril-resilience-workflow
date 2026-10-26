import ee
import requests
import os

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

# 3. Use a simplified bounding box for the download region to avoid geometry errors
# Approximate bounds of Ethiopia: [min_lon, min_lat, max_lon, max_lat]
download_region = ee.Geometry.Rectangle([32.9, 3.4, 47.9, 14.9])

# 4. Get the download URL directly using getDownloadURL
print("Generating download URL...")
try:
    url = s2_composite.select(['B4', 'B3', 'B2']).getDownloadURL({
        'scale': 2000,  # 2km resolution
        'region': download_region,
        'format': 'GeoTIFF',
        'crs': 'EPSG:4326'
    })

    print("Downloading file...")
    base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase1_Data_Acquisition")
    out_path = os.path.join(base_path, "Ethiopia_Sentinel2_Composite.tif")
    
    response = requests.get(url)
    with open(out_path, 'wb') as f:
        f.write(response.content)
        
    print(f"=== SUCCESS: FULL ETHIOPIA COMPOSITE DOWNLOADED to {out_path} ===")

except Exception as e:
    print(f"=== DOWNLOAD FAILED: {e} ===")
