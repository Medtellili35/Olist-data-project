import os
import urllib.parse
from pathlib import Path

# ==========================================
# 1. CHEMINS DE BASE ET DOSSIERS (PATH)
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "etl" else Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "DATA" / "Raw"

# ==========================================
# 2. CONFIGURATION POSTGRESQL (BASE DE DONNÉES)
# ==========================================
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")  # <--- Mot de passe mis à jour
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "sales_warehouse")  # <--- Vérifiez bien le nom de votre BDD (sales_warehouse ou olist_db)

# Encodage sécurisé des identifiants
encoded_user = urllib.parse.quote_plus(DB_USER)
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

# URL de connexion SQLAlchemy (avec le driver psycopg)
DB_URL = f"postgresql+psycopg://{encoded_user}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ==========================================
# 3. MAPPAGE DES FICHIERS CSV BRUTS
# ==========================================
OLIST_FILES = {
    "orders": DATA_DIR / "olist_orders_dataset.csv",
    "customers": DATA_DIR / "olist_customers_dataset.csv",
    "order_items": DATA_DIR / "olist_order_items_dataset.csv",
    "order_payments": DATA_DIR / "olist_order_payments_dataset.csv",
    "products": DATA_DIR / "olist_products_dataset.csv",
    "sellers": DATA_DIR / "olist_sellers_dataset.csv",
    "reviews": DATA_DIR / "olist_order_reviews_dataset.csv",
    "category_translation": DATA_DIR / "product_category_name_translation.csv"
}
