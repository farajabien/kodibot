#!/usr/bin/env python3
"""
Test script for the improved intent classifier
Demonstrates rule-based slot extraction and confidence scoring,
with the enriched RDC/Kodinet system prompt.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from src.model import get_intent

# Load environment variables
load_dotenv()

def test_intent_classifier():
    """Test the improved intent classifier with various examples"""
    
    print("🧠 Testing Improved Intent Classifier")
    print("=" * 60)
    
    test_examples = [
        # Greeting intent
        "Bonjour, comment allez-vous ?",
        "Salut KodiBOT !",
        
        # Goodbye intent  
        "Merci beaucoup, au revoir !",
        "À bientôt et bonne journée",
        
        # Profile intent
        "Quelle est mon adresse enregistrée ?",
        "Quel est mon nom complet ?",
        "Ma date de naissance",
        
        # Tax info intent
        "Quel est mon solde de taxe foncière ?",
        "Combien je dois en impôts cette année ?",
        "Statut de mes taxes",
        
        # Parcels intent with ID extraction
        "Mes biens cadastraux",
        "Informations sur la parcelle P-A12345",
        "Propriété P-KIN-2024",
        
        # Procedures intent with keyword extraction
        "Comment renouveler mon permis de conduire ?",
        "Procédure pour demande de passeport",
        "Étapes pour obtenir un certificat",
        
        # Linking intent with citizen ID extraction
        "Mon numéro de citoyen est CIT123456789",
        "Je veux lier mon compte avec l'ID 987654321",
        "Liaison avec CIT555666777",
        
        # Fallback intent
        "asdfghjkl qwerty",
        "Je veux acheter des bananes",
        "Quel temps fait-il ?"
    ]
    
    for i, message in enumerate(test_examples, 1):
        print(f"\n{i:2d}. 👤 Message: \"{message}\"")
        
        try:
            result = get_intent(message)
            intent     = result["intent"]
            confidence = result["confidence"]
            slots      = result.get("slots", {})
            
            print(f"    🎯 Intent: {intent}")
            print(f"    📊 Confidence: {confidence:.2f}")
            
            if slots:
                print(f"    🔍 Slots extraits:")
                for key, value in slots.items():
                    print(f"       • {key}: {value}")
            else:
                print(f"    🔍 Slots: Aucun")
                
            # Confidence assessment
            if confidence >= 0.8:
                print(f"    ✅ Confiance élevée")
            elif confidence >= 0.6:
                print(f"    ⚠️  Confiance moyenne")
            else:
                print(f"    ❌ Confiance faible - fallback recommandé")
                
        except Exception as e:
            print(f"    ❌ Erreur: {e}")

def test_slot_extraction():
    """Test specific slot extraction patterns"""
    
    print("\n\n🔍 Testing Slot Extraction Patterns")
    print("=" * 60)
    
    slot_tests = [
        ("Mon ID est CIT123456789", "citizen_id"),
        ("Numéro citoyen: 987654321", "citizen_id"), 
        ("Parcelle P-A12345 informations", "parcel_id"),
        ("Comment renouveler mon permis ?", "procedure_name"),
        ("Demande de passeport urgent", "procedure_name"),
        ("Propriété P-KIN-2024-X details", "parcel_id")
    ]
    
    for message, expected_slot in slot_tests:
        print(f"\n👤 Message: \"{message}\"")
        print(f"🎯 Expected slot: {expected_slot}")
        
        try:
            result = get_intent(message)
            slots = result.get("slots", {})
            
            if expected_slot in slots:
                print(f"✅ Slot extrait: {expected_slot} = {slots[expected_slot]}")
            else:
                print(f"❌ Slot manqué: {expected_slot}")
                
            if slots:
                print(f"🔍 Tous les slots: {slots}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY manquante dans le fichier .env")
        exit(1)
    
    test_intent_classifier()
    test_slot_extraction()
