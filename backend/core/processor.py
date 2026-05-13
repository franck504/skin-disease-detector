import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# --- CONFIGURATION DES FRAMEWORKS ---
# Patch pour assurer la compatibilité entre Keras et segmentation-models
import keras
class GenericUtilsStub:
    def get_custom_objects(self):
        try: return keras.saving.get_custom_objects()
        except: return {}
if not hasattr(keras.utils, 'generic_utils'):
    keras.utils.generic_utils = GenericUtilsStub()
os.environ['SM_FRAMEWORK'] = 'tf.keras'
import segmentation_models as sm

# Paramètres globaux
IMG_SIZE = (384, 384)
UNET_SIZE = (256, 256)
LABELS = ['Candidiase', 'Leprosy', 'Monkeypox', 'Mélanomes', 'Scabies', 'Tinea']

def equalize_derma(img):
    """
    Applique l'égalisation adaptative de l'histogramme (CLAHE) pour normaliser
    le contraste des images dermatologiques.
    """
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

def load_unet_model():
    """
    Initialise et charge le modèle U-Net pour la segmentation des lésions.
    Utilise un backbone ResNet34 pré-entraîné.
    """
    backbone = 'resnet34'
    preprocess_input = sm.get_preprocessing(backbone)
    model = sm.Unet(backbone, encoder_weights='imagenet', classes=1, activation='sigmoid')
    return model, preprocess_input

def segment_and_crop(img_rgb, unet_model, unet_preprocess):
    """
    Isoler la lésion cutanée en utilisant le modèle U-Net et rogne l'image 
    autour de la zone détectée.
    """
    h, w = img_rgb.shape[:2]
    # Redimensionnement pour l'entrée U-Net
    img_small = cv2.resize(img_rgb, UNET_SIZE)
    img_input = np.expand_dims(img_small, axis=0)
    img_input = unet_preprocess(img_input)
    
    # Prédiction du masque
    pr_mask = unet_model.predict(img_input, verbose=0).squeeze()
    binary_mask = (pr_mask > 0.5).astype(np.uint8) * 255
    
    # Redimensionnement du masque à la taille originale
    full_mask = cv2.resize(binary_mask, (w, h))
    
    # Détermination des coordonnées de rognage
    coords = np.where(full_mask > 0)
    if len(coords[0]) == 0:
        return img_rgb # Retourne l'image entière si aucune lésion n'est détectée
        
    y0, x0 = coords[0].min(), coords[1].min()
    y1, x1 = coords[0].max(), coords[1].max()
    
    return img_rgb[y0:y1, x0:x1]

def preprocess_for_classification(image_pil, unet_model, unet_preprocess):
    """
    Chaîne complète de prétraitement : Segmentation -> Crop -> Resize -> CLAHE -> Normalisation.
    """
    # 1. Conversion en tableau NumPy
    img = np.array(image_pil.convert('RGB'))
    
    # 2. Segmentation et rognage
    img = segment_and_crop(img, unet_model, unet_preprocess)
    
    # 3. Redimensionnement final
    img = cv2.resize(img, IMG_SIZE)
    
    # 4. Amélioration du contraste
    img = equalize_derma(img)
    
    # 5. Normalisation et mise en forme pour le modèle
    img = img.astype(np.float32) / 255.0
    return np.expand_dims(img, axis=0)
