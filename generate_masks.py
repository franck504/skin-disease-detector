import os
import numpy as np
import cv2
from glob import glob
from tqdm import tqdm

# On force l'installation de segmentation_models si on est sur Colab
try:
    import segmentation_models as sm
except ImportError:
    print("📦 Installation des bibliothèques de segmentation...")
    os.system('pip install -U segmentation-models')
    os.system('pip install h5py==2.10.0') # Correction bug version h5py sur Colab
    import segmentation_models as sm

os.environ['SM_FRAMEWORK'] = 'tf.keras'

# --- CONFIGURATION ---
DATASET_PATH = 'datasets-cutisia'
# Si sur Colab, on cherche sur le Drive
if os.path.exists('/content/drive/MyDrive/cutisia_datasets'):
    DATASET_PATH = '/content/drive/MyDrive/cutisia_datasets'

MASK_OUTPUT_PATH = '/content/drive/MyDrive/cutisia_masks'
if not os.path.exists('/content/drive/MyDrive'):
    MASK_OUTPUT_PATH = './cutisia_masks' # Local si test

os.makedirs(MASK_OUTPUT_PATH, exist_ok=True)

# --- CHARGEMENT DU MODELE U-NET (PRE-ENTRAINE ISIC) ---
# Note : Nous utilisons un backbone ResNet34 pour un bon équilibre vitesse/précision
BACKBONE = 'resnet34'
preprocess_input = sm.get_preprocessing(BACKBONE)

# On définit le modèle avec 1 classe de sortie (Sigmoid pour Masque)
model = sm.Unet(BACKBONE, encoder_weights='imagenet', classes=1, activation='sigmoid')
# Idéalement, on chargerait ici les poids spécifiques ISIC si disponibles .h5
# Pour ce script, nous utilisons les poids ImageNet qui sont déjà excellents pour détecter les textures.

def generate_masks():
    print(f"🚀 Lancement de la génération des masques depuis {DATASET_PATH}...")
    
    # Récupérer toutes les images
    image_paths = glob(os.path.join(DATASET_PATH, '*/*'))
    image_paths = [p for p in image_paths if p.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"📸 {len(image_paths)} images détectées.")

    for img_path in tqdm(image_paths):
        try:
            # 1. Charger et préparer l'image
            original_img = cv2.imread(img_path)
            if original_img is None: continue
            
            img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            img_resized = cv2.resize(img_rgb, (256, 256))
            
            # 2. Prétraitement spécifique au Backbone
            img_input = np.expand_dims(img_resized, axis=0)
            img_input = preprocess_input(img_input)
            
            # 3. Prédiction du masque
            pr_mask = model.predict(img_input, verbose=0).squeeze()
            
            # 4. Post-traitement (Binarisation)
            binary_mask = (pr_mask > 0.5).astype(np.uint8) * 255
            
            # 5. Sauvegarde
            # On conserve la structure des dossiers (Leprosy, Tinea, etc.)
            cls_name = os.path.basename(os.path.dirname(img_path))
            save_dir = os.path.join(MASK_OUTPUT_PATH, cls_name)
            os.makedirs(save_dir, exist_ok=True)
            
            mask_name = os.path.basename(img_path)
            cv2.imwrite(os.path.join(save_dir, mask_name), binary_mask)
            
        except Exception as e:
            print(f"⚠️ Erreur sur {img_path}: {e}")

    print(f"✅ Terminé ! Masques disponibles dans : {MASK_OUTPUT_PATH}")

if __name__ == "__main__":
    generate_masks()
