import random
import smtplib
from typing import List

from pandas import DataFrame

from recommendation import top_3_reco
from random_transaction import transaction_data

def send_email(customer_id: str, articles_ids: List[int], predicted_reco: DataFrame):
    # retrieve the necessary information
    customer_info = {"firstname": "", "lastname": "Jean"}
    reco_products_info = [{"product_name": "abc", "img_url": ""}, {"product_name": "abc", "img_url": ""}]
    pass

# user_id = random.choice(list(transaction_data.keys()))
# user = transaction_data[user_id]
#
# # Générer l'email personnalisé    àici, insérer le code html et css ?
#
# email_subject = "Nouveaux produits recommandés pour vous"
#
# email_body = f"Bonjour {user['nom']},\n\nVoici nos derniers produits recommandés pour vous:\n\n"
#
# for produit in top_3_reco:
#     email_body += f"- {produit['nom']} ({produit['categorie']})\n"
#
# email_body += "\nMerci d'avoir utilisé notre site !"
#
# # Envoyer l'email
#
# sender_email = "votre@email.com"
# sender_password = "votre_mot_de_passe"
# server = smtplib.SMTP('smtp.gmail.com', 587)
# server.starttls()
# server.login(sender_email, sender_password)
# server.sendmail(sender_email, user['email'], f"Subject: {email_subject}\n\n{email_body}")
# server.quit()