import json
from .prompts import MAIN_SYSTEM_PROMPT, INTENT_SYSTEM_PROMPT
from .openai_client import get_client

chat_logs = []

def generate_answer(prompt, system_prompt=MAIN_SYSTEM_PROMPT):
    chat_logs.append({
        "role": "user",
        "content": prompt
    })

    try:
        client = get_client()
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
        client = get_client()
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": INTENT_SYSTEM_PROMPT},
                {"role": "user", "content": intent_prompt}
            ],
            temperature=0.0,
            max_tokens=100
        )
        
        content = (completion.choices[0].message.content or "").strip()
        
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