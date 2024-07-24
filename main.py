from pydantic import BaseModel
from services.chatbot.generaleQuestion import chatbotAskQuestion, chatbotGetCure
from fastapi import FastAPI, APIRouter, HTTPException
from contextlib import asynccontextmanager
from Models.ChatbotModel import ChatbotModel
from Models.AuthenticationModel import AuthModel

data = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    data['chatbotModel'] = ChatbotModel()
    data['authModel'] = AuthModel()

    yield

    data.clear()


app = FastAPI(
    docs_url="/chatbot/docs",    # Customize Swagger UI
    redoc_url="/chatbot/redoc",
    lifespan=lifespan
)
# router = APIRouter(prefix="/chatbot")

class UserQuestion(BaseModel):
    user_id: str | None
    user_question: str

@app.get('/chatbot')
def home():
    return "Chatbot home page"

@app.post('/chatbot/ask-question')
async def chatbot_general(user_data: UserQuestion):
    chatbotModel = data['chatbotModel']

    user_question = user_data.user_question 
    # user_id = user_data.user_id
    user_id = "665f995565bb190409468564"
    
    answer = chatbotAskQuestion(user_question, user_id, chatbotModel)
    
    return answer

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
    
    return answer

# class ClearData(BaseModel):
    # user_id: str

@app.post('/chatbot/clear-history')
async def clear_history_route():
    chatbotModel = data['chatbotModel']

    # user_id = clearData.user_id
    user_id = "665f995565bb190409468564"

    return chatbotModel.clear_history(user_id)

class UserData(BaseModel):
    email: str
    password: str

@app.post('/api/login')
def login_route(user_data: UserData):
    try:
        # take the email and password
        email = user_data.email
        password = user_data.password
        
        # should return the user id
        authModel = data['authModel']

        res = authModel.login(email, password)

        if res == "Wrong Credentials":
            raise HTTPException(status_code=401, detail=res)
        else:
            return res
        
    except Exception as e:
        print(f"Error in Login: {e}")
        raise HTTPException(status_code=500, detail=f"Error in Login")
    print(res)
   

@app.post('/api/signup')
def signup_route(user_data: UserData):
   
    try:
        # take the email and password
        email = user_data.email
        password = user_data.password
        
        # should return the user id
        authModel = data['authModel']

        res = authModel.signup(email, password)
        
        if res == "User Already Exists":
            raise HTTPException(status_code=401, detail=res)
        else:
            return res
    except Exception as e:
        print(f"Error in SignUp: {e}")
        raise HTTPException(status_code=500, detail=f"Error in SignUp")


# @app.get('/api/history')
# async def history_route(history_data: HistoryData):
#     # takes the user id
#     user_id = history_data.user_id
#     # return the user history

#     # todo: search for a way to store the user scan
#     pass