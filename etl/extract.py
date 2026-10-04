import pandas as pd
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour pouvoir importer config
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import OLIST_FILES

def extract_data():
    """Lit tous les fichiers CSV bruts et renvoie un dictionnaire de DataFrames."""
    print("--- 1. EXTRACTION DES DONNEES ---")
    dataframes = {}
    
    for key, path in OLIST_FILES.items():
        if path.exists():
            print(f"Chargement de {key} depuis {path.name}...")
            dataframes[key] = pd.read_csv(path)
        else:
            print(f"⚠️ AVERTISSEMENT: Le fichier {path} n'existe pas.")
            
    print("Extraction terminée avec succès !\n")
    return dataframes

if __name__ == "__main__":
    df_dict = extract_data()
