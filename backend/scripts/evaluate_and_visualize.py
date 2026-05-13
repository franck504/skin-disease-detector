import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import load_model

# Ajout du chemin racine pour supporter l'exécution sur Colab/Kaggle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.core.processor import LABELS, IMG_SIZE, equalize_derma
import tensorflow as tf

def evaluate_model(model_path="cutisia_heavy_elite.h5", test_path="datasets-cutisia"):
    """
    Évalue les performances du modèle sur le jeu de données et génère 
    une matrice de confusion ainsi qu'un rapport détaillé.
    """
    if not os.path.exists(model_path):
        print(f"Erreur : Modèle {model_path} introuvable.")
        return

    print(f"Chargement du modèle pour évaluation : {model_path}")
    model = load_model(model_path)
    
    # Préparation du générateur de test (sans augmentation)
    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        test_path,
        target_size=IMG_SIZE,
        batch_size=1,
        class_mode='categorical',
        shuffle=False
    )
    
    # Prédictions
    print("Calcul des prédictions en cours...")
    y_pred_probs = model.predict(test_generator)
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = test_generator.classes
    
    # Rapport de classification
    print("\nRapport de classification :")
    print(classification_report(y_true, y_pred, target_names=test_generator.class_indices.keys()))
    
    # Matrice de confusion
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=LABELS, yticklabels=LABELS)
    plt.xlabel('Prédiction')
    plt.ylabel('Réalité')
    plt.title('Matrice de Confusion - Cutisia Elite')
    plt.savefig('confusion_matrix.png')
    print("Matrice de confusion sauvegardée sous 'confusion_matrix.png'.")

if __name__ == "__main__":
    evaluate_model()
