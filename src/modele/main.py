import json

from google.cloud import bigquery

from src.modele.email_sender import send_email
from src.modele.recommendation import predict_recommendations

client = bigquery.Client()


def get_articles_data():
    query = """
        SELECT *
        FROM `valued-decker-380221.donnees_hm.articles`
    """
    all_articles = client.query(query).to_dataframe()
    return all_articles


def get_articles_in_cart(products_ids):
    query = """
        SELECT *
        FROM `valued-decker-380221.donnees_hm.articles`
        WHERE article_id IN (448831026, 510264001, 566941026)
    """
    articles_in_cart = client.query(query).to_dataframe()
    return articles_in_cart



def receive_msg(msg):
    msg_dict = json.loads(msg)
    customer_id = msg_dict["user_id"]
    articles_ids = msg_dict["articles_id"]

    products_in_carts = get_articles_in_cart(articles_ids)
    print("Info about products in cart acquired")
    all_articles = get_articles_data()
    print("Info about all products acquired")
    predicted_reco = predict_recommendations(all_articles, products_in_carts)
    print("Predicted products:")
    print(predicted_reco)

    # Send an email
    send_email(customer_id, articles_ids, predicted_reco)

    # Write the recommendation in a new table
        # DB-admin -> create recommendations table

test_msg = """
{
    "user_id": "bcfb8358-da22-11ed-8d56-6c94661fccae", 
    "articles_id": [802024001, 736489021, 892915001]
}
"""
receive_msg(test_msg)
