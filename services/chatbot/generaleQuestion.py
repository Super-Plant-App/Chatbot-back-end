from .chatbotModel import ChatBotModel
import dotenv 

dotenv.load_dotenv()

def generalQuestion(user_question: str, user_id: str):
    chatbot = ChatBotModel(user_id)
    answer = chatbot.chat(user_question)

    return answer