# from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import OpenAI, ChatOpenAI
from langchain.chains.llm import LLMChain 
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from Models.ChatbotModel import ChatbotModel
from services.chatbot.CureDB import CureDB
import dotenv

dotenv.load_dotenv()


class ChatBotController:

    def __init__(self, user_id: str, chatbotModel: ChatbotModel):
        self.user_id = user_id
        self.llm = ChatOpenAI(temperature=0)
        self.chatbotModel = chatbotModel

    def __load_chat_history(self):
        history = self.chatbotModel.load_history(self.user_id)

        messages = []
        for i, message in enumerate(history):
            if i % 2 == 0:
                messages.append(SystemMessage(content=message))
            else:
                messages.append(HumanMessage(content=message))

        return messages

            
    def __update_chat_history(self, messages: list):
        # remove the system message from the history
        history = []

        # we will only store the last 8 messages (last 4 user and system messages)
        for message in messages[-8:]:
            history.append(message.content.strip())

        self.chatbotModel.update_history(history, self.user_id)

    def __clear_chat_history(self):
        self.chatbotModel.clear_history(self.user_id)
    
    def classifyQuestion(self, user_question) -> str:
        chat = ChatOpenAI(temperature=0)
        
        messages = [
            SystemMessage(
                content=f"""You are a plant assistant. Your task is to categorize user questions into one of the following categories: ["general question", "plant disease"].
                Choose "general question" if the message is asking anything about plants.
                Choose "plant disease" if the message is specifically asking about a disease of a plant and provoided both disease name and plant name.
                Please return only the category as a string, such as 'general question'.
            """
            ),
            HumanMessage(content=user_question),
        ]

        classification = chat(messages).content

        return classification

    def generalQuestion(self, user_question):
        chat = ChatOpenAI(temperature=0)
        
        messages = self.__load_chat_history()

        messages += [
            SystemMessage(
                content="""
                        You are a helpful AI Plant assistant that answers the questions about Plants and its fields
                        Keep your answer length moderate and help user with his question.
                        """
            ),
            HumanMessage(content=user_question),
        ]

        aiAnswer = chat(messages).content

        messages.append(SystemMessage(content=aiAnswer))

        # remove the template prompt from the messages
        messages.pop(-3)
        self.__update_chat_history(messages)

        return aiAnswer

    def other(self):
        return """
                Sorry, I'm an AI plant assistant. 
                How can I assist you with this categories : ["general question", "plant disease", "other"]
                """

    def translateQuestion(self, user_message):
        chat = ChatOpenAI(temperature=0)

        messages = [
            SystemMessage(
                content=f"""
                    You have only one task, tranlsate the user's message to English.
                    If the user's message is in English return the same message.
                """
            ),
            HumanMessage(
                content=user_message
            )
        ]

        aiAnswer = chat(messages).content

        return aiAnswer
    
    def __getDiseaseAnswer(self, relatedDocs, messages, user_question=None, plantName=None, diseaseName=None):
        chat = ChatOpenAI(temperature=0)
        
        if user_question is None:
            messages += [
                SystemMessage(
                    content=f"""
                        You are a helpful AI Plant assistant that answers the questions about Plants and its fields.
                        You can use Docs to answer the question of user, it is optional to use it

                        ***
                        Docs:
                        {relatedDocs}
                    """
                ),
                HumanMessage(
                    content=f"""
                        What is the cure of {plantName} plant with {diseaseName} disease 
                        """
                )
            ]
        else:
            messages += [
                SystemMessage(
                    content=f"""
                            You are a helpful AI Plant assistant that answers the questions about Plants and its fields.
                            You can use Docs to answer the question of user, it is optional to use it

                            *** 
                            Docs:
                            {relatedDocs}

                            """
                ),
                HumanMessage(content=user_question)
            ]

        aiAnswer = chat(messages).content

        messages.append(SystemMessage(content=aiAnswer))

        return aiAnswer, messages

    def plantDisease(self, user_question):
        messages = self.__load_chat_history()

        translated_question = self.translateQuestion(user_question)

        cure = CureDB()
        relatedDocs, _ = cure.getCureDocsFromPinecone(translated_question)

        aiAnswer, messages = self.__getDiseaseAnswer(relatedDocs, messages, user_question=user_question)

        # remove the template prompt from the messages
        messages.pop(-3)
        self.__update_chat_history(messages)

        return aiAnswer

    def cureResponse(self, plantName, diseaseName, cureDocs, isHealthy):
        if isHealthy:
            return f"""
                    The plant captured in the photo is thriving and identified as a {plantName} Plant. 
                    and I'm pleased to inform you that it is free from any signs of disease.
                """

        template = f"""
                    The user has {plantName} plant with {diseaseName} disease.
                    Give the user a suitable treatment for the disease.
                    You are given a number of documents, use them to make a suitable treatment.
                    If you find a part in documents related to index, ignore it
                    
                    ***

                    Docs:
                    {cureDocs}
                """

        prompt = PromptTemplate(
            template=template, input_variables=["plantName", "diseaseeName", "cureDocs"]
        )
        llm = OpenAI(temperature=0)
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        aiAnswer = llm_chain.invoke(
            plantName=plantName, diseaseName=diseaseName, cureDocs=cureDocs
        )

        self.__update_chat_history(template, aiAnswer)

        return aiAnswer

    """
    The most suitable treatment for late blight disease in potato plants is a combination of several management practices. The first step is to avoid introducing the disease into the field by using disease-free seed tubers and destroying any cull or volunteer potatoes. Planting resistant varieties can also help to prevent the disease from spreading.\n\nIn terms of cultural practices, it is important to maintain good plant health by providing adequate air circulation and removing old vines after harvest. Chemical control can also be effective, with fungicides such as chlorothalonil and maneb being recommended for preventative use. Resistance to the disease can also be achieved by planting resistant cultivars such as Mountain Fresh, Mountain Supreme, and Plum Dandy.\n\nLate blight is caused by the fungus Phytophthora infestans, which can survive in potato tubers over the winter and be reintroduced into the field through infected seed potatoes or tomato transplants. The disease is favored by cool, moist weather and can spread rapidly, causing severe damage to foliage and tubers.\n\nSymptoms of late blight include pale-green, water-soaked spots on the leaf edges or tips, which can quickly expand and turn purplish, brownish, or blackish in color. Infected tubers will have brown, dry, sun
    """

    def chat(self, user_question: str):
        # translate the question to english first
        # user_question = self.translateQuestion(user_question)

        question_type = self.classifyQuestion(user_question)

        if question_type == "general question":
            return self.generalQuestion(user_question)
        elif question_type == "plant disease":
            return self.plantDisease(user_question)
        elif question_type == "other":
            return self.other()
        else:
            return "Sorry, I'm an AI plant assistant. How can I assist you with this categories : general question, plant disease, other"

    def getCure(self, plantName: str, diseaseName: str):
        messages = self.__load_chat_history()

        cure = CureDB()
        relatedDocs, _ = cure.getCureDocsFromPinecone(plantName, diseaseName)

        aiAnswer, messages = self.__getDiseaseAnswer(relatedDocs, messages, plantName=plantName, diseaseName=diseaseName)

        # remove the template prompt from the messages
        messages.pop(-3)
        self.__update_chat_history(messages)

        return aiAnswer

    def clearHistory(self):
        self.__clear_chat_history()
        return "Chat history has been cleared successfully."
    