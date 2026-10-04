-- Active: 1790833703694@@127.0.0.1@5432@sales_warehouse
SELECT * FROM dim_customers LIMIT 10;
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
SELECT * 
FROM fact_orders 
LIMIT 10;
SELECT SUM(price) AS chiffre_affaires_total 
FROM fact_orders;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'fact_orders';
SELECT SUM(price) AS chiffre_affaires_total 
FROM fact_orders;
SELECT COUNT(DISTINCT order_id) AS total_commandes 
FROM fact_orders;
SELECT 
    COUNT(DISTINCT order_id) AS total_commandes,  -- ✅ Virgule ajoutée
    ROUND(AVG(price)::numeric, 2) AS panier_moyen
FROM fact_orders;

-- KPI 1 : Chiffre d'Affaires Total
SELECT 
    SUM(price) AS chiffre_affaires_total
FROM fact_orders;

-- KPI 2 : Nombre Total de Commandes
SELECT 
    COUNT(DISTINCT order_id) AS total_commandes
FROM fact_orders;

-- KPI 3 : Panier Moyen (AOV)
SELECT 
    ROUND(AVG(price)::numeric, 2) AS panier_moyen
FROM fact_orders;
-- KPI 4 : Top 5 des Catégories de Produits les Plus Vendues
SELECT 
    p.product_category_name,
    COUNT(DISTINCT f.order_id) AS total_commandes,
    ROUND(SUM(f.price)::numeric, 2) AS chiffre_affaires
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY chiffre_affaires DESC
LIMIT 5;

-- KPI 5 : Top 5 des États (Régions) les Plus Rentables
SELECT 
    c.customer_state,
    COUNT(DISTINCT f.order_id) AS total_commandes,
    ROUND(SUM(f.price)::numeric, 2) AS total_ventes
FROM fact_orders f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY total_ventes DESC
LIMIT 5;

-- KPI 6 : Répartition des Modes de Paiement
SELECT 
    price,
    COUNT(order_id) AS nombre_utilisations,
    ROUND(SUM(price)::numeric, 2) AS montant_total
FROM fact_orders
GROUP BY price
ORDER BY montant_total DESC;
-- KPI 7 : Délai Moyen de Livraison (en jours)
-- KPI 7 : Délai Moyen de Livraison (en jours)
SELECT 
    ROUND(AVG(DATE(order_delivered_customer_date) - DATE(order_purchase_timestamp))::numeric, 1) AS delai_moyen_livraison
FROM fact_orders
WHERE order_delivered_customer_date IS NOT NULL;


-- KPI 8 : Taux de Satisfaction Client (Note Moyenne)
-- KPI 8 : Taux de Satisfaction Client
SELECT 
    ROUND(AVG(score)::numeric, 2) AS score_moyen_avis
FROM fact_orders;
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'fact_orders'
ORDER BY ordinal_position;
-- KPI 8 (Alternative) : Taux de livraison dans les temps (%)
SELECT 
    ROUND(
        (COUNT(CASE WHEN order_delivered_customer_date <= order_estimated_delivery_date THEN 1 END) * 100.0 / COUNT(*))::numeric, 
        2
    ) AS taux_livraison_a_temps_pct
FROM fact_orders
WHERE order_delivered_customer_date IS NOT NULL 
  AND order_estimated_delivery_date IS NOT NULL;
CREATE OR REPLACE VIEW view_kpi_summary AS
SELECT 
    COUNT(DISTINCT order_id) AS total_commandes,
    ROUND(SUM(price)::numeric, 2) AS chiffre_affaires_total,
    ROUND(AVG(price)::numeric, 2) AS panier_moyen,
    ROUND(AVG(DATE(order_delivered_customer_date) - DATE(order_purchase_timestamp))::numeric, 1) AS delai_moyen_livraison,
    ROUND(
        (COUNT(CASE WHEN order_delivered_customer_date <= order_estimated_delivery_date THEN 1 END) * 100.0 / COUNT(*))::numeric, 
        2
    ) AS taux_livraison_a_temps_pct
FROM fact_orders
WHERE order_delivered_customer_date IS NOT NULL;
CREATE OR REPLACE VIEW view_kpi_global AS
SELECT 
    COUNT(DISTINCT order_id) AS total_commandes,
    ROUND(SUM(price)::numeric, 2) AS chiffre_affaires_total,
    ROUND(AVG(price)::numeric, 2) AS panier_moyen,
    ROUND(AVG(DATE(order_delivered_customer_date) - DATE(order_purchase_timestamp))::numeric, 1) AS delai_moyen_livraison,
    ROUND(
        (COUNT(CASE WHEN order_delivered_customer_date <= order_estimated_delivery_date THEN 1 END) * 100.0 / COUNT(*))::numeric, 
        2
    ) AS taux_livraison_a_temps_pct
FROM fact_orders
WHERE order_delivered_customer_date IS NOT NULL;
CREATE OR REPLACE VIEW view_kpi_price AS
SELECT 
    price,
    COUNT(order_id) AS nombre_utilisations,
    ROUND(SUM(price)::numeric, 2) AS montant_total
FROM fact_orders
GROUP BY price
ORDER BY montant_total DESC;
CREATE OR REPLACE VIEW view_kpi_products AS
SELECT 
    p.product_category_name,
    COUNT(DISTINCT f.order_id) AS total_commandes,
    ROUND(SUM(f.price)::numeric, 2) AS chiffre_affaires
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY chiffre_affaires DESC;
CREATE OR REPLACE VIEW view_kpi_customers AS
SELECT 
    c.customer_state,
    COUNT(DISTINCT f.order_id) AS total_commandes,
    ROUND(SUM(f.price)::numeric, 2) AS total_ventes
FROM fact_orders f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY total_ventes DESC;

CREATE OR REPLACE VIEW view_kpi_payments AS
SELECT 
    price,
    COUNT(order_id) AS nombre_utilisations,
    ROUND(SUM(price)::numeric, 2) AS montant_total
FROM fact_orders
GROUP BY price
ORDER BY montant_total DESC;
CREATE OR REPLACE VIEW view_kpi_payments AS
SELECT 
    price,
    COUNT(order_id) AS nombre_utilisations,
    ROUND(SUM(price)::numeric, 2) AS montant_total
FROM fact_orders
GROUP BY price
ORDER BY montant_total DESC;
CREATE OR REPLACE VIEW view_kpi_products AS
SELECT 
    p.product_category_name,
    COUNT(DISTINCT f.order_id) AS total_commandes,
    ROUND(SUM(f.price)::numeric, 2) AS chiffre_affaires
FROM fact_orders f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY chiffre_affaires DESC;
CREATE OR REPLACE VIEW view_kpi_reviews AS
SELECT 
    review_score,
    COUNT(review_id) AS nombre_avis,
    ROUND(AVG(review_score)::numeric, 2) AS note_moyenne
FROM dim_reviews
GROUP BY review_score
ORDER BY review_score DESC;