from model import generate_answer, get_intent
from fastapi import FastAPI, Request
from models import ChatRequest
from kodibot import Kodibot

app = FastAPI()
route = Kodibot()

@app.get('/')
def home():
    return "Hello World"

@app.post('/chat')
async def chat(request: ChatRequest):
    intent = get_intent(request)
    if intent == 'greeting':
        return route.handle_greeting()
    if intent == 'goodbye':
        return route.handle_goodbye()
    if intent == 'query':
        return route.handle_citizen(request)


