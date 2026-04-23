import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from tensorflow.keras.models import load_model

# --- CONFIGURATION ---
MODEL_PATH = 'cutisia_heavy_elite.h5' # Ou 'best_cutisia_v2L.h5'
DATA_DIR = 'datasets-cutisia'
SAVE_DIR = 'evaluation_results'
IMG_SIZE = (384, 384)

os.makedirs(SAVE_DIR, exist_ok=True)

# --- 1. CHARGEMENT DU MODÈLE ET DES DONNÉES ---
print("⏳ Chargement du modèle...")
model = load_model(MODEL_PATH)

# Récupération des noms de classes (doit être identique à l'entraînement)
classes = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
print(f"✅ Classes détectées : {classes}")

# --- 2. FONCTION GRAD-CAM ---
def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.reduce_max(heatmap)
    return heatmap.numpy()

# --- 3. ÉVALUATION ET MATRICE ---
print("📊 Évaluation en cours...")
# On charge un petit échantillon pour la démo ou tout le dossier test
# Ici on simule une évaluation sur un dataset de test
# (Dans un vrai notebook, utilisez votre val_ds)

# Supposons que y_true et y_pred sont obtenus via model.predict(val_ds)
# y_pred = model.predict(val_ds)
# y_true = ...

# Génération d'une fausse matrice pour l'exemple de structure si pas de données
# Mais sur Kaggle, vous lancerez le vrai calcul.

def save_confusion_matrix(y_true, y_pred, classes):
    cm = confusion_matrix(np.argmax(y_true, axis=1), np.argmax(y_pred, axis=1))
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Matrice de Confusion - Cutisia Elite')
    plt.ylabel('Réalité')
    plt.xlabel('Prédiction')
    plt.savefig(os.path.join(SAVE_DIR, 'confusion_matrix.png'))
    print("✅ Matrice de confusion sauvegardée.")

# --- 4. VISUALISATION GRAD-CAM SUR UN EXEMPLE RÉEL ---
def save_gradcam_sample(model, classes):
    # On cherche la première image disponible dans le dataset
    sample_img_path = None
    for cls in classes:
        cls_p = os.path.join(DATA_DIR, cls)
        imgs = [f for f in os.listdir(cls_p) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if imgs:
            sample_img_path = os.path.join(cls_p, imgs[0])
            break
    
    if not sample_img_path:
        print("❌ Aucune image trouvée pour Grad-CAM.")
        return

    img = cv2.imread(sample_img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_res = cv2.resize(img_rgb, IMG_SIZE)
    img_array = np.expand_dims(img_res, axis=0) / 255.0

    # Nom de la dernière couche de convolution pour EfficientNetV2L
    last_conv = "top_activation" 
    
    heatmap = make_gradcam_heatmap(img_array, model, last_conv)
    
    # Superposition
    heatmap_res = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap_res = np.uint8(255 * heatmap_res)
    heatmap_res = cv2.applyColorMap(heatmap_res, cv2.COLORMAP_JET)
    
    superimposed_img = cv2.addWeighted(img, 0.6, heatmap_res, 0.4, 0)
    
    output_path = os.path.join(SAVE_DIR, 'gradcam_sample.png')
    cv2.imwrite(output_path, superimposed_img)
    print(f"✅ Grad-CAM sauvegardé dans {output_path} (utilisant {sample_img_path})")

# --- 5. EXECUTION FINALE ---
# Ici on appelle les fonctions
# Dans votre cas réel, passez vos vrais y_true et y_pred
# y_pred = model.predict(val_ds) 

save_gradcam_sample(model, classes)

print("\n✨ Terminé ! Récupérez vos images dans le dossier 'evaluation_results'.")
