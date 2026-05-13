import os
import sys
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetV2L
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    ModelCheckpoint, 
    EarlyStopping, 
    ReduceLROnPlateau
)

# Ajout du chemin racine pour supporter l'exécution sur Colab/Kaggle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.core.processor import LABELS, IMG_SIZE

# Configuration de l'entraînement
BATCH_SIZE = 8
EPOCHS = 50
DATASET_PATH = "datasets-cutisia"

def build_elite_model(num_classes):
    """
    Construit l'architecture du modèle Elite basée sur EfficientNetV2-L.
    Applique le Transfer Learning avec les poids ImageNet.
    """
    base_model = EfficientNetV2L(
        weights='imagenet', 
        include_top=False, 
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)
    )
    
    # On commence par geler la base pour entraîner uniquement la nouvelle tête
    base_model.trainable = False
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.4)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    return model, base_model

def prepare_datasets():
    """
    Charge et prépare les générateurs de données avec augmentation.
    """
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    train_generator = datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )
    
    val_generator = datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )
    
    return train_generator, val_generator

def train():
    """
    Lance le cycle complet d'entraînement : Warm-up puis Fine-tuning.
    """
    if not os.path.exists(DATASET_PATH):
        print(f"Erreur : Dataset introuvable à {DATASET_PATH}")
        return

    train_gen, val_gen = prepare_datasets()
    model, base_model = build_elite_model(len(LABELS))
    
    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Callbacks
    checkpoint = ModelCheckpoint(
        "cutisia_heavy_elite.h5", 
        monitor='val_accuracy', 
        save_best_only=True, 
        mode='max'
    )
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-7)
    
    print("Début de la Phase 1 : Entraînement de la tête (Warm-up)")
    model.fit(
        train_gen,
        epochs=5,
        validation_data=val_gen,
        callbacks=[checkpoint, early_stop, reduce_lr]
    )
    
    print("Début de la Phase 2 : Fine-tuning (Dégel partiel)")
    base_model.trainable = True
    # On ne dégèle que les 50 dernières couches pour la finesse du diagnostic
    for layer in base_model.layers[:-50]:
        layer.trainable = False
        
    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[checkpoint, early_stop, reduce_lr]
    )
    
    print("Entraînement terminé. Modèle sauvegardé.")

if __name__ == "__main__":
    train()
