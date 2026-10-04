from extract import extract_data
from transform import transform_data
from load import load_data

def run_pipeline():
    print("==========================================")
    print("Lancement du Pipeline ETL Olist Project")
    print("==========================================\n")
    
    # 1. Extraction
    raw_data = extract_data()
    
    # 2. Transformation
    transformed_data = transform_data(raw_data)
    
    # 3. Chargement
    load_data(transformed_data)
    
    print("\n==========================================")
    print("   PIPELINE EXECUTÉ AVEC SUCCÈS ! 🎉   ")
    print("==========================================")

if __name__ == "__main__":
    run_pipeline()
