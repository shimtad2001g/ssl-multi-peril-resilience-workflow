import ee
import geemap
import os

ee.Initialize()
print("GEE Initialized.")

ethiopia = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq('ADM0_NAME', 'Ethiopia'))

print("Building composite (this takes a few seconds)...")
s2_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                 .filterBounds(ethiopia)
                 .filterDate('2023-01-01', '2023-12-31')
                 .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)))

s2_composite = s2_collection.median().clip(ethiopia)

base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase4_Deliverables")
out_path = os.path.join(base_path, "Ethiopia_10km.tif")

if os.path.exists(out_path):
    os.remove(out_path)

print("Downloading via geemap (10km scale)...")
try:
    geemap.ee_export_image(
        s2_composite.select(['B4', 'B3', 'B2']),
        filename=out_path,
        scale=10000,  # 10km resolution - guaranteed to be tiny and fast
        region=ethiopia.geometry().bounds(),
        file_per_band=False
    )
    print("Download finished.")
except Exception as e:
    print(f"Failed: {e}")
    exit(1)

if os.path.exists(out_path):
    print(f"=== SUCCESS: TIF SAVED TO {out_path} ===")
else:
    print("ERROR: File not found.")
