from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    api_key=api_key
)

chat_logs = []

system_prompt = """
    You are a French-speaking virtual assistant, Kodibot, specialized in answering questions about taxes in the Democratic Republic of Congo (DRC), specifically within the context of the Kodinet e-government platform. Respond clearly, concisely, and helpfully in French. Use the following intent categories to guide your responses:
    salutation - Greet the user politely.
    aurevoir - Say goodbye in a friendly and professional manner.
    remerciement - Acknowledge and respond to thanks.
    declaration_impot - Explain how users can declare their taxes via Kodinet.
    paiement_impot - Describe the available methods for paying taxes (e.g., mobile money, bank card, online).
    If a user asks you for their name, answe like this: "Your name is [name]. How may I help you?"
    retard_paiement - Inform users about the consequences of late tax payments.
    exoneration - Provide information on who may be eligible for tax exemptions.
    support - Guide users on how to get help if they encounter issues with Kodinet.
    Always respond in a friendly, professional tone. If a question falls outside these categories, politely inform the user that you are specialized in tax-related topics on Kodinet and suggest they contact official support for further assistance.
"""

def generate_answer(prompt, system_prompt=system_prompt):
    chat_logs.append({
        "role": "user",
        "content": prompt
    })

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

def get_intent(prompt):
    intent_prompt = f"""
    Classifie l'intention de l'utilisateur à partir du message ci-dessous. Choisis uniquement une des catégories suivantes :

    - greeting : si l'utilisateur salue (ex : bonjour, salut)
    - goodbye : si l'utilisateur prend congé (ex : au revoir, merci beaucoup, à bientôt)
    - query : si l'utilisateur pose une question ou demande une information concernant les citoyens, les impôts, les procédures administratives ou les parcelles.

    Réponds uniquement par l'intention exacte (greeting, goodbye, ou query) sans ajouter de texte supplémentaire.

    Message utilisateur :
    "{prompt}"
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant de classification d'intention. Réponds uniquement avec l'intention correcte sans justification."
            },
            {
                "role": "user",
                "content": intent_prompt
            }
        ],
        max_tokens=10,
        temperature=0.0
    )

    return completion.choices[0].message.content.strip()