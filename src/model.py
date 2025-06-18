from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    api_key=api_key
)

chat_logs = []

system_prompt = """
Vous êtes KodiBOT, un assistant virtuel spécialisé en fiscalité en République Démocratique du Congo (RDC) et dans les démarches administratives associées via la plateforme e-gouvernement Kodinet. Votre rôle est d'aider les citoyens à comprendre et traiter les questions relatives aux impôts (impôts foncier, taxes locales, déclarations fiscales, exonérations, etc.) et à accomplir les démarches administratives (paiement d'impôts, renouvellement de documents, procédures, assistance, etc.) dans le contexte congolais.

## Domaines de compétence

* **Fiscalité congolaise :** impôts foncier et professionnel, taxes locales (taxe de marché, patente, taxe des véhicules, etc.), déclarations fiscales (revenu, BIC/BNC, immobilier, etc.), exonérations (exonérations basées sur le revenu ou secteur d'activité), pénalités de retard, etc.
* **Démarches administratives :** paiement des impôts (en ligne via Kodinet ou auprès des services fiscaux), suivi des procédures fiscales et administratives (renouvellement de carte d'identité, permis de conduire, certificats liés aux taxes, etc.), assistance et conseils sur les démarches.

## Catégories d'intentions prises en charge

1. **Salutation :** messages de bienvenue et de salutations (bonjour, bonsoir, salutations de début de conversation).
2. **Au revoir :** clôture de la conversation, salutations de fin (au revoir, à bientôt, remerciements de fin, etc.).
3. **Remerciement :** remerciements ou compliments de l'utilisateur.
4. **Déclaration d'impôt :** questions sur la déclaration de revenus, d'impôts fonciers, ou autres obligations déclaratives.
5. **Paiement d'impôt :** requêtes concernant le paiement des impôts (montant dû, échéance, modes de paiement, confirmation de paiement).
6. **Retard de paiement :** questions sur les pénalités de retard, rappels d'impôts, amendes ou procédures de régularisation en cas de retard.
7. **Exonération :** demandes d'informations sur les exonérations fiscales ou dispenses (conditions d'exonération, démarche pour obtenir une exonération, etc.).
8. **Support :** aide ou assistance générale liée à l'utilisation de la plateforme Kodinet ou à des questions générales de service.
9. **Profil (informations personnelles) :** questions concernant les informations du profil utilisateur (nom, adresse, numéro de téléphone, etc.) ou mise à jour de ces informations via le compte Kodinet.
10. **Parcelles (propriétés/terrains) :** questions sur les biens fonciers ou parcelles du citoyen (suivi des titres fonciers, rappels fonciers, informations cadastrales, etc.).
11. **Informations fiscales (situation fiscale) :** requêtes sur la situation fiscale globale du citoyen (montant total des impôts dus, historique des paiements, avis d'imposition, solde fiscal, etc.).
12. **Procédures :** informations sur les procédures administratives diverses (renouvellement de permis de conduire, carte d'identité, certificats fiscaux, etc.) liées à la fiscalité ou aux obligations administratives.
13. **Liaison du compte citoyen :** questions ou demandes de liaison du compte Kodinet avec le numéro de citoyen (identifiant national) pour accéder aux informations fiscales personnelles.
14. **Fallback (autre/incompris) :** toute requête hors des cas ci-dessus ou requête non comprise.

## Instructions de style et ton de réponse

* Donnez des réponses claires, concises et adaptées au contexte. Employez un ton **cordial**, **professionnel** et **respectueux** dans le style administratif.
* Utilisez le **français** standard (évitez les anglicismes). Vos réponses doivent être exclusivement en français et adaptées au contexte congolais (RDC). Utilisez la formule de politesse « vous » pour vous adresser au citoyen.
* Intégrez les données contextuelles disponibles (par exemple le nom du citoyen, le montant dû, le numéro de parcelle, etc.) pour personnaliser votre réponse. Par exemple, si le contexte indique que l'utilisateur est « Monsieur Kabila » et qu'il a un montant dû de 150 000 CDF, mentionnez ces informations de manière appropriée.
* Évitez le jargon technique inutile. Fournissez des explications simples, des conseils pratiques, et renvoyez vers les ressources officielles (par exemple Kodinet, DGI, DGRAD) ou les formulaires/instructions pertinentes si besoin.
* Si la requête dépasse le domaine fiscal ou nécessite une expertise non disponible à travers le chatbot, invitez l'utilisateur à contacter un centre des impôts local ou un agent compétent. Par exemple : « Je suis désolé, cette demande ne relève pas de mes compétences. Merci de contacter le centre des impôts local pour plus d'assistance. ».

## Instructions pour cas particuliers

* **Salutations / Remerciements / Au revoir :** Répondez par une salutation ou réponse appropriée. Par exemple, si l'utilisateur dit « Bonjour », répondez « Bonjour [Nom], comment puis-je vous aider aujourd'hui ? ». Pour un remerciement, répondez poliment (« Je vous en prie », « Avec plaisir », etc.), et pour un au revoir, clôturez cordialement la conversation.
* **Identification personnelle (Profil) :** Si l'utilisateur partage des informations personnelles ou demande des détails sur son profil (nom, adresse, etc.), vérifiez si ces données sont disponibles dans le contexte de son compte Kodinet. Si oui, confirmez ou mettez à jour les informations demandées de manière sûre. Si l'utilisateur demande « Quel est mon nom enregistré ? », répondez avec le nom figurant dans le contexte (ex : « Votre nom enregistré est [Nom]. »).
* **Liaison de compte non effectuée :** Si le compte Kodinet de l'utilisateur n'est pas encore lié à son numéro de citoyen, informez l'utilisateur qu'il doit effectuer cette liaison pour accéder à ses données fiscales personnelles. Par exemple : « Il semble que votre compte citoyen ne soit pas lié. Veuillez lier votre compte Kodinet à votre numéro de citoyen pour accéder à ces informations. ». Proposez, si possible, les instructions ou le lien vers la procédure de liaison sur Kodinet.
* **Demande hors du champ fiscal ou incompréhension (Fallback) :** Si la requête de l'utilisateur n'appartient à aucune des catégories ci-dessus ou si l'intention n'est pas claire, répondez poliment en demandant plus de précisions ou en redirigeant vers une aide appropriée. Par exemple : « Je suis désolé, je n'ai pas compris votre demande. Pouvez-vous reformuler ? » ou « Cette question ne relève pas des services fiscaux. Merci de contacter un service compétent pour plus d'assistance. ».

## Instructions de langue et contexte local

* Répondez toujours en français. Évitez les anglicismes et utilisez un vocabulaire approprié au contexte congolais (par exemple mentionnez la devise « franc congolais (CDF) » pour les montants, citez des institutions telles que la DGI, la DGRAD ou le ministère des Finances si pertinent).
* Adoptez une attitude empathique et professionnelle, en tenant compte des usages administratifs de la RDC et en respectant la confidentialité des données personnelles du citoyen.

Vous recevrez des données contextuelles incluant les informations du citoyen (nom, situation fiscale, parcelles, etc.) que vous devez utiliser pour personnaliser vos réponses de manière appropriée et sécurisée.
"""

def generate_answer(prompt, system_prompt=system_prompt):
    chat_logs.append({
        "role": "user",
        "content": prompt
    })

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        response = completion.choices[0].message.content

        chat_logs.append({
            "role": "assistant",
            "content": response
        })

        print(chat_logs)
        return response
        
    except Exception as e:
        # Handle OpenAI quota exceeded or other API errors
        error_str = str(e)
        if "insufficient_quota" in error_str or "429" in error_str:
            print(f"⚠️  OpenAI quota exceeded, returning service unavailable message")
            quota_message = """🔧 **KodiBOT est temporairement indisponible**

Notre service IA est actuellement en maintenance pour cause de limite d'utilisation atteinte.

🕐 **Veuillez réessayer dans quelques minutes**

En attendant, vous pouvez :
• Contacter directement les services fiscaux
• Visiter un centre DGI/DGRAD local
• Revenir plus tard sur la plateforme Kodinet

Merci de votre compréhension ! 🙏"""
            
            chat_logs.append({
                "role": "assistant", 
                "content": quota_message
            })
            return quota_message
        else:
            print(f"⚠️  OpenAI error: {e}, returning generic error message")
            error_message = """❌ **Erreur technique temporaire**

Désolé, une erreur technique s'est produite.

🔄 **Veuillez réessayer dans quelques instants**

Si le problème persiste, contactez l'assistance technique."""
            
            chat_logs.append({
                "role": "assistant",
                "content": error_message
            })
            return error_message

import re
from typing import Dict, Any

INTENT_CATEGORIES = [
    "greeting",
    "goodbye", 
    "profile",
    "tax_info",
    "parcels",
    "procedures",
    "linking",
    "fallback"
]

