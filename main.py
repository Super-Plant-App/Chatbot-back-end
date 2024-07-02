from pydantic import BaseModel
from services.chatbot.generaleQuestion import chatbotAskQuestion, chatbotGetCure
from fastapi import FastAPI
from contextlib import asynccontextmanager
from Models.ChatbotModel import ChatbotModel

data = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    data['chatbotModel'] = ChatbotModel()

    yield

    data.clear()


app = FastAPI(lifespan=lifespan)

class UserData(BaseModel):
    user_id: str
    user_question: str

@app.get('/')
def home():
    return "Chatbot home page"

@app.post('/ask-question')
async def chatbot_general(user_data: UserData):
    chatbotModel = data['chatbotModel']

    user_id = user_data.user_id
    user_question = user_data.user_question 

    answer = chatbotAskQuestion(user_question, user_id, chatbotModel)
    
    return answer

class DiseaseData(BaseModel):
    plantName: str
    diseaseName: str
    user_id: str

@app.post('/get-cure')
async def chatbot_general(disease_date: DiseaseData):
    chatbotModel = data['chatbotModel']

    plant_name = disease_date.plantName
    disease_name = disease_date.diseaseName 
    user_id = disease_date.user_id

    # clear chat history before getting the cure
    chatbotModel.clear_history(user_id)
    
    answer = chatbotGetCure(plant_name, disease_name, user_id, chatbotModel)
    
    return answer

class ClearData(BaseModel):
    user_id: str

@app.post('/clear-history')
async def clear_history_route(clearData: ClearData):
    chatbotModel = data['chatbotModel']

    user_id = clearData.user_id

    return chatbotModel.clear_history(user_id)