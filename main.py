from fastapi import FastAPI
from pydantic import BaseModel
from services.chatbot.getCure import getCure
from services.chatbot.generaleQuestion import generalQuestion

app = FastAPI()

class ChatbotCure(BaseModel):
    plant: str
    disease: str

@app.get('/chatbot/general/{question}')
async def chatbot_general(question: str):
    answer = generalQuestion(question)
    
    return answer

@app.post('/chatbot/cure')
async def chatbot_cure(question: ChatbotCure):
    cure = getCure(question.plant, question.disease)

    return f"{question.plant}:{question.disease}"