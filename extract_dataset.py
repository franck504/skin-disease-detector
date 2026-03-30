import os
import io
import pandas as pd
from PIL import Image
from tqdm import tqdm
from pathlib import Path

# Paths
base_dir = Path.home() / "Téléchargements" / "Africa-skin-cancer-images-EHR"
data_dir = base_dir / "data"
output_dir = base_dir / "extracted_images"

# Create output dir if not exists
os.makedirs(output_dir, exist_ok=True)

# Get all parquet files
parquet_files = [f for f in data_dir.glob("*.parquet")]

print(f"Found {len(parquet_files)} parquet files to process.")

for pfile in parquet_files:
    print(f"Processing {pfile.name}...")
    df = pd.read_parquet(pfile)
    
    # Process each row
    for _, row in tqdm(df.iterrows(), total=len(df)):
        # Determine the diagnosis column
        diag_col = 'diagnosis' if 'diagnosis' in df.columns else 'dx'
        if diag_col not in df.columns:
            continue
            
        diagnosis = str(row[diag_col]).replace(" ", "_").lower()
        image_id = row['image_id']
        
        # Create folder for diagnosis
        diag_path = output_dir / diagnosis
        os.makedirs(diag_path, exist_ok=True)
        
        # Save image
        try:
            # Handle different image columns
            if 'image' in df.columns and isinstance(row['image'], dict) and 'bytes' in row['image']:
                image_data = row['image']['bytes']
            elif 'image_bytes' in df.columns:
                image_data = row['image_bytes']
            else:
                print(f"No image data column found for {image_id}")
                continue

            if image_data is None:
                continue
                
            img = Image.open(io.BytesIO(image_data))
            
            # Save as jpg
            img_filename = f"{image_id}.jpg"
            img.save(diag_path / img_filename, "JPEG")
        except Exception as e:
            print(f"Error saving image {image_id}: {e}")

print(f"\nExtraction complete! Images are in {output_dir}")
