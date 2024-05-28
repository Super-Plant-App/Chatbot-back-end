from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/chatbot/general/{question}')
async def chatbot_general(question: str):
    return question

class ChatbotCure(BaseModel):
    plant: str
    disease: str

@app.post('/chatbot/cure')
async def chatbot_cure(question: ChatbotCure):
    return f"{question.plant}:{question.disease}"