import os
from PIL import Image

def audit_dataset(directory):
    print(f"--- 📊 AUDIT DU DATASET : {directory} ---")
    if not os.path.exists(directory):
        print(f"❌ Dossier {directory} introuvable.")
        return

    classes = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    total_images = 0
    stats = {}

    for cls in classes:
        cls_path = os.path.join(directory, cls)
        images = [f for f in os.listdir(cls_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        stats[cls] = len(images)
        total_images += len(images)

    print(f"\n📂 Nombre de classes : {len(classes)}")
    print(f"🖼️ Nombre total d'images : {total_images}")
    print("\n📈 Distribution par classe :")
    for cls, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_images) * 100
        print(f" - {cls}: {count} images ({percentage:.1f}%)")

    # Recherche de masques ou métadonnées
    print("\n🔍 Vérification des métadonnées/masques...")
    metadata_files = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if 'mask' in f.lower() or f.endswith(('.json', '.xml', '.csv')):
                metadata_files.append(f)
    
    if metadata_files:
        print(f" ✅ {len(metadata_files)} fichiers de métadonnées ou masques potentiels trouvés.")
        print(f" Exemples : {metadata_files[:5]}")
    else:
        print(" ℹ️ Aucun fichier nommé 'mask' ou métadonnées (JSON/XML) trouvé.")

if __name__ == "__main__":
    audit_dataset('datasets-cutisia')
