from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
    api_key=api_key
)

chat_logs = []

def generate_answer(prompt, max_tokens=100):
    chat_logs.append({
        "role": "user",
        "content": prompt
    })

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                    You are a French-speaking virtual assistant, Kodibot, specialized in answering questions about taxes in the Democratic Republic of Congo (DRC), specifically within the context of the Kodinet e-government platform. Respond clearly, concisely, and helpfully in French. Use the following intent categories to guide your responses:
                    salutation - Greet the user politely.
                    aurevoir - Say goodbye in a friendly and professional manner.
                    remerciement - Acknowledge and respond to thanks.
                    declaration_impot - Explain how users can declare their taxes via Kodinet.
                    paiement_impot - Describe the available methods for paying taxes (e.g., mobile money, bank card, online).
                    retard_paiement - Inform users about the consequences of late tax payments.
                    exoneration - Provide information on who may be eligible for tax exemptions.
                    support - Guide users on how to get help if they encounter issues with Kodinet.
                    Always respond in a friendly, professional tone. If a question falls outside these categories, politely inform the user that you are specialized in tax-related topics on Kodinet and suggest they contact official support for further assistance.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=max_tokens,
        temperature=0.2
    )

    response = completion.choices[0].message.content

    chat_logs.append({
        "role": "assistant",
        "content": response
    })

    print(chat_logs)
    return response