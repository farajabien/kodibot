"""
KodiBOT Core Chat Logic
Modernized to use centralized prompts and DRC-specific responses
"""

import random
from .prompts import MAIN_SYSTEM_PROMPT

class Kodibot:
    """
    Core KodiBOT chat logic with DRC-specific responses
    Uses centralized prompt system and modern architecture
    """
    
    def __init__(self):
        # Modern initialization - no dependencies on obsolete data
        self.name = "KodiBOT"
        self.version = "2.0.0"
        self.country = "République Démocratique du Congo"
    
    def get_system_info(self) -> dict:
        """Get system information"""
        return {
            "name": self.name,
            "version": self.version,
            "country": self.country,
            "services": ["Fiscalité", "Parcelles", "Procédures", "Profil citoyen"]
        }

    def handle_greeting(self) -> str:
        """
        Handle greeting messages with DRC-specific responses
        Returns randomized professional greetings
        """
        greeting_responses = [
            "Bonjour et bienvenue sur KodiBOT! 🇨🇩 Je suis votre assistant pour les services gouvernementaux de la RDC. Comment puis-je vous aider?",
            "Salut! Ici KodiBOT, votre assistant numérique pour la fiscalité et les démarches administratives en RDC. Que puis-je faire pour vous?",
            "Bienvenue! KodiBOT à votre service pour tous vos besoins liés aux taxes, parcelles et procédures gouvernementales.",
            "Bonjour! Je suis KodiBOT, spécialisé dans l'assistance fiscale DGI/DGRAD. Comment puis-je vous accompagner aujourd'hui?",
            "Bienvenue ! Ici Kodibot, votre assistant dédié à la fiscalité sur la plateforme Kodinet."
        ]
        return random.choice(greeting_responses)

    def handle_goodbye(self) -> str:
        """
        Handle goodbye messages with professional DRC responses
        Returns randomized farewell messages
        """
        goodbye_responses = [
            "Merci d'avoir utilisé KodiBOT! 🙏 N'hésitez pas à revenir pour vos questions fiscales et administratives.",
            "Au revoir! KodiBOT reste disponible 24/7 pour vous accompagner dans vos démarches gouvernementales.",
            "Bonne journée! Merci de faire confiance à KodiBOT pour vos services citoyens en RDC.",
            "À bientôt sur KodiBOT! Votre assistant numérique pour la République Démocratique du Congo.",
            "Merci pour votre confiance. Kodibot vous dit à la prochaine sur la plateforme Kodinet."
        ]
        return random.choice(goodbye_responses)

    def handle_system_unavailable(self) -> str:
        """
        Handle system unavailable scenarios (quota exceeded, maintenance)
        Returns professional service unavailable message
        """
        return """🔧 **KodiBOT est temporairement indisponible**

Notre service IA est actuellement en maintenance.

🕐 **Veuillez réessayer dans quelques minutes**

En attendant, vous pouvez :
• Contacter directement les services DGI/DGRAD
• Visiter un centre fiscal local
• Revenir plus tard sur la plateforme

Merci de votre compréhension ! 🙏"""
    
    def handle_linking_required(self) -> str:
        """
        Handle cases where user needs to link their account
        Returns linking prompt message
        """
        return "Bienvenue sur KodiBOT! 📋 Pour accéder à vos informations, veuillez lier votre téléphone en tapant votre numéro de citoyen (format: CIT123456789)."
    
    def handle_unknown_request(self) -> str:
        """
        Handle unknown or unclear requests
        Returns helpful fallback message
        """
        return """Je ne comprends pas bien votre demande. 

Voici ce que je peux vous aider à faire:

📊 **Informations fiscales**: "Quel est mon solde de taxe?"
👤 **Profil personnel**: "Quelle est mon adresse?"
🏠 **Biens cadastraux**: "Mes parcelles"
📋 **Procédures**: "Comment renouveler mon permis?"

Reformulez votre question ou choisissez une option ci-dessus."""
    
    def get_available_services(self) -> list:
        """
        Get list of available services
        Returns list of service categories
        """
        return [
            {"name": "Fiscalité", "description": "Taxes, impôts, soldes fiscaux"},
            {"name": "Parcelles", "description": "Biens cadastraux, propriétés foncières"},
            {"name": "Procédures", "description": "Démarches administratives, renouvellements"},
            {"name": "Profil", "description": "Informations personnelles citoyens"},
            {"name": "Liaison", "description": "Connexion compte citoyen"}
        ]
