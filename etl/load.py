from sqlalchemy import create_engine
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import DB_URL

def load_data(transformed_data):
    """Charge les DataFrames dans la base de données PostgreSQL."""
    print("--- 3. CHARGEMENT DANS POSTGRESQL ---")
    engine = create_engine(DB_URL)
    
    # Ordre de chargement : D'abord les dimensions, puis la table de faits
    load_order = [
        'dim_customers',
        'dim_products',
        'dim_sellers',
        'dim_payments',
        'dim_reviews',
        'fact_orders'
    ]
    
    for table_name in load_order:
        if table_name in transformed_data:
            df = transformed_data[table_name]
            print(f"Chargement de {len(df)} lignes dans la table {table_name}...")
            # 'append' ajoute les données dans les tables SQL existantes
            df.to_sql(table_name, engine, if_exists='append', index=False, chunksize=1000)
            
    print("\nChargement dans le Data Warehouse terminé avec succès !")

if __name__ == "__main__":
    pass