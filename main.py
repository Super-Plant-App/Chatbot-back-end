from pydantic import BaseModel
from services.chatbot.generaleQuestion import generalQuestion
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

@app.post('/chatbot/')
async def chatbot_general(user_data: UserData):
    chatbotModel = data['chatbotModel']

    user_id = user_data.user_id
    user_question = user_data.user_question 

    answer = generalQuestion(user_question, user_id, chatbotModel)
    
    return answer

# @app.post('/chatbot/clearHistory')
# async def chatbot_general(user_data: UserData):
#     client = data['mongo_client']

#     user_id = user_data.user_id

#     answer = clearHistory(user_id, client)
    
#     return answer