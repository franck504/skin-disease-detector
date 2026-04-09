import os
import io
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import nest_asyncio

# --- CONFIGURATION ---
MODEL_PATH = 'cutisia_heavy_server.h5'
# Détection auto du modèle sur Drive pour Colab
drive_model_path = '/content/drive/MyDrive/cutisia_models/cutisia_heavy_server.h5'
if os.path.exists(drive_model_path):
    MODEL_PATH = drive_model_path
    print(f"📡 Modèle chargé depuis Google Drive : {MODEL_PATH}")

LABELS = sorted(os.listdir('datasets-cutisia'))  # Ordre alphabétique des classes
PORT = 8000

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

def preprocess_image(image: Image.Image):
    image = image.convert("RGB")
    image = image.resize((224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0  # Normalisation (Identique à l'entraînement)
    return image

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
