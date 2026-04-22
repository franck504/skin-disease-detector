import os
import io
import uvicorn
import json
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import nest_asyncio
import cv2

# --- CONFIGURATION ---
IMG_SIZE = (384, 384)
PORT = 8000

# Labels hardcodés (ordre alphabétique = ordre du modèle)
LABELS = ['Candidiase', 'Leprosy', 'Mélanomes', 'Monkeypox', 'Scabies', 'Tinea']

# Détection auto du modèle : Drive Colab > local
DRIVE_PATHS = [
    '/content/drive/MyDrive/Cutisia_Elite_AI_Models/best_cutisia_v2L.h5',
    '/content/drive/MyDrive/Cutisia_Elite_AI_Models/cutisia_heavy_elite.h5',
]
MODEL_PATH = 'cutisia_heavy_elite.h5'  # Fallback local
for path in DRIVE_PATHS:
    if os.path.exists(path):
        MODEL_PATH = path
        print(f"📡 Modèle ELITE chargé depuis Google Drive : {MODEL_PATH}")
        break

# Lecture sécurisée du Token Ngrok (priorité à la variable d'environnement)
NGROK_AUTHTOKEN = os.getenv("NGROK_AUTHTOKEN", "VOTRE_AUTHTOKEN_NGROK")

# --- INITIALISATION ---
app = FastAPI(title="Cutisia API - Skin Disease Detection")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Chargement du modèle
try:
    model = load_model(MODEL_PATH)
    print(f"✅ Modèle chargé avec succès : {MODEL_PATH}")
except:
    print(f"❌ Erreur : Modèle {MODEL_PATH} introuvable. Entraînez-le d'abord.")

def equalize_derma(img):
    """Égalisation adaptative (CLAHE) identique à l'entraînement"""
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    return img

def preprocess_image(image: Image.Image):
    # 1. Conversion en array et redimensionnement
    img = np.array(image.convert('RGB'))
    img = cv2.resize(img, IMG_SIZE)
    # 2. Application de l'égalisation CLAHE
    img = equalize_derma(img)
    # 3. Normalisation
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Dossier de collecte sur Google Drive
COLLECT_DIR = "/content/drive/MyDrive/new_cutisia_images"
if not os.path.exists(COLLECT_DIR):
    try:
        os.makedirs(COLLECT_DIR)
        print(f"📁 Dossier de collecte créé : {COLLECT_DIR}")
    except:
        # Fallback local si pas sur Colab/Drive
        COLLECT_DIR = "new_cutisia_images"
        if not os.path.exists(COLLECT_DIR): os.makedirs(COLLECT_DIR)

@app.get("/")
def home():
    return {"message": "Serveur Cutisia en ligne", "classes": LABELS}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Lecture de l'image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Prétraitement
    processed_image = preprocess_image(image)
    
    # Prédiction
    predictions = model.predict(processed_image)
    class_idx = np.argmax(predictions[0])
    confidence = float(predictions[0][class_idx])
    
    return {
        "class": LABELS[class_idx],
        "confidence": confidence,
        "results": {LABELS[i]: float(predictions[0][i]) for i in range(len(LABELS))}
    }

@app.post("/collect")
async def collect(
    file: UploadFile = File(...),
    metadata: str = Form(...)
):
    """Reçoit une image et un JSON, les enregistre sur le Drive"""
    try:
        # Création d'un nom unique basé sur le timestamp
        import time
        timestamp = int(time.time() * 1000)
        base_filename = f"collect_{timestamp}"
        
        # 1. Sauvegarde de l'image
        extension = os.path.splitext(file.filename)[1] or ".jpg"
        img_path = os.path.join(COLLECT_DIR, base_filename + extension)
        with open(img_path, "wb") as f:
            f.write(await file.read())
            
        # 2. Sauvegarde des métadonnées JSON
        json_path = os.path.join(COLLECT_DIR, base_filename + ".json")
        metadata_dict = json.loads(metadata)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(metadata_dict, f, ensure_ascii=False, indent=4)
            
        return {
            "status": "success",
            "message": "Données enregistrées sur le Drive",
            "filename": base_filename
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- LANCEMENT NGROK & SERVEUR ---
def start_server():
    ngrok.set_auth_token(NGROK_AUTHTOKEN)
    public_url = ngrok.connect(PORT)
    print(f"\n🌍 URL PUBILQUE NGROK : {public_url}")
    print(f"🔗 Point de terminaison API : {public_url}/predict")
    
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    start_server()
