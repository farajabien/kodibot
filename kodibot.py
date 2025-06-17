import random
from data import user_tax_data
from model import generate_answer
import json

class Kodibot:
    def __init__(self):
        pass

    def handle_greeting(self):
        greeting_responses = [
            "Bonjour et bienvenue sur Kodinet, je suis Kodibot. Comment puis-je vous aider aujourd'hui ?",
            "Salut ! Je suis Kodibot, votre assistant pour les questions fiscales en RDC. Que puis-je faire pour vous ?",
            "Bienvenue ! Ici Kodibot, votre assistant dédié à la fiscalité sur la plateforme Kodinet.",
            "Bonjour ! Kodibot à votre service. Avez-vous une question concernant les impôts ou les procédures ?",
            "Bonjour, je suis Kodibot. Je suis là pour vous aider avec vos démarches fiscales sur Kodinet."
        ]

        return random.choice(greeting_responses)

    def handle_goodbye(self):
        goodbye_responses = [
            "Merci de m'avoir consulté. Kodibot vous souhaite une excellente journée !",
            "Au revoir et à bientôt sur Kodinet ! Kodibot reste à votre disposition.",
            "Kodibot vous remercie pour votre visite. N'hésitez pas à revenir si vous avez d'autres questions.",
            "Bonne journée et à très bientôt ! Kodibot est toujours là pour vous aider.",
            "Merci pour votre confiance. Kodibot vous dit à la prochaine sur la plateforme Kodinet."
        ]

        return random.choice(goodbye_responses)

    def handle_citizen(self, user_message):
        data = user_tax_data.get('personal_info')
        user_data = json.dumps(data)
        
        response = generate_answer(f"Data: {user_data} User_message: {user_message}")

        return response
