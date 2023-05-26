# pip install Jinja2

import smtplib

from jinja2 import Environment, FileSystemLoader
from template.mime.text import MIMEText


def send_email(sender_email, sender_password, receiver_email, subject, heading, content):
    # Configurer le système de fichiers pour les modèles Jinja2
    file_loader = FileSystemLoader('chemin/vers/le/dossier/contenant/le/template')
    env = Environment(loader=file_loader)

    # Charger le modèle Jinja2
    template = env.get_template('email_template.html')

    # Remplir les variables du modèle Jinja2 avec les valeurs des arguments de la fonction
    html_content = template.render(subject=subject, heading=heading, content=content)

    # Créer le message MIME pour l'template
    message = MIMEText(html_content, 'html')
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Configurer le serveur SMTP
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)

    # Envoyer l'template
    smtp_server.sendmail(sender_email, receiver_email, message.as_string())
    smtp_server.quit()


sender_email = 'monadresse@template.com'
sender_password = 'monmotdepasse'
receiver_email = 'adressedestinataire@template.com'
subject = 'Sujet de l\'template'
heading = 'Titre de l\'template'
content = 'Contenu de l\'template'

send_email(sender_email, sender_password, receiver_email, subject, heading, content)
