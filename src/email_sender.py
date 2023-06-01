import os
from typing import List

from google.cloud import storage, bigquery
from jinja2 import Template
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from utils import get_image_path

storage_client = storage.Client()
bucket = storage_client.get_bucket('bucket_hm')

client = bigquery.Client()

table_id = "valued-decker-380221.donnees_hm.clients"

EMAIL_ADDRESS = "shoppingrecommendation.esme@gmail.com"
PASSWORD = "owjhybpyeqlmqysl"


# passwordESME2023


def generate_template(filepath: str, user: dict, products: List[dict]) -> str:
    with open(filepath, 'r', encoding='utf-8') as file:
        template = Template(file.read())
    product_images = [get_image_path(product['article_id']) for product in products]
    html_content = template.render(user=user, products=products, product_images=product_images)
    return html_content


def send_email(customer: dict, predicted_reco: List[dict]):
    email_subject = "Nouveaux produits recommandés pour vous"
    template_path = "template/email_template.html"
    email_body = generate_template(template_path, customer, predicted_reco)

    message = Mail(
        from_email=EMAIL_ADDRESS,
        to_emails=EMAIL_ADDRESS,
        subject=email_subject,
        html_content=email_body)
    message.encoding = 'utf-8'

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
#        print(e.message)
