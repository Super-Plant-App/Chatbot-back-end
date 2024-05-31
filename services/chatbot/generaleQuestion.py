from .chatbotModel import ChatBotModel
import dotenv 

dotenv.load_dotenv()

def generalQuestion(question: str):
    chatbot = ChatBotModel()
    answer = chatbot.generalQuestion(question)
    # answer = "answer"
    return answer