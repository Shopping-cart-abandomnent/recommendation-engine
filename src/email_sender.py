import random
import smtplib
import ssl
from typing import List
from google.cloud import storage, bigquery
from jinja2 import Template, FileSystemLoader, Environment
from pandas import DataFrame

storage_client = storage.Client()
bucket = storage_client.get_bucket('bucket_hm')

client = bigquery.Client()

table_id = "valued-decker-380221.donnees_hm.clients"

EMAIL_ADDRESS = "shoppingrecommendation.esme@gmail.com"
PASSWORD = "esme2023"

def generate_template(filepath: str, user: dict, products: List[dict]) -> str:
    with open(filepath) as file:
        template = Template(file.read())
    html_content = template.render(user=user, products= products)
    return html_content


def send_email(customer: dict, predicted_reco: List[dict]):
    email_subject = "Nouveaux produits recommandés pour vous"
    template_path = "src/template/email_template.html"
    email_body = generate_template(template_path, customer, predicted_reco)
    sender_email = EMAIL_ADDRESS
    receivers = EMAIL_ADDRESS

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_ADDRESS, PASSWORD)
        server.sendmail(sender_email, receivers, f"Subject: {email_subject}\n\n{email_body}")