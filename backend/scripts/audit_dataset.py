import os
from glob import glob

def audit_dataset(dataset_path="datasets-cutisia"):
    """
    Analyse le jeu de données pour compter le nombre d'images par classe 
    et identifier d'éventuels déséquilibres.
    """
    if not os.path.exists(dataset_path):
        print(f"Erreur : Le dossier {dataset_path} est introuvable.")
        return

    print(f"Analyse du jeu de données dans : {dataset_path}")
    classes = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
    
    total_images = 0
    stats = {}

    for cls in sorted(classes):
        cls_path = os.path.join(dataset_path, cls)
        # On ne compte que les fichiers images standards
        images = glob(os.path.join(cls_path, "*.[jJ][pP][gG]")) + \
                 glob(os.path.join(cls_path, "*.[jJ][pP][eE][gG]")) + \
                 glob(os.path.join(cls_path, "*.[pP][nN][gG]"))
        
        count = len(images)
        stats[cls] = count
        total_images += count
        print(f"  - {cls} : {count} images")

    print("-" * 30)
    print(f"Total des images détectées : {total_images}")
    
    if total_images > 0:
        print("Répartition relative :")
        for cls, count in stats.items():
            percentage = (count / total_images) * 100
            print(f"  - {cls} : {percentage:.2f}%")

if __name__ == "__main__":
    audit_dataset()
