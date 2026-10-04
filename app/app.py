import os
import joblib
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# 1. Configuration de la page Streamlit
# ---------------------------------------------------------
st.set_page_config(
    page_title="Olist Analytics & ML Platform", page_icon="📦", layout="wide"
)

st.title("📦 Olist E-Commerce - Analytics & Predictive Platform")

# ---------------------------------------------------------
# 2. Gestion dynamique des chemins (Path Resolution)
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))


def get_asset_path(filename):
    """Recherche l'image dans app/assets/ ou assets/"""
    path_app = os.path.join(BASE_DIR, "assets", filename)
    path_root = os.path.join(PROJECT_ROOT, "assets", filename)

    if os.path.exists(path_app):
        return path_app
    elif os.path.exists(path_root):
        return path_root
    return None


def get_model_path():
    """Recherche le modèle .pkl dans ml/ ou app/ml/"""
    path_ml = os.path.join(PROJECT_ROOT, "ml", "model_delivery.pkl")
    path_app = os.path.join(BASE_DIR, "ml", "model_delivery.pkl")

    if os.path.exists(path_ml):
        return path_ml
    elif os.path.exists(path_app):
        return path_app
    return None


# ---------------------------------------------------------
# 3. Structure de l'application en onglets
# ---------------------------------------------------------
tab_bi, tab_ml, tab_predict = st.tabs([
    "📊 Tableaux de Bord BI",
    "🤖 Modèle & Feature Importance",
    "🔮 Simulateur de Livraison",
])

# --- ONGLET 1 : Tableaux de Bord Power BI ---
with tab_bi:
    st.header("Analyse Descriptive de la Performance Commerciale")
    bi_img_path = get_asset_path("dashboard_bi.png")

    if bi_img_path:
        st.image(
            bi_img_path,
            caption="Dashboard Ventes et Logistique (Power BI)",
            use_container_width=True,
        )
    else:
        st.warning(
            "⚠️ Image 'dashboard_bi.png' introuvable dans le dossier 'assets/'. "
            "Veuillez y ajouter la capture d'écran de votre dashboard Power BI."
        )

# --- ONGLET 2 : Machine Learning & Importance des Variables ---
with tab_ml:
    st.header("Évaluation de la Précision du Modèle Machine Learning")
    ml_img_path = get_asset_path("dashboard_ml.png")

    if ml_img_path:
        st.image(
            ml_img_path,
            caption="Comparaison Réel vs Prédit & Importance des Variables (Power BI)",
            use_container_width=True,
        )
    else:
        st.warning(
            "⚠️ Image 'dashboard_ml.png' introuvable dans le dossier 'assets/'. "
            "Veuillez y ajouter la capture d'écran de votre visuel ML."
        )

# --- ONGLET 3 : Simulateur de Prédiction en direct ---
with tab_predict:
    st.header("🔮 Estimer le Délai de Livraison en Temps Réel")
    st.write(
        "Saisissez les caractéristiques d'une commande pour estimer le délai de livraison grâce au modèle **Random Forest** :"
    )

    col1, col2 = st.columns(2)

    with col1:
        weight = st.number_input(
            "Poids du produit (en grammes)", min_value=1.0, value=500.0, step=50.0
        )
        volume = st.number_input(
            "Volume du produit (cm³)", min_value=1.0, value=1200.0, step=100.0
        )
        price = st.number_input(
            "Prix de l'article ($)", min_value=1.0, value=45.0, step=5.0
        )

    with col2:
        freight = st.number_input(
            "Frais de port / Fret ($)", min_value=0.0, value=12.0, step=1.0
        )
        same_state_opt = st.selectbox(
            "Livraison dans le même État ?", ["Oui", "Non"]
        )
        same_state = 1 if same_state_opt == "Oui" else 0

    st.markdown("---")

    if st.button("Calculer la prédiction", type="primary"):
        model_file = get_model_path()

        if model_file and os.path.exists(model_file):
            try:
                # Chargement du modèle sérialisé
                model = joblib.load(model_file)

                # Préparation du DataFrame pour l'inférence
                X_input = pd.DataFrame([{
                    "product_weight_g": weight,
                    "product_volume_cm3": volume,
                    "price": price,
                    "freight_value": freight,
                    "same_state": same_state,
                }])

                # Prédiction
                pred_days = model.predict(X_input)[0]

                st.metric(
                    label="⏱️ Délai de livraison estimé",
                    value=f"{pred_days:.1f} jours",
                )
                st.success("✅ Prédiction générée avec succès par le modèle.")

            except Exception as e:
                st.error(f"Erreur lors de l'exécution du modèle : {e}")
        else:
            st.error(
                "❌ Fichier 'model_delivery.pkl' introuvable dans le dossier 'ml/'. "
                "Veuillez exécuter le script d'entraînement pour générer le modèle."
            )
