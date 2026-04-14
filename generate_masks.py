import os
import sys

# --- PATCH UNIVERSEL KERAS 3 (TF 2.16+) ---
import tensorflow as tf
import keras

# Création d'un objet factice pour simuler generic_utils
class GenericUtilsStub:
    def get_custom_objects(self):
        # Redirection vers le nouveau système de Keras 3
        try:
            return keras.saving.get_custom_objects()
        except:
            return {}

if not hasattr(keras.utils, 'generic_utils'):
    keras.utils.generic_utils = GenericUtilsStub()
    print("🔧 Patch Keras 3 (Object-based) appliqué.")

os.environ['SM_FRAMEWORK'] = 'tf.keras'

try:
    import segmentation_models as sm
except ImportError:
    print("📦 Installation de segmentation-models...")
    os.system('pip install -U segmentation-models')
    import segmentation_models as sm

import numpy as np
import cv2
from glob import glob
from tqdm import tqdm

# --- DÉTECTION DU DOSSIER DATASET ---
def find_dataset_path(base_name):
    # Les chemins prioritaires sur Colab
    possible_paths = [
        '/kaggle/input/cutisiav2/datasets-cutisia',
        '/content/drive/MyDrive/cutisia_datasets',
        '/content/skin-disease-detector/datasets-cutisia',
        'datasets-cutisia'
    ]
    for p in possible_paths:
        if os.path.exists(p):
            return p
    return None

DATASET_PATH = find_dataset_path('datasets-cutisia')
if not DATASET_PATH:
    print("❌ Dossier dataset introuvable.")
    sys.exit(1)

print(f"📌 Dataset : {DATASET_PATH}")

MASK_OUTPUT_PATH = '/content/drive/MyDrive/cutisia_masks'
if os.path.exists('/kaggle'):
    print("💎 Environnement KAGGLE détecté.")
    MASK_OUTPUT_PATH = '/kaggle/working/cutisia_masks'
elif not os.path.exists('/content/drive/MyDrive'):
    MASK_OUTPUT_PATH = './cutisia_masks'

os.makedirs(MASK_OUTPUT_PATH, exist_ok=True)

# --- MODELE U-NET ---
BACKBONE = 'resnet34'
preprocess_input = sm.get_preprocessing(BACKBONE)
model = sm.Unet(BACKBONE, encoder_weights='imagenet', classes=1, activation='sigmoid')

def generate_masks():
    image_paths = glob(os.path.join(DATASET_PATH, '*/*'))
    image_paths = [p for p in image_paths if p.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"📸 Traitement de {len(image_paths)} images...")

    for img_path in tqdm(image_paths):
        try:
            original_img = cv2.imread(img_path)
            if original_img is None: continue
            
            img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
            h, w = img_rgb.shape[:2]
            
            img_resized = cv2.resize(img_rgb, (256, 256))
            img_input = np.expand_dims(img_resized, axis=0)
            img_input = preprocess_input(img_input)
            
            pr_mask = model.predict(img_input, verbose=0).squeeze()
            
            binary_mask = (pr_mask > 0.5).astype(np.uint8) * 255
            final_mask = cv2.resize(binary_mask, (w, h))
            
            cls_name = os.path.basename(os.path.dirname(img_path))
            save_dir = os.path.join(MASK_OUTPUT_PATH, cls_name)
            os.makedirs(save_dir, exist_ok=True)
            
            mask_name = os.path.basename(img_path)
            cv2.imwrite(os.path.join(save_dir, mask_name), final_mask)
            
        except Exception:
            pass

    print(f"✅ Terminé : {MASK_OUTPUT_PATH}")

if __name__ == "__main__":
    generate_masks()
