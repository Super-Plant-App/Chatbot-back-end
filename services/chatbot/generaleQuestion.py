from Models.ChatbotModel import ChatbotModel
from Controllers.ChatbotController import ChatBotController
import dotenv 

dotenv.load_dotenv()

def generalQuestion(user_question: str, user_id: str, chatbotModel: ChatbotModel):
    chatbot = ChatBotController(user_id, chatbotModel)
    answer = chatbot.chat(user_question)

    return answer