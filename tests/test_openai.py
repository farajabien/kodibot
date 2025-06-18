#!/usr/bin/env python3
"""
Test script for OpenAI API to diagnose confidence issues
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

def test_openai_basic():
    """Test basic OpenAI functionality"""
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print('🧪 Test de l\'API OpenAI...')
        
        completion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'Tu es un assistant test. Réponds juste "Test réussi!"'},
                {'role': 'user', 'content': 'Hello'}
            ],
            max_tokens=50
        )
        
        response = completion.choices[0].message.content
        print(f'✅ Réponse OpenAI: {response}')
        print(f'✅ Modèle utilisé: {completion.model}')
        return True
        
    except Exception as e:
        print(f'❌ Erreur OpenAI: {e}')
        return False

def test_intent_classification():
    """Test the intent classification with OpenAI"""
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        print('\n🎯 Test de classification d\'intention...')
        
        test_messages = [
            "Bonjour, comment allez-vous ?",
            "Quel est mon solde de taxe foncière ?", 
            "Mes parcelles",
            "Comment renouveler mon permis ?"
        ]
        
        intent_categories = ["greeting", "goodbye", "profile", "tax_info", "parcels", "procedures", "linking", "fallback"]
        
        for message in test_messages:
            print(f'\n📝 Message: "{message}"')
            
            intent_prompt = f"""
Classifie l'intention de l'utilisateur (uniquement une de ces catégories) et renvoie aussi un score de confiance et les slots extraits:
{', '.join(intent_categories)}

Réponds en JSON EXACT, sans explications :
{{"intent":"<nom_intention>","confidence":<0.00-1.00>,"slots":{{ ... }}}}

Message utilisateur :
\"\"\"{message}\"\"\"
"""
            
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu es KodiBOT, un assistant gouvernemental. Réponds toujours en JSON."},
                    {"role": "user", "content": intent_prompt}
                ],
                temperature=0.0,
                max_tokens=100
            )
            
            response = completion.choices[0].message.content.strip()
            print(f'🔍 Réponse brute: {response}')
            
            try:
                parsed = json.loads(response)
                print(f'✅ Intent: {parsed.get("intent", "N/A")}')
                print(f'✅ Confidence: {parsed.get("confidence", "N/A")}')
                print(f'✅ Slots: {parsed.get("slots", {})}')
            except json.JSONDecodeError as e:
                print(f'❌ Erreur JSON: {e}')
                print(f'❌ Contenu non parsable: {response}')
        
        return True
        
    except Exception as e:
        print(f'❌ Erreur classification: {e}')
        return False

def test_generate_answer():
    """Test the generate_answer function"""
    try:
        from model import generate_answer
        print('\n💬 Test de génération de réponse...')
        
        test_prompt = "Bonjour, je suis Jean Kabila et je veux connaître mon solde de taxe foncière"
        response = generate_answer(test_prompt)
        print(f'✅ Réponse générée: {response[:200]}...')
        return True
        
    except Exception as e:
        print(f'❌ Erreur génération: {e}')
        return False

if __name__ == "__main__":
    print("🔬 Diagnostic OpenAI pour KodiBOT")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY manquante!")
        exit(1)
    else:
        print(f"✅ Clé API trouvée: {api_key[:20]}...")
    
    # Run tests
    print("\n" + "="*50)
    test1 = test_openai_basic()
    test2 = test_intent_classification() if test1 else False
    test3 = test_generate_answer() if test1 else False
    
    print("\n" + "="*50)
    print("📊 RÉSULTATS:")
    print(f"🔗 API OpenAI de base: {'✅' if test1 else '❌'}")
    print(f"🎯 Classification d'intention: {'✅' if test2 else '❌'}")
    print(f"💬 Génération de réponse: {'✅' if test3 else '❌'}") 