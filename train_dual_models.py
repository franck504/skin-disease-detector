import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetV2L
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.model_selection import train_test_split

# --- CONFIGURATION ---
DATA_DIR = 'datasets-cutisia'
MASK_DIR = '/content/drive/MyDrive/cutisia_masks'
SAVE_DIR = '/content/drive/MyDrive/cutisia_models/'

# --- DETECTION AUTO DE L'ENVIRONNEMENT ---
if os.path.exists('/kaggle'):
    print("💎 Environnement KAGGLE détecté.")
    DATA_DIR = '/kaggle/input/datasets/scribeassistant/cutisiav2/cutisia_data/cutisia_datasets'
    MASK_DIR = '/kaggle/input/datasets/scribeassistant/cutisiav2/cutisia_data/cutisia_masks'
    SAVE_DIR = '/kaggle/working/'
elif os.path.exists('/content/drive/MyDrive/cutisia_datasets'):
    print("☁️ Environnement COLAB détecté.")
    DATA_DIR = '/content/drive/MyDrive/cutisia_datasets'
    MASK_DIR = '/content/drive/MyDrive/cutisia_masks'
    SAVE_DIR = '/content/drive/MyDrive/cutisia_models/'

os.makedirs(SAVE_DIR, exist_ok=True)

IMG_SIZE = (384, 384) # Taille optimale pour EfficientNetV2L
BATCH_SIZE = 8       # Réduit pour éviter les erreurs Out of Memory (OOM) avec EfficientNetV2-L
EPOCHS = 50

# --- PRETRAITEMENT MEDICAL (CLAHE + CROP) ---

def equalize_derma(img):
    """Égalisation adaptative (CLAHE) - Proposition de votre amie"""
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    return img

def crop_lesion(image, mask):
    """Découpe l'image sur la zone active du masque"""
    coords = np.where(mask > 0)
    if len(coords[0]) == 0: # Si pas de masque détecté, on garde l'image entière
        return image
    y0, x0 = coords[0].min(), coords[1].min()
    y1, x1 = coords[0].max(), coords[1].max()
    cropped = image[y0:y1, x0:x1]
    return cropped

def process_image(img_path, mask_path):
    """Pipeline complet pour une image individuelle"""
    # Correction TF 2.18 : extraction du numpy avant décodage
    img_path_str = img_path.numpy().decode('utf-8')
    mask_path_str = mask_path.numpy().decode('utf-8')

    img = cv2.imread(img_path_str)
    if img is None:
        return np.zeros((*IMG_SIZE, 3), dtype=np.float32)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Charger le masque si disponible
    if os.path.exists(mask_path_str):
        mask = cv2.imread(mask_path_str, cv2.IMREAD_GRAYSCALE)
        if mask is not None:
            # 1. Crop
            img = crop_lesion(img, mask)
    
    # 2. Resize final
    img = cv2.resize(img, IMG_SIZE)
    # 3. CLAHE
    img = equalize_derma(img)
    # 4. Normalisation
    img = img.astype(np.float32) / 255.0
    return img

# --- PIPELINE TF.DATA (Pour performance optimale) ---

def load_data():
    image_paths = []
    mask_paths = []
    labels = []
    
    classes = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
    class_to_idx = {cls: i for i, cls in enumerate(classes)}
    
    for cls in classes:
        cls_path = os.path.join(DATA_DIR, cls)
        for img_name in os.listdir(cls_path):
            if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_p = os.path.join(cls_path, img_name)
                mask_p = os.path.join(MASK_DIR, cls, img_name)
                
                image_paths.append(img_p)
                mask_paths.append(mask_p)
                # On utilise One-Hot Encoding
                one_hot = np.zeros(len(classes))
                one_hot[class_to_idx[cls]] = 1
                labels.append(one_hot)
                
    return image_paths, mask_paths, np.array(labels), len(classes)

# --- CONSTRUCTION DU MODELE ---

def build_elite_model(num_classes):
    print(f"🏗️ Construction de EfficientNetV2-L pour {num_classes} classes...")
    base_model = EfficientNetV2L(weights='imagenet', include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    base_model.trainable = False # Gelé au début
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.4)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=Adam(learning_rate=1e-4), loss='categorical_crossentropy', metrics=['accuracy'])
    return model, base_model

# --- EXECUTION ---

image_paths, mask_paths, labels, num_classes = load_data()
X_train_img, X_val_img, X_train_mask, X_val_mask, y_train, y_val = train_test_split(
    image_paths, mask_paths, labels, test_size=0.2, random_state=42
)

def tf_map_fn(img_p, mask_p, label):
    [img] = tf.py_function(process_image, [img_p, mask_p], [tf.float32])
    img.set_shape((IMG_SIZE[0], IMG_SIZE[1], 3))
    return img, label

train_ds = tf.data.Dataset.from_tensor_slices((X_train_img, X_train_mask, y_train))
train_ds = train_ds.shuffle(1000).map(tf_map_fn, num_parallel_calls=tf.data.AUTOTUNE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

val_ds = tf.data.Dataset.from_tensor_slices((X_val_img, X_val_mask, y_val))
val_ds = val_ds.map(tf_map_fn, num_parallel_calls=tf.data.AUTOTUNE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

model, base_model = build_elite_model(num_classes)

# Callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=4, min_lr=1e-7),
    ModelCheckpoint(os.path.join(SAVE_DIR, 'best_cutisia_v2L.h5'), save_best_only=True)
]

print("\n🚀 Phase 1 : Entraînement des couches hautes (Warm-up)...")
model.fit(train_ds, validation_data=val_ds, epochs=5, callbacks=callbacks)

print("\n🔓 Phase 2 : Fine-tuning (Dégel des 50 dernières couches)...")
base_model.trainable = True
# On ne gèle pas tout, on laisse les couches de tête libres
for layer in base_model.layers[:-50]:
    layer.trainable = False

model.compile(optimizer=Adam(learning_rate=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=callbacks)

# --- SAUVEGARDE FINALE ---
model.save(os.path.join(SAVE_DIR, 'cutisia_heavy_elite.h5'))
print(f"✅ Modèle ELITE (H5) sauvegardé dans {SAVE_DIR}")

# --- CONVERSION TFLITE POUR MOBILE ---
print("📱 Conversion du modèle pour mobile...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

tflite_path = os.path.join(SAVE_DIR, 'cutisia_mobile.tflite')
with open(tflite_path, 'wb') as f:
    f.write(tflite_model)

print(f"✅ Modèle MOBILE (TFLite) sauvegardé dans {SAVE_DIR}")
