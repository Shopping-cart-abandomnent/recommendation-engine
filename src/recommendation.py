from google.cloud import bigquery
import pandas as pd
import random

# Initialize BigQuery client
from pandas import DataFrame


def predict_recommendations(all_articles: DataFrame, products_in_carts: DataFrame):
    all_articles["score"] = 0

    # Same product type
    for _, product in products_in_carts.iterrows():
        all_articles.loc[all_articles["product_type_name"] == product["product_type_name"], "score"] += 1

    # Same color
    for _, product in products_in_carts.iterrows():
        all_articles.loc[all_articles["colour_group_name"] == product["colour_group_name"], "score"] += 1

    # Same product group
    for _, product in products_in_carts.iterrows():
        all_articles.loc[all_articles["product_group_name"] == product["product_group_name"], "score"] += 1

    # Same garment group
    for _, product in products_in_carts.iterrows():
        all_articles.loc[all_articles["garment_group_name"] == product["garment_group_name"], "score"] += 1

    # Sorting by score and print the 2 best recommendations
    all_articles = all_articles[all_articles.index != products_in_carts.index[0]]
    all_articles = all_articles[all_articles.index != products_in_carts.index[1]]
    all_articles = all_articles[all_articles.index != products_in_carts.index[2]]
    top_3_reco = all_articles.sort_values(by=["score"], ascending=False).head(3)
    return top_3_reco

#
#print("\nRecommended products :")
#for _, product in all_articles.iterrows():
#    print("- " + product["prod_name"])
