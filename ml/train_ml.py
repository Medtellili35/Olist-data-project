import pandas as pd
import numpy as np
import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Connexion & Chargement des données
DB_URI = 'postgresql://postgres:postgres@localhost:5432/sales_warehouse'
engine = create_engine(DB_URI)

query = """
SELECT 
    p.product_weight_g,
    (p.product_length_cm * p.product_height_cm * p.product_width_cm) AS product_volume_cm3,
    f.price,
    f.freight_value,
    (c.customer_state = s.seller_state)::int AS same_state,
    EXTRACT(DAY FROM (f.order_delivered_customer_date - f.order_purchase_timestamp)) AS delivery_time_days
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
JOIN dim_customers c ON f.customer_id = c.customer_id
JOIN dim_sellers s ON f.seller_id = s.seller_id
WHERE f.order_delivered_customer_date IS NOT NULL;
"""

df = pd.read_sql(query, engine)

# Nettoyage rapide des valeurs aberrantes et des valeurs manquantes
df = df.dropna()
df = df[(df['delivery_time_days'] > 0) & (df['delivery_time_days'] <= 60)]

# 2. Séparation des Features (X) et de la Cible (y)
X = df[['product_weight_g', 'product_volume_cm3', 'price', 'freight_value', 'same_state']]
y = df['delivery_time_days']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Entraînement du modèle (Random Forest)
print("Entraînement du modèle Random Forest en cours...")
model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# 4. Évaluation des performances
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"\n--- Résultats du Modèle ---")
print(f"MAE  (Erreur moyenne absolue) : {mae:.2f} jours")
print(f"RMSE (Racine de l'erreur quadratique) : {rmse:.2f} jours")
print(f"Score R² : {r2:.4f}")

# 5. Sauvegarde du modèle entraîné
joblib.dump(model, 'ml/model_delivery.pkl')
print("\n✅ Modèle sauvegardé avec succès sous 'ml/model_delivery.pkl'")
# Extraction de l'importance des variables
importances = model.feature_importances_
feature_names = ['product_weight_g', 'product_volume_cm3', 'price', 'freight_value', 'same_state']

df_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': importances
}).sort_values(by='importance', ascending=False)

# Export vers PostgreSQL
df_importance.to_sql('fact_feature_importance', engine, if_exists='replace', index=False)
print("✅ Table 'fact_feature_importance' créée dans PostgreSQL !")