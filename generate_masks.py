import os
import sys

# --- PATCH DE COMPATIBILITÉ KERAS 3 / TF 2.18 ---
# Ce patch corrige l'erreur 'AttributeError: module keras.utils has no attribute generic_utils'
import tensorflow as tf
import keras
if not hasattr(keras.utils, 'generic_utils'):
    import keras.src.utils.generic_utils as generic_utils
    keras.utils.generic_utils = generic_utils
    print("🔧 Patch Keras generic_utils appliqué.")

os.environ['SM_FRAMEWORK'] = 'tf.keras'

try:
    import segmentation_models as sm
except ImportError:
    print("📦 Installation de segmentation-models...")
    # On installe sans h5py imposé pour éviter les conflits Python 3.12
    os.system('pip install -U segmentation-models')
    import segmentation_models as sm

import numpy as np
import cv2
from glob import glob
from tqdm import tqdm

# --- DÉTECTION ROBUSTE DU DOSSIER DATASET ---
def find_dataset_path(base_name):
    possible_roots = ['/content', '/content/skin-disease-detector', os.getcwd()]
    for root in possible_roots:
        # Recherche récursive du dossier
        for dirpath, dirnames, filenames in os.walk(root):
            if base_name in dirnames:
                return os.path.join(dirpath, base_name)
    return None

DATASET_PATH = find_dataset_path('datasets-cutisia')
if not DATASET_PATH:
    print("❌ ERREUR : Le dossier 'datasets-cutisia' est introuvable sur le disque.")
    print(f"DEBUG: Dossier actuel : {os.getcwd()}")
    print(f"DEBUG: Contenu : {os.listdir('.')}")
    sys.exit(1)

print(f"📌 Dataset trouvé à : {DATASET_PATH}")

MASK_OUTPUT_PATH = '/content/drive/MyDrive/cutisia_masks'
if not os.path.exists('/content/drive/MyDrive'):
    MASK_OUTPUT_PATH = './cutisia_masks'

os.makedirs(MASK_OUTPUT_PATH, exist_ok=True)

# --- CHARGEMENT DU MODELE U-NET ---
BACKBONE = 'resnet34'
preprocess_input = sm.get_preprocessing(BACKBONE)
model = sm.Unet(BACKBONE, encoder_weights='imagenet', classes=1, activation='sigmoid')

def generate_masks():
    image_paths = glob(os.path.join(DATASET_PATH, '*/*'))
    image_paths = [p for p in image_paths if p.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"📸 {len(image_paths)} images à traiter.")

    for img_path in tqdm(image_paths):
        try:
            original_img = cv2.imread(img_path)
            if original_img is None: continue
            
            img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            h, w = img_rgb.shape[:2]
            
            # Prediction on 256x256
            img_resized = cv2.resize(img_rgb, (256, 256))
            img_input = np.expand_dims(img_resized, axis=0)
            img_input = preprocess_input(img_input)
            
            pr_mask = model.predict(img_input, verbose=0).squeeze()
            
            # Resize mask back to original size for perfect crop later
            binary_mask = (pr_mask > 0.5).astype(np.uint8) * 255
            final_mask = cv2.resize(binary_mask, (w, h))
            
            cls_name = os.path.basename(os.path.dirname(img_path))
            save_dir = os.path.join(MASK_OUTPUT_PATH, cls_name)
            os.makedirs(save_dir, exist_ok=True)
            
            mask_name = os.path.basename(img_path)
            cv2.imwrite(os.path.join(save_dir, mask_name), final_mask)
            
        except Exception as e:
            pass

    print(f"✅ Masques générés dans : {MASK_OUTPUT_PATH}")

if __name__ == "__main__":
    generate_masks()
