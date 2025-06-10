from model import generate_answer
from fastapi import FastAPI, Request
from models import ChatRequest

app = FastAPI()

@app.get('/')
def home():
    return "Hello World"

@app.post('/chat')
async def chat(request: ChatRequest):
    user_message = request.message
    response = generate_answer(user_message)
    return {"response": response}
