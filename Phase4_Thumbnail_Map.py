import ee
import requests
import os

ee.Initialize()
print("GEE Initialized.")

ethiopia = ee.FeatureCollection("FAO/GAUL/2015/level0").filter(ee.Filter.eq('ADM0_NAME', 'Ethiopia'))

print("Building FAST Sentinel-2 composite...")
s2_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                 .filterBounds(ethiopia)
                 .filterDate('2023-01-01', '2023-01-31')
                 .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)))

s2_composite = s2_collection.mosaic().clip(ethiopia)

print("Generating map thumbnail...")
try:
    bbox = ee.Geometry.Rectangle([32.9, 3.4, 47.9, 14.9])
    url = s2_composite.select(['B4', 'B3', 'B2']).getThumbURL({
        'dimensions': 600, 
        'region': bbox,
        'format': 'png',
        'min': 0,
        'max': 3000
    })
    
    print("Downloading image...")
    base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow\\Phase4_Deliverables")
    out_path = os.path.join(base_path, "Ethiopia_National_Map.png")
    
    if os.path.exists(out_path):
        os.remove(out_path)
    
    response = requests.get(url, timeout=60)
    
    if response.status_code == 200 and response.headers.get('Content-Type') == 'image/png':
        with open(out_path, 'wb') as f:
            f.write(response.content)
        print(f"=== SUCCESS: VALID MAP SAVED TO {out_path} ===")
    else:
        print(f"ERROR: Status {response.status_code}")
        print("Details:", response.text[:300])

except Exception as e:
    print(f"Failed: {e}")
