import os
import rasterio
import matplotlib.pyplot as plt
import numpy as np

base_path = os.path.expanduser("~\\Desktop\\ssl-multi-peril-resilience-workflow")
s2_path = os.path.join(base_path, "Phase1_Data_Acquisition", "Sentinel2_Optical.tif")
out_path = os.path.join(base_path, "Phase4_Deliverables", "Publication_Ready_Map.png")

with rasterio.open(s2_path) as src:
    img = src.read([1, 2, 3]).astype(np.float32)
    
    # 1. Find the bounding box of the valid (non-black) pixels
    valid_mask = np.any(img > 0, axis=0)
    rows = np.any(valid_mask, axis=1)
    cols = np.any(valid_mask, axis=0)
    
    if np.any(rows) and np.any(cols):
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        
        # 2. Crop the image to the valid area
        img_cropped = img[:, rmin:rmax+1, cmin:cmax+1]
    else:
        img_cropped = img
        
    # 3. Normalize the cropped image for contrast
    valid_pixels = img_cropped[img_cropped > 0]
    if valid_pixels.size > 0:
        p98 = np.percentile(valid_pixels, 98)
    else:
        p98 = 1.0
        
    img_normalized = np.clip(img_cropped / p98, 0, 1)
    img_plot = np.transpose(img_normalized, (1, 2, 0))
    
    # 4. Create a professional plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img_plot)
    
    # 5. Remove axes and add a clean title
    ax.axis('off')
    plt.title("Sentinel-2 True Color Composite\nDrought Trigger Zone (Ethiopia)", fontsize=14, fontweight='bold')
    
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()

print("=== PUBLICATION READY MAP GENERATED ===")
