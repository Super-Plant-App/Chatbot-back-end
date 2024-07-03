from pydantic import BaseModel
from services.chatbot.generaleQuestion import chatbotAskQuestion, chatbotGetCure
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from Models.ChatbotModel import ChatbotModel

data = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    data['chatbotModel'] = ChatbotModel()

    yield

    data.clear()


app = FastAPI(
    docs_url="/chatbot/docs",    # Customize Swagger UI
    redoc_url="/chatbot/redoc",
    lifespan=lifespan
)
# router = APIRouter(prefix="/chatbot")

class UserData(BaseModel):
    # user_id: str
    user_question: str

@app.get('/chatbot')
def home():
    return "Chatbot home page"

@app.post('/chatbot/ask-question')
async def chatbot_general(user_data: UserData):
    chatbotModel = data['chatbotModel']

    user_question = user_data.user_question 
    # user_id = user_data.user_id
    user_id = "665f995565bb190409468564"
    
    answer = chatbotAskQuestion(user_question, user_id, chatbotModel)
    
    return answer[1:-1]

class DiseaseData(BaseModel):
    plantName: str
    diseaseName: str
    # user_id: str

@app.post('/chatbot/get-cure')
async def chatbot_general(disease_date: DiseaseData):
    chatbotModel = data['chatbotModel']

    plant_name = disease_date.plantName
    disease_name = disease_date.diseaseName 
    # user_id = disease_date.user_id
    user_id = "665f995565bb190409468564"

    # clear chat history before getting the cure
    chatbotModel.clear_history(user_id)
    
    answer = chatbotGetCure(plant_name, disease_name, user_id, chatbotModel)
    
    return answer[1:-1]

# class ClearData(BaseModel):
    # user_id: str

@app.post('/chatbot/clear-history')
async def clear_history_route():
    chatbotModel = data['chatbotModel']

    # user_id = clearData.user_id
    user_id = "665f995565bb190409468564"

    return chatbotModel.clear_history(user_id)