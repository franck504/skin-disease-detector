# Mapping des Chemins Sources vers les Classes Finales

Ce tableau récapitule les correspondances entre vos **9 classes de destination** (dossiers dans `datasets-cutisia`) et les **chemins des dossiers sources** présents dans vos différentes archives extraites.

⚠️ *Note : Dans certains datasets comme `dataset-2`, plusieurs maladies sont regroupées dans le même dossier (ex : Cellulite et Impétigo, ou Scabies et Bites). Il sera peut-être nécessaire de trier ces dossiers manuellement ou de les copier complètement dans les deux dossiers cibles.*

| Classe Finale ciblée | Chemins des dossiers sources correspondants (Chemins relatifs) |
| :--- | :--- |
| **Leprosy** | - `datasets/leprosy/ ✅OK-selected-moved✅`<br>- `CO2Wounds-V2 Extended Chronic Wounds Dataset From Leprosy Patients/imgs/` |
| **Scabies** | - `Raw_Dataset/sc_Scabies_sarna/`<br>- `dataset-2/train/Scabies Lyme Disease and other Infestations and Bites/` ⚠️ **IGNORÉ (Trop sale)**<br>- `dataset-2/test/Scabies Lyme Disease and other Infestations and Bites/`<br>- `skindiseasedataset/SkinDisease/SkinDisease/train/Infestations_Bites/`<br>- `skindiseasedataset/SkinDisease/SkinDisease/test/Infestations_Bites/` |
| **Monkeypox** | - `datasets/mk_Monkeypox/`<br>- `Raw_Dataset/mk_Monkeypox/` |
| **Tinea** | - `skindiseasedataset/SkinDisease/SkinDisease/train/Tinea/`<br>- `skindiseasedataset/SkinDisease/SkinDisease/test/Tinea/`<br>- `dataset-2/train/Tinea Ringworm Candidiasis and other Fungal Infections/`<br>- `dataset-2/test/Tinea Ringworm Candidiasis and other Fungal Infections/` |
| **Candidiase** | - `skindiseasedataset/SkinDisease/SkinDisease/train/Candidiasis/`<br>- `skindiseasedataset/SkinDisease/SkinDisease/test/Candidiasis/`<br>- `dataset-2/train/Tinea Ringworm Candidiasis and other Fungal Infections/` *(regroupé)*<br>- `dataset-2/test/Tinea Ringworm Candidiasis and other Fungal Infections/` |
| **Mélanomes** | - `datasets/me_Melanoma/`<br>- `Raw_Dataset/me_Melanoma/`<br>- `dataset-2/train/Melanoma Skin Cancer Nevi and Moles/`<br>- `dataset-2/test/Melanoma Skin Cancer Nevi and Moles/`<br>- `skindiseasedataset/SkinDisease/SkinDisease/train/SkinCancer/`<br>- `skindiseasedataset/SkinDisease/SkinDisease/test/SkinCancer/`<br>- `skindiseasedataset/SkinDisease/SkinDisease/train/Moles/`<br>- `skindiseasedataset/SkinDisease/SkinDisease/test/Moles/`<br>*- Images de `HAM10000_images` étiquetées 'mel' ou 'nv' via son fichier CSV* |
