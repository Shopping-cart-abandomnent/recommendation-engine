from google.cloud import bigquery

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


def receive_msg(message):
    """
    {
        "customerId": 55,
        "products_id": [10, 20, 99]
    }
    """
    products_in_carts = get_articles_in_cart([448831026, 510264001, 566941026])
    print("Info about products in cart acquired")
    all_articles = get_articles_data()
    print("Info about all products acquired")
    predicted_reco = predict_recommendations(all_articles, products_in_carts)
    print("Predicted products:")
    print(predicted_reco)

    # Write the recommendation in a new table

    # Send an email

receive_msg()
