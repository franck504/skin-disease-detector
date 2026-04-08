import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetV2B0, MobileNetV3Large
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
DATA_DIR = 'datasets-cutisia'

# Détection automatique pour Google Colab
if not os.path.exists(DATA_DIR):
    colab_drive_path = '/content/drive/MyDrive/datasets-cutisia'
    if os.path.exists(colab_drive_path):
        DATA_DIR = colab_drive_path
        print(f"📌 Dataset détecté sur Google Drive : {DATA_DIR}")
    else:
        print(f"❌ Erreur : Le dossier '{DATA_DIR}' est introuvable localement et sur le Drive.")
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
NUM_CLASSES = len(os.listdir(DATA_DIR))

def build_model(base_model_func, name):
    base_model = base_model_func(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False  # Freeze local layers initially
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(NUM_CLASSES, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions, name=name)
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

print(f"🚀 Préparation de l'entraînement pour {NUM_CLASSES} classes...")

# --- DATA AUGMENTATION ---
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2  # 20% pour le test
)

train_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# --- ENTRAINEMENT MODELE LOURD (EfficientNetV2) ---
print("\n📦 Entraînement du modèle LOURD (Serveur/Cloud)...")
heavy_model = build_model(EfficientNetV2B0, "EfficientNetV2_Server")
heavy_history = heavy_model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)
heavy_model.save('cutisia_heavy_server.h5')

# --- ENTRAINEMENT MODELE LEGER (MobileNetV3) ---
print("\n📱 Entraînement du modèle LEGER (Mobile/Flutter)...")
mobile_model = build_model(MobileNetV3Large, "MobileNetV3_App")
mobile_history = mobile_model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)
mobile_model.save('cutisia_mobile.h5')

# --- CONVERSION TFLITE POUR MOBILE ---
print("\n🔄 Conversion vers TensorFlow Lite...")
converter = tf.lite.TFLiteConverter.from_keras_model(mobile_model)
tflite_model = converter.convert()
with open('cutisia_mobile.tflite', 'wb') as f:
    f.write(tflite_model)

print("\n✅ Tous les modèles ont été sauvegardés !")
print("- cutisia_heavy_server.h5 (Pour le serveur API)")
print("- cutisia_mobile.tflite (Pour l'application Flutter)")
