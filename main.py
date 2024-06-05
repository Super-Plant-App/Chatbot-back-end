from pydantic import BaseModel
from services.chatbot.generaleQuestion import generalQuestion
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from database.init_db import init_mongo

data = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init
    data['mongo_client'] = init_mongo()

    yield

    data.clear()


app = FastAPI(lifespan=lifespan)

class UserData(BaseModel):
    user_id: str
    user_question: str

@app.post('/chatbot/')
async def chatbot_general(user_data: UserData):
    client = data['mongo_client']

    user_id = user_data.user_id
    user_question = user_data.user_question 

    answer = generalQuestion(user_question, user_id)
    
    return answer