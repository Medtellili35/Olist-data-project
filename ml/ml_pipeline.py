import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# 1. Connexion à la base PostgreSQL
# ⚠️ Remplacez 'mot_de_passe' par votre vrai mot de passe PostgreSQL
DB_URI = 'postgresql://postgres:postgres@localhost:5432/sales_warehouse'
engine = create_engine(DB_URI)

print("Connexion à la base de données en cours...")

# 2. Requête d'extraction des caractéristiques (Features)
query = """
SELECT 
    f.order_id,
    p.product_weight_g,
    (p.product_length_cm * p.product_height_cm * p.product_width_cm) AS product_volume_cm3,
    f.price,
    f.freight_value,
    c.customer_state,
    s.seller_state,
    f.order_purchase_timestamp,
    f.order_delivered_customer_date
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_sellers s ON f.seller_id = s.seller_id
WHERE f.order_delivered_customer_date IS NOT NULL;
"""

df = pd.read_sql(query, engine)
print(f"✅ Données chargées avec succès : {df.shape[0]} lignes et {df.shape[1]} colonnes.\n")

# 3. Calcul de la variable cible (Target variable) : Délai de livraison en jours
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])

df['delivery_time_days'] = (
    df['order_delivered_customer_date'] - df['order_purchase_timestamp']
).dt.total_seconds() / (24 * 3600)

# Filtrer les valeurs aberrantes (ex: délais négatifs ou supérieurs à 60 jours)
df = df[(df['delivery_time_days'] > 0) & (df['delivery_time_days'] <= 60)]

# Indication si le vendeur et le client sont dans le même État
df['same_state'] = (df['customer_state'] == df['seller_state']).astype(int)

print("Aperçu du jeu de données préparé :")
print(df[['delivery_time_days', 'product_weight_g', 'freight_value', 'same_state']].head())
