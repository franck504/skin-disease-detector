import json
import os

def update_master_notebook(notebook_path="Cutisia_Master.ipynb"):
    """
    Met à jour la cellule de lancement de l'API dans le notebook Master.
    Cela permet d'assurer que le code de démonstration sur Colab est 
    toujours à jour avec les dernières routes API.
    """
    if not os.path.exists(notebook_path):
        print(f"Le notebook {notebook_path} est introuvable.")
        return

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # La cellule A3 est à l'index 7 (vérifié précédemment)
    new_source = [
        "# === ÉTAPE A3 : Lancement du serveur FastAPI + Ngrok ===\n",
        "import io\n",
        "import os\n",
        "import cv2\n",
        "import json\n",
        "import time\n",
        "import uvicorn\n",
        "import nest_asyncio\n",
        "from PIL import Image\n",
        "from fastapi import FastAPI, UploadFile, File, Form\n",
        "from fastapi.middleware.cors import CORSMiddleware\n",
        "from pyngrok import ngrok\n",
        "\n",
        "# --- CONFIGURATION ---\n",
        "LABELS = ['Candidiase', 'Leprosy', 'Monkeypox', 'Mélanomes', 'Scabies', 'Tinea']\n",
        "IMG_SIZE = (384, 384)\n",
        "PORT = 8000\n",
        "NGROK_TOKEN = '3BlAngRylGIHjrS1492IQM3yT0C_7ocjnd4T6TrZzMLH2HmuE'\n",
        "COLLECT_DIR = '/content/drive/MyDrive/new_cutisia_images'\n",
        "\n",
        "if not os.path.exists(COLLECT_DIR):\n",
        "    try:\n",
        "        os.makedirs(COLLECT_DIR)\n",
        "        print(f'Dossier de collecte créé : {COLLECT_DIR}')\n",
        "    except:\n",
        "        print('Impossible de créer le dossier sur Drive, utilisation locale.')\n",
        "        COLLECT_DIR = 'new_cutisia_images'\n",
        "        if not os.path.exists(COLLECT_DIR): os.makedirs(COLLECT_DIR)\n",
        "\n",
        "# --- PRÉTRAITEMENT ---\n",
        "def equalize_derma(img):\n",
        "    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)\n",
        "    l, a, b = cv2.split(lab)\n",
        "    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))\n",
        "    l = clahe.apply(l)\n",
        "    lab = cv2.merge((l, a, b))\n",
        "    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)\n",
        "\n",
        "def preprocess_image(image):\n",
        "    img = np.array(image.convert('RGB'))\n",
        "    img = cv2.resize(img, IMG_SIZE)\n",
        "    img = equalize_derma(img)\n",
        "    img = img.astype(np.float32) / 255.0\n",
        "    return np.expand_dims(img, axis=0)\n",
        "\n",
        "# --- API ---\n",
        "app = FastAPI(title='Cutisia Elite API')\n",
        "app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])\n",
        "\n",
        "@app.get('/')\n",
        "def home():\n",
        "    return {'status': 'online', 'model': 'EfficientNetV2-L', 'classes': LABELS}\n",
        "\n",
        "@app.post('/predict')\n",
        "async def predict(file: UploadFile = File(...)):\n",
        "    contents = await file.read()\n",
        "    image = Image.open(io.BytesIO(contents))\n",
        "    processed = preprocess_image(image)\n",
        "    predictions = model.predict(processed)\n",
        "    idx = int(np.argmax(predictions[0]))\n",
        "    return {\n",
        "        'class': LABELS[idx],\n",
        "        'confidence': float(predictions[0][idx]),\n",
        "        'results': {LABELS[i]: float(predictions[0][i]) for i in range(len(LABELS))}\n",
        "    }\n",
        "\n",
        "# --- LANCEMENT ---\n",
        "ngrok.set_auth_token(NGROK_TOKEN)\n",
        "tunnel = ngrok.connect(PORT)\n",
        "public_url = tunnel.public_url\n",
        "\n",
        "print('CUTISIA ELITE AI - SERVEUR EN LIGNE')\n",
        "print(f'URL PUBLIQUE : {public_url}')\n",
        "\n",
        "nest_asyncio.apply()\n",
        "config = uvicorn.Config(app, host='0.0.0.0', port=PORT)\n",
        "server = uvicorn.Server(config)\n",
        "await server.serve()"
    ]

    nb['cells'][7]['source'] = new_source

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

    print("Notebook Master mis à jour avec succès.")

if __name__ == "__main__":
    update_master_notebook()
