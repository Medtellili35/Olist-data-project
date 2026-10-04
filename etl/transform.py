import pandas as pd
import numpy as np

def transform_data(raw_data):
    """Effectue toutes les transformations et nettoyages sur les DataFrames."""
    print("--- 2. TRANSFORMATION ET NETTOYAGE ---")
    
    # 1. Dimension Customers
    df_customers = raw_data['customers'][
        ['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']
    ].drop_duplicates()
    
    # 2. Dimension Products (Jointure avec les traductions de catégories)
    df_products = raw_data['products'].copy()
    if 'category_translation' in raw_data:
        df_products = df_products.merge(
            raw_data['category_translation'],
            on='product_category_name',
            how='left'
        )
    else:
        df_products['product_category_name_english'] = df_products['product_category_name']
        
    df_products = df_products.rename(columns={
        'product_category_name_english_x': 'product_category_name_english'
    }) if 'product_category_name_english_x' in df_products.columns else df_products

    cols_products = [
        'product_id', 'product_category_name', 'product_category_name_english',
        'product_name_lenght', 'product_description_lenght', 'product_photos_qty',
        'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    # S'assurer que toutes les colonnes existent
    for col in cols_products:
        if col not in df_products.columns:
            df_products[col] = np.nan
            
    df_products = df_products[cols_products].drop_duplicates()

    # 3. Dimension Sellers
    df_sellers = raw_data['sellers'][
        ['seller_id', 'seller_zip_code_prefix', 'seller_city', 'seller_state']
    ].drop_duplicates()

    # 4. Dimension Payments
    df_payments = raw_data['order_payments'].copy()

    # 5. Dimension Reviews
    df_reviews = raw_data['reviews'].copy()
    date_cols_rev = ['review_creation_date', 'review_answer_timestamp']
    for col in date_cols_rev:
        if col in df_reviews.columns:
            df_reviews[col] = pd.to_datetime(df_reviews[col])

    # 6. Fact Orders (Calculs métier & Délais de livraison)
    df_orders = raw_data['orders'].copy()
    df_items = raw_data['order_items'].copy()
    
    # Conversion des dates
    date_cols_ord = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    for col in date_cols_ord:
        if col in df_orders.columns:
            df_orders[col] = pd.to_datetime(df_orders[col])
            
    # Calcul du retard de livraison (en jours)
    df_orders['delivery_delay_days'] = (
        df_orders['order_delivered_customer_date'] - df_orders['order_estimated_delivery_date']
    ).dt.days
    
    # Indicateur binaire de retard (1 = Retard, 0 = Dans les temps)
    df_orders['is_late'] = (df_orders['delivery_delay_days'] > 0).astype(int)

    # Fusion des commandes et articles pour former la table de faits
    df_fact_orders = df_items.merge(df_orders, on='order_id', how='inner')
    
    cols_fact = [
        'order_id', 'order_item_id', 'customer_id', 'product_id', 'seller_id',
        'order_status', 'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date', 'price', 'freight_value',
        'delivery_delay_days', 'is_late'
    ]
    df_fact_orders = df_fact_orders[cols_fact]

    print("Transformation terminée avec succès !\n")
    
    return {
        'dim_customers': df_customers,
        'dim_products': df_products,
        'dim_sellers': df_sellers,
        'dim_payments': df_payments,
        'dim_reviews': df_reviews,
        'fact_orders': df_fact_orders
    }