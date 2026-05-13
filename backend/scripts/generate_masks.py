import os
import sys
import cv2
import numpy as np
from glob import glob
from tqdm import tqdm

# Ajout du chemin racine pour supporter l'exécution sur Colab/Kaggle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.core.processor import load_unet_model, UNET_SIZE

def run_segmentation(dataset_path="datasets-cutisia", output_path="masks"):
    """
    Génère des masques de segmentation pour l'ensemble du jeu de données.
    Ces masques servent à isoler les lésions lors de l'entraînement.
    """
    # Chargement du modèle U-Net via le module core
    model, preprocess_input = load_unet_model()
    
    # Recherche de toutes les images
    image_paths = glob(os.path.join(dataset_path, "*/*"))
    image_paths = [p for p in image_paths if p.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Traitement de {len(image_paths)} images pour la segmentation...")
    
    for img_path in tqdm(image_paths, desc="Segmentation"):
        try:
            # Lecture
            original_img = cv2.imread(img_path)
            if original_img is None:
                continue
            
            h, w = original_img.shape[:2]
            img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            
            # Prétraitement U-Net
            img_resized = cv2.resize(img_rgb, UNET_SIZE)
            img_input = np.expand_dims(img_resized, axis=0)
            img_input = preprocess_input(img_input)
            
            # Prédiction
            pr_mask = model.predict(img_input, verbose=0).squeeze()
            
            # Post-traitement du masque
            binary_mask = (pr_mask > 0.5).astype(np.uint8) * 255
            final_mask = cv2.resize(binary_mask, (w, h))
            
            # Organisation des dossiers de sortie
            cls_name = os.path.basename(os.path.dirname(img_path))
            save_dir = os.path.join(output_path, cls_name)
            os.makedirs(save_dir, exist_ok=True)
            
            # Sauvegarde
            mask_name = os.path.basename(img_path)
            cv2.imwrite(os.path.join(save_dir, mask_name), final_mask)
            
        except Exception as e:
            print(f"Erreur sur {img_path} : {str(e)}")

if __name__ == "__main__":
    run_segmentation()
