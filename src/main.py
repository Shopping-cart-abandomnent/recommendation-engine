import base64
import json
from google.cloud import storage
from google.cloud import bigquery
from datetime import datetime, timedelta

from email_sender import send_email
from recommendation import predict_recommendations

project_id = "valued-decker-380221"
client = bigquery.Client(project=project_id)
client2 = storage.Client()

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
#
# def retrieve_user_info(user_id):
#     query = f'''
#         SELECT first_name, last_name
#         FROM `valued-decker-380221.donnees_hm.clients`
#         WHERE id = "{user_id}"'''
#     user_info = client.query(query).to_dataframe().iloc[0]
#     return {"firstname": user_info["first_name"], "lastname": user_info["last_name"]}
#
# def retrieve_reco_products_info(top_3_reco, recommendation=None):
#     product_ids = recommendation.top_3_reco["product_id"].tolist()
#     query = f"""
#         SELECT prod_name
#         FROM `valued-decker-380221.donnees_hm.articles`
#         WHERE article_id IN ({", ".join(str(product_id) for product_id in product_ids)}) """
#     reco_products_info = client.query(query).to_dataframe()
#     reco_products_info = reco_products_info.to_dict(orient="records")
#     return reco_products_info
#
# def get_image_paths(article_ids):
#     image_paths = []
#     bucket_name = 'bucket_hm'
#     base_folder = 'articles_image'
#
#     for article_id in article_ids:
#         article_id_str = str(article_id)
#         folder_path = article_id_str[:3]
#         image_filename = article_id_str + '.jpg'
#         image_path = f'{base_folder}/{folder_path}/{image_filename}'
#
#         bucket = client2.get_bucket(bucket_name)
#         blob = bucket.blob(image_path)
#         expiration = datetime.utcnow() + timedelta(hours=1)
#         image_url = blob.generate_signed_url(expiration=expiration)
#
#         image_paths.append(image_url)
#
#     return image_paths
#
# top_3_reco = [620036002,351098028,685601036]
# image_paths = get_image_paths(top_3_reco)
# for image_path in image_paths:
#     print(image_path)

def receive_msg(event, context):
    """
    The input message has the following format:
    message = {
        "user_id": user_id,
        "articles_id": []
    }
    """
    received_msg_json = base64.b64decode(event['data'])
    message = json.loads(received_msg_json)
    user_id = message["user_id"]
    articles_ids = message["articles_id"]
    print(f"user id: {user_id}")
    print(f"articles ids: {articles_ids}")

    products_in_carts = get_articles_in_cart(articles_ids)
    print("Info about products in cart acquired")
    all_articles = get_articles_data()
    print("Info about all products acquired")
    predicted_reco = predict_recommendations(all_articles, products_in_carts)
    print("Predicted products:")
    print(predicted_reco)

    # Send a template
    user = retrieve_user_info(user_id)
    products = retrieve_reco_products_info(predicted_reco)
    send_email(user, products)

test_msg = """
 {
     "user_id": "bcfb8358-da22-11ed-8d56-6c94661fccae",
     "articles_id": [620036002,351098028,685601036]
 }
 """
sample_data = {
     "@type": None,
     "data": base64.b64encode(test_msg.encode('ascii'))
 }
receive_msg(sample_data, None)
