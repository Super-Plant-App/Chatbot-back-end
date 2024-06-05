from pydantic import BaseModel
from services.chatbot.generaleQuestion import generalQuestion
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from database.init_db import init_mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' Run at startup
        Initialise the Client and add it to app.state
    '''
    app.state.mongo_client = init_mongo()
    yield
    ''' Run on shutdown
        Close the connection
        Clear variables and release the resources
    '''
    app.state.mongo_client.close()


app = FastAPI(lifespan=lifespan)

class UserData(BaseModel):
    user_id: str
    user_question: str

@app.post('/chatbot/')
async def chatbot_general(request:Request, user_data: UserData):
    user_id = user_data.user_id
    user_question = user_data.user_question 

    print(request.state.mongo_client)

    answer = generalQuestion(user_question, user_id)
    
    return answer
