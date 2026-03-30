import os
import shutil
import re
from pathlib import Path

# Configuration
BASE_DIR = Path("/home/franck/Documents/M2 OCC 2026/smart DATA-CITY/projet3")
TARGET_BASE = BASE_DIR / "datasets-cutisia"

# Liste des dossiers à ignorer (Trop sale)
IGNORED_PATHS = [
    "dataset-2/train/Scabies Lyme Disease and other Infestations and Bites"
]

# Mapping des dossiers vers les classes finales
# Format: { "Classe_Cible": ["Chemin/Vers/Source1", "Chemin/Vers/Source2"] }
MAPPING = {
    "Leprosy": [
        "datasets/leprosy",
        "CO2Wounds-V2 Extended Chronic Wounds Dataset From Leprosy Patients/imgs"
    ],
    "Scabies": [
        "Raw_Dataset/sc_Scabies_sarna",
        "dataset-2/test/Scabies Lyme Disease and other Infestations and Bites",
        "skindiseasedataset/SkinDisease/SkinDisease/train/Infestations_Bites",
        "skindiseasedataset/SkinDisease/SkinDisease/test/Infestations_Bites"
    ],
    "Monkeypox": [
        "datasets/mk_Monkeypox",
        "Raw_Dataset/mk_Monkeypox"
    ],
    "Tinea": [
        "skindiseasedataset/SkinDisease/SkinDisease/train/Tinea",
        "skindiseasedataset/SkinDisease/SkinDisease/test/Tinea",
        "dataset-2/train/Tinea Ringworm Candidiasis and other Fungal Infections",
        "dataset-2/test/Tinea Ringworm Candidiasis and other Fungal Infections"
    ],
    "Candidiase": [
        "skindiseasedataset/SkinDisease/SkinDisease/train/Candidiasis",
        "skindiseasedataset/SkinDisease/SkinDisease/test/Candidiasis",
        "dataset-2/train/Tinea Ringworm Candidiasis and other Fungal Infections",
        "dataset-2/test/Tinea Ringworm Candidiasis and other Fungal Infections"
    ],
    "Mélanomes": [
        "datasets/me_Melanoma",
        "Raw_Dataset/me_Melanoma",
        "dataset-2/train/Melanoma Skin Cancer Nevi and Moles",
        "dataset-2/test/Melanoma Skin Cancer Nevi and Moles",
        "skindiseasedataset/SkinDisease/SkinDisease/train/SkinCancer",
        "skindiseasedataset/SkinDisease/SkinDisease/test/SkinCancer",
        "skindiseasedataset/SkinDisease/SkinDisease/train/Moles",
        "skindiseasedataset/SkinDisease/SkinDisease/test/Moles"
    ]
}

# Dossiers hybrides nécessitant un tri par REGEX
HYBRID_FOLDERS = [
    "dataset-2/train/Cellulitis Impetigo and other Bacterial Infections",
    "dataset-2/test/Cellulitis Impetigo and other Bacterial Infections"
]

# Regex de tri pour les dossiers hybrides
REGEX_RULES = {
    "Cellulite": r"cellulit|09cellulitis",
    "Impétigo": r"impetigo"
}

def migrate():
    print("🚀 Démarrage de la migration intelligente...")
    
    # 1. Traitement des classes standards
    for target_class, sources in MAPPING.items():
        target_dir = TARGET_BASE / target_class
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for source_rel in sources:
            if source_rel in IGNORED_PATHS:
                print(f"⚠️  Ignoré (Dossier sale) : {source_rel}")
                continue
                
            source_dir = BASE_DIR / source_rel
            if not source_dir.exists():
                print(f"❌ Dossier source inexistant : {source_dir}")
                continue
                
            print(f"📦 Traitement de {target_class} depuis {source_rel}...")
            
            for file in source_dir.iterdir():
                if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    # Renommage pour éviter les collisions : source_filename
                    safe_source_name = source_rel.replace("/", "_").replace(" ", "_")
                    new_name = f"{safe_source_name}_{file.name}"
                    target_file = target_dir / new_name
                    
                    # Sécurité : Supprimer si le lien ou le fichier existe déjà
                    if target_file.exists() or target_file.is_symlink():
                        target_file.unlink()
                        
                    # DÉPLACEMENT PHYSIQUE (Aucun espace supplémentaire sur même partition)
                    shutil.move(str(file.absolute()), str(target_file))

    # 2. Traitement des dossiers hybrides (Cellulite / Impétigo)
    for hybrid_rel in HYBRID_FOLDERS:
        source_dir = BASE_DIR / hybrid_rel
        if not source_dir.exists():
            continue
            
        print(f"🔍 Tri intelligent du dossier hybride : {hybrid_rel}...")
        
        for file in source_dir.iterdir():
            if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                matched = False
                for target_class, pattern in REGEX_RULES.items():
                    if re.search(pattern, file.name, re.IGNORECASE):
                        target_dir = TARGET_BASE / target_class
                        target_dir.mkdir(parents=True, exist_ok=True)
                        
                        safe_source_name = hybrid_rel.replace("/", "_").replace(" ", "_")
                        new_name = f"{safe_source_name}_{file.name}"
                        target_file = target_dir / new_name
                        
                        if target_file.exists() or target_file.is_symlink():
                            target_file.unlink()
                            
                        # DÉPLACEMENT PHYSIQUE
                        shutil.move(str(file.absolute()), str(target_file))
                        matched = True
                        break
                
                if not matched:
                    # Optionnel: loguer les fichiers non classés
                    pass

    print("\n✅ Migration terminée avec succès !")

if __name__ == "__main__":
    migrate()