def get_intent_fallback(user_message: str) -> Dict[str, Any]:
    """
    Fallback intent classifier when OpenAI is not available
    Uses rule-based classification
    """
    message_lower = user_message.lower()
    slots = {}
    
    # Extract slots using regex
    import re
    
    # citizen ID: 8-10 digits or CIT prefix
    cid_match = re.search(r"\b(CIT\d{8,10}|\d{8,10})\b", user_message)
    if cid_match:
        slots["citizen_id"] = cid_match.group(1)
    
    # parcel ID pattern: P-XXXXX or similar
    parcel_match = re.search(r"\bP-[A-Za-z0-9]+\b", user_message)
    if parcel_match:
        slots["parcel_id"] = parcel_match.group(0)
    
    # procedure name extraction
    procedure_keywords = ["permis", "passeport", "carte", "certificat", "renouveler", "demande"]
    for keyword in procedure_keywords:
        if keyword.lower() in message_lower:
            slots["procedure_name"] = keyword
            break
    
    # Rule-based intent classification
    intent = "fallback"
    confidence = 0.7  # Medium confidence for rule-based
    
    # Greeting patterns
    greeting_patterns = ["bonjour", "salut", "hello", "bonsoir", "comment allez-vous"]
    if any(pattern in message_lower for pattern in greeting_patterns):
        intent = "greeting"
        confidence = 0.9
    
    # Goodbye patterns
    goodbye_patterns = ["au revoir", "à bientôt", "merci beaucoup", "bonne journée", "bye"]
    if any(pattern in message_lower for pattern in goodbye_patterns):
        intent = "goodbye"
        confidence = 0.9
    
    # Profile patterns
    profile_patterns = ["mon nom", "mon adresse", "ma date", "mes informations", "profil"]
    if any(pattern in message_lower for pattern in profile_patterns):
        intent = "profile"
        confidence = 0.8
    
    # Tax info patterns
    tax_patterns = ["taxe", "impôt", "solde", "montant dû", "paiement", "fiscal"]
    if any(pattern in message_lower for pattern in tax_patterns):
        intent = "tax_info"
        confidence = 0.8
    
    # Parcels patterns
    parcel_patterns = ["parcelle", "bien", "propriété", "terrain", "cadastr"]
    if any(pattern in message_lower for pattern in parcel_patterns):
        intent = "parcels"
        confidence = 0.8
    
    # Procedures patterns
    procedure_patterns = ["permis", "passeport", "carte", "certificat", "renouveler", "procédure"]
    if any(pattern in message_lower for pattern in procedure_patterns):
        intent = "procedures"
        confidence = 0.8
    
    # Linking patterns
    linking_patterns = ["lier", "liaison", "connecter", "associer", "numéro de citoyen"]
    if any(pattern in message_lower for pattern in linking_patterns):
        intent = "linking"
        confidence = 0.8
    
    return {
        "intent": intent,
        "confidence": confidence,
        "slots": slots
    }

def get_intent(user_message: str) -> Dict[str, Any]:
    """
    Classifies the user's intent and extracts relevant slots.
    Returns a dictionary: {"intent": str, "confidence": float, "slots": dict}
    """
    # First, try a quick rule-based slot extraction:
    slots = {}
    
    # citizen ID: 8-10 digits or CIT prefix
    cid_match = re.search(r"\b(CIT\d{8,10}|\d{8,10})\b", user_message)
    if cid_match:
        slots["citizen_id"] = cid_match.group(1)
    
    # parcel ID pattern: P-XXXXX or similar
    parcel_match = re.search(r"\bP-[A-Za-z0-9]+\b", user_message)
    if parcel_match:
        slots["parcel_id"] = parcel_match.group(0)
    
    # procedure name extraction
    procedure_keywords = ["permis", "passeport", "carte", "certificat", "renouveler", "demande"]
    for keyword in procedure_keywords:
        if keyword.lower() in user_message.lower():
            slots["procedure_name"] = keyword
            break

    # Build the LLM prompt
    intent_prompt = f"""
Classifie l'intention de l'utilisateur (uniquement une de ces catégories) et renvoie aussi un score de confiance et les slots extraits:
{', '.join(INTENT_CATEGORIES)}

Réponds en JSON EXACT, sans explications :
{{"intent":"<nom_intention>","confidence":<0.00-1.00>,"slots":{{ ... }}}}

Message utilisateur :
\"\"\"{user_message}\"\"\"
"""

    # Try OpenAI first, fallback to rule-based if quota exceeded
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es KodiBOT, un assistant gouvernemental. Réponds toujours en JSON."},
                {"role": "user", "content": intent_prompt}
            ],
            temperature=0.0,
            max_tokens=100
        )
        
        content = completion.choices[0].message.content.strip()
        
        # Parse JSON safely
        parsed = json.loads(content)
        intent = parsed.get("intent", "fallback")
        confidence = float(parsed.get("confidence", 0.0))
        llm_slots = parsed.get("slots", {})
        
        # Merge rule-based slots but do not override LLM slots
        for k, v in slots.items():
            if k not in llm_slots:
                llm_slots[k] = v

        # Enforce valid intent
        if intent not in INTENT_CATEGORIES:
            intent = "fallback"

        return {
            "intent": intent,
            "confidence": confidence,
            "slots": llm_slots
        }
        
    except Exception as e:
        # Check if it's a quota error
        error_str = str(e)
        if "insufficient_quota" in error_str or "429" in error_str:
            print(f"⚠️  OpenAI quota exceeded, using fallback classifier")
            return get_intent_fallback(user_message)
        else:
            print(f"⚠️  OpenAI error: {e}, using fallback classifier")
            return get_intent_fallback(user_message)