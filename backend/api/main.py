import os
import sys
import io
import time
import json
import uvicorn
import numpy as np
from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
from dotenv import load_dotenv

# Ajout du chemin racine pour supporter l'exécution sur Colab/Kaggle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importations locales
from backend.core.processor import (
    preprocess_for_classification, 
    load_unet_model, 
    LABELS
)
from tensorflow.keras.models import load_model

# Chargement des variables d'environnement
load_dotenv()

# --- CONFIGURATION ---
PORT = int(os.getenv("API_PORT", 8000))
MODEL_PATH = os.getenv("MODEL_PATH", "cutisia_heavy_elite.h5")
NGROK_AUTHTOKEN = os.getenv("NGROK_AUTHTOKEN", "")
COLLECT_DIR = os.getenv("COLLECT_DIR", "collected_data")

# --- INITIALISATION ---
app = FastAPI(title="Cutisia API - Système de Détection Dermatologique")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement des modèles au démarrage
try:
    print(f"Chargement du modèle de classification : {MODEL_PATH}")
    classification_model = load_model(MODEL_PATH)
    
    print("Initialisation du modèle de segmentation U-Net...")
    unet_model, unet_preprocess = load_unet_model()
    
    print("Modèles prêts pour l'inférence.")
except Exception as e:
    print(f"Erreur lors du chargement des modèles : {str(e)}")
    # On ne lève pas d'exception ici pour permettre au serveur de démarrer 
    # et de renvoyer des erreurs explicites lors des requêtes.

# Création du dossier de collecte
os.makedirs(COLLECT_DIR, exist_ok=True)

@app.get("/")
def read_root():
    """Vérification de l'état du serveur."""
    return {
        "status": "online",
        "message": "Le serveur Cutisia est opérationnel",
        "supported_classes": LABELS
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint principal pour la prédiction. 
    Prend une image en entrée et renvoie la classe détectée.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier fourni n'est pas une image.")

    try:
        # Lecture et prétraitement
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        input_data = preprocess_for_classification(image, unet_model, unet_preprocess)
        
        # Inférence
        predictions = classification_model.predict(input_data, verbose=0)
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        
        return {
            "class": LABELS[class_idx],
            "confidence": confidence,
            "all_predictions": {
                LABELS[i]: float(predictions[0][i]) for i in range(len(LABELS))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement : {str(e)}")

@app.post("/collect")
async def collect(
    file: UploadFile = File(...),
    metadata: str = Form(...)
):
    """
    Permet de collecter des données terrain pour améliorer le modèle futur.
    Enregistre l'image et ses métadonnées JSON.
    """
    try:
        timestamp = int(time.time() * 1000)
        filename_base = f"capture_{timestamp}"
        
        # Sauvegarde de l'image
        ext = os.path.splitext(file.filename)[1] or ".jpg"
        image_path = os.path.join(COLLECT_DIR, f"{filename_base}{ext}")
        with open(image_path, "wb") as f:
            f.write(await file.read())
            
        # Sauvegarde des métadonnées
        meta_path = os.path.join(COLLECT_DIR, f"{filename_base}.json")
        meta_dict = json.loads(metadata)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta_dict, f, indent=4, ensure_ascii=False)
            
        return {"status": "success", "id": filename_base}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Échec de la collecte : {str(e)}")

def start():
    """Démarre le serveur avec Ngrok si un token est fourni."""
    if NGROK_AUTHTOKEN:
        ngrok.set_auth_token(NGROK_AUTHTOKEN)
        public_url = ngrok.connect(PORT)
        print(f"Tunnel public disponible : {public_url}")
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    start()
