import pandas as pd
import joblib
from sqlalchemy import create_engine

# Connexion à PostgreSQL
engine = create_engine('postgresql://postgres:postgres@localhost:5432/sales_warehouse')

# 1. Charger le modèle
model = joblib.load('ml/model_delivery.pkl')

# 2. Requéter les données en incluant customer_state
query = """
SELECT 
    f.order_id,
    c.customer_state,
    p.product_weight_g,
    (p.product_length_cm * p.product_height_cm * p.product_width_cm) AS product_volume_cm3,
    f.price,
    f.freight_value,
    (c.customer_state = s.seller_state)::int AS same_state,
    EXTRACT(DAY FROM (f.order_delivered_customer_date - f.order_purchase_timestamp)) AS delivery_time_actual
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_sellers s ON f.seller_id = s.seller_id
WHERE f.order_delivered_customer_date IS NOT NULL;
"""

df = pd.read_sql(query, engine)
df = df.dropna()

# 3. Générer les prédictions
X = df[['product_weight_g', 'product_volume_cm3', 'price', 'freight_value', 'same_state']]
df['delivery_time_predicted'] = model.predict(X)

# 4. Enregistrer la table avec customer_state dans PostgreSQL
df_output = df[['order_id', 'customer_state', 'delivery_time_actual', 'delivery_time_predicted']]
df_output.to_sql('fact_predictions', engine, if_exists='replace', index=False)

print("✅ Table 'fact_predictions' mise à jour avec la colonne 'customer_state' !")
