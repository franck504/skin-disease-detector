import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from tensorflow.keras.models import load_model

# --- CONFIGURATION & AUTO-DETECTION ---
MODEL_NAME = 'cutisia_heavy_elite.h5'
DATA_DIR = 'datasets-cutisia'
SAVE_DIR = 'evaluation_results'
IMG_SIZE = (384, 384)

# Détection de l'environnement et recherche récursive du modèle/données
if os.path.exists('/kaggle/working'):
    MODEL_PATH = os.path.join('/kaggle/working', MODEL_NAME)
    # Sur Kaggle, cherchez dans /kaggle/input/
    dataset_search = glob.glob("/kaggle/input/**/Candidiase", recursive=True)
    DATA_DIR = os.path.dirname(dataset_search[0]) if dataset_search else 'datasets-cutisia'
elif os.path.exists('/content/drive/MyDrive'):
    print("🔍 Recherche du modèle et des données dans Google Drive...")
    import glob
    
    # 1. Recherche du modèle
    model_matches = glob.glob(f"/content/drive/MyDrive/**/{MODEL_NAME}", recursive=True)
    MODEL_PATH = model_matches[0] if model_matches else MODEL_NAME
    if model_matches: print(f"🎯 Modèle trouvé : {MODEL_PATH}")

    # 2. Recherche des données (on cherche le dossier qui contient 'Candidiase')
    data_matches = glob.glob("/content/drive/MyDrive/**/Candidiase", recursive=True)
    if data_matches:
        DATA_DIR = os.path.dirname(data_matches[0])
        print(f"📂 Dossier de données trouvé : {DATA_DIR}")
    else:
        DATA_DIR = 'datasets-cutisia'
else:
    MODEL_PATH = MODEL_NAME
    DATA_DIR = 'datasets-cutisia'

# Vérification finale
if not os.path.exists(MODEL_PATH):
    print(f"⚠️ AVERTISSEMENT : Modèle introuvable.")
if not os.path.exists(DATA_DIR):
    print(f"⚠️ AVERTISSEMENT : Dossier de données {DATA_DIR} introuvable.")

os.makedirs(SAVE_DIR, exist_ok=True)

# --- 1. CHARGEMENT DU MODÈLE ET DES DONNÉES ---
print("⏳ Chargement du modèle...")
model = load_model(MODEL_PATH)

# Récupération des noms de classes (doit être identique à l'entraînement)
classes = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
print(f"✅ Classes détectées : {classes}")

# --- 2. FONCTION GRAD-CAM ---
def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # On crée un modèle qui sort à la fois la dernière couche conv et les prédictions
    grad_model = tf.keras.models.Model(
        inputs=model.inputs, 
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        
        # On s'assure que preds est un tenseur simple
        if isinstance(preds, list):
            preds = preds[0]
            
        if pred_index is None:
            # On récupère l'index de la classe avec la plus haute probabilité
            import numpy as np
            pred_index = np.argmax(preds[0])
            
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
print("🚀 Génération des statistiques globales (Matrice & ROC)...")

# Chargement du dataset pour évaluation
from tensorflow.keras.utils import image_dataset_from_directory

val_ds = image_dataset_from_directory(
    DATA_DIR,
    image_size=IMG_SIZE,
    batch_size=32,
    shuffle=False
)

# Prédictions
y_pred_probs = model.predict(val_ds)
y_true = np.concatenate([y for x, y in val_ds], axis=0)
y_true_indices = y_true # Comme shuffle=False, c'est direct

# En cas d'encodage one-hot
if len(y_true.shape) > 1 and y_true.shape[1] > 1:
    y_true_indices = np.argmax(y_true, axis=1)

# Matrice de confusion
save_confusion_matrix(tf.one_hot(y_true_indices, depth=len(classes)).numpy(), y_pred_probs, classes)

# Courbe ROC (simplifiée pour multi-classe)
plt.figure(figsize=(10, 8))
for i in range(len(classes)):
    fpr, tpr, _ = roc_curve((y_true_indices == i).astype(int), y_pred_probs[:, i])
    plt.plot(fpr, tpr, label=f'ROC {classes[i]} (AUC = {auc(fpr, tpr):.2f})')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('Taux de Faux Positifs')
plt.ylabel('Taux de Vrais Positifs')
plt.title('Courbes AUC-ROC - Cutisia')
plt.legend()
plt.savefig(os.path.join(SAVE_DIR, 'roc_curve.png'))
print("✅ Courbes ROC sauvegardées.")

# Grad-CAM
save_gradcam_sample(model, classes)

print("\n✨ TOUT EST PRÊT ! Récupérez vos PNG dans 'evaluation_results'.")
