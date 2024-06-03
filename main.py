from fastapi import FastAPI
from pydantic import BaseModel
from services.chatbot.getCure import getCure
from services.chatbot.generaleQuestion import generalQuestion


app = FastAPI()
class UserData(BaseModel):
    user_id: str
    user_question: str

@app.post('/chatbot/')
async def chatbot_general(user_data: UserData):
    user_id = user_data.user_id
    user_question = user_data.user_question 

    answer = generalQuestion(user_question, user_id)
    
    return answer
