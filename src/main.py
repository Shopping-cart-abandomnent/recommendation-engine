import base64
import json
import os

from email_sender import send_email
# Définition de la variable d'environnement GOOGLE_APPLICATION_CREDENTIALS
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "auth.json"
from src.recommendation import predict_recommendations

# client = bigquery.Client()
from google.cloud import bigquery

project_id = "valued-decker-380221"
client = bigquery.Client(project=project_id)


def get_articles_data():
    query = """
        SELECT *
        FROM `valued-decker-380221.donnees_hm.articles`
    """
    all_articles = client.query(query).to_dataframe()
    return all_articles


def get_articles_in_cart(products_ids):
    query = f"""
        SELECT *
        FROM `valued-decker-380221.donnees_hm.articles`
        WHERE article_id IN ({products_ids[0]}, {products_ids[1]}, {products_ids[2]})
    """
    articles_in_cart = client.query(query).to_dataframe()
    return articles_in_cart


def retrieve_user_info(user_id):
    return {"firstname": "Jean", "lastname": "De Jaeger"}


def retrieve_reco_products_info(reco_df):
    return [
        {"name": "Chaussette Superman", "url": "http://this_is_product1_url.com"},
        {"name": "T-Shirt", "url": "http://this_is_product2_url.com"}
    ]


def receive_msg(event, context):
    """
    The input message has the following format:
    message = {
        "user_id": user_id,
        "articles_id": []
    }
    """
    received_msg_json = base64.b64decode(event['data']).decode('utf-8')
    message = json.loads(received_msg_json)
    user_id = message["user_id"]
    articles_ids = message["articles_id"]

    products_in_carts = get_articles_in_cart(articles_ids)
    print("Info about products in cart acquired")
    all_articles = get_articles_data()
    print("Info about all products acquired")
    predicted_reco = predict_recommendations(all_articles, products_in_carts)
    print("Predicted products:")
    print(predicted_reco)

    # Send an template
    user = retrieve_user_info(user_id)
    products = retrieve_reco_products_info(predicted_reco)
    send_email(user, products)

    # Write the recommendation in a new table
    # DB-admin -> create recommendations table


test_msg = """
{
    "user_id": "bcfb8358-da22-11ed-8d56-6c94661fccae", 
    "articles_id": [802024001, 736489021, 892915001]
}
"""
receive_msg(test_msg)
