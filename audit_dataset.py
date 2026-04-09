import os
import sys

def audit_dataset():
    # Détection dynamique du dossier
    possible_paths = [
        'datasets-cutisia',
        '/content/skin-disease-detector/datasets-cutisia',
        '/content/drive/MyDrive/cutisia_datasets'
    ]
    
    DATA_DIR = None
    for p in possible_paths:
        if os.path.exists(p):
            DATA_DIR = p
            break
            
    if not DATA_DIR:
        print("❌ Dossier datasets-cutisia introuvable.")
        print(f"DEBUG info: os.getcwd() = {os.getcwd()}")
        print(f"DEBUG info: os.listdir() = {os.listdir('.')}")
        return

    print(f"--- 📊 AUDIT DU DATASET ({DATA_DIR}) ---")
    classes = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
    
    total = 0
    for cls in classes:
        count = len([f for f in os.listdir(os.path.join(DATA_DIR, cls)) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
        print(f" - {cls}: {count} images")
        total += count
    print(f"\n✅ Total : {total} images.")

if __name__ == "__main__":
    audit_dataset()
