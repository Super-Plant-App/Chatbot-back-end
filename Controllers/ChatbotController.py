from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import OpenAI, ChatOpenAI
from Models.ChatbotModel import ChatbotModel
from services.chatbot.CureDB import CureDB
import tiktoken
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
        history = []

        for message in messages:
            history.append(message.content.strip())

        self.chatbotModel.update_history(history, self.user_id)

    def __clear_chat_history(self):
        self.chatbotModel.clear_history(self.user_id)
    
    def __count_tokens(chain, query):
        encoding = tiktoken.get_encoding("cl100k_base")
        result = 0
        # todo: implment this function
        return result

    def getResponseType(self, user_question) -> str:
        template = f"""
                    You are a plant assistant, and your task is to classify user questions. 
                    Please categorize the following question into one of the categories from this list: {user_question} - ["general question", "cure of disease", "other"].
                    For example:
                    - If the question is "What is the Apple?","How can I plant a Tomato?", it should be classified as 'general question'.
                    - If the question is "What is the apple black rot?", it should be classified as 'general question'.
                    - If the question is "What is the cure of Apple black rot?", it should be classified as 'cure of disease'.
                    - If the question is "What is the football? Who is Mohamed Salah?", it should be classified as 'other'.
                    just return the value os a string like 'general question'
                """
        prompt = PromptTemplate.from_template(template=template)
        # question_prompt = prompt.format(user_question)
        llm = OpenAI(temperature=0)
        LLMChain = LLMChain(llm=llm, prompt=prompt)
        ret = LLMChain.invoke({"user_question": user_question})
        return ret
    
    def classifyQuestion(self, user_question) -> str:
        chat = ChatOpenAI(temperature=0)
        
        messages = [
            SystemMessage(
                content=f"""You are a plant assistant. Your task is to categorize user questions into one of the following categories: ["general question", "cure of disease", "other"].
                Choose "cure of disease" if the message is specifically asking about the cure of a plant disease.
                Choose "general question" if the message is asking anything about plants, including questions about diseases that do not ask for a cure.
                Choose "other" if the message is about anything unrelated to plants.
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

        if messages is not None and len(messages) == 0:
            messages = [
                SystemMessage(
                    content="""
                            You are a helpful AI Plant assistant that answers the questions about Plants and its fields
                            but any other field outside the plant or the agriculture don't response and say 
                            Sorry I'm an AI plant assistant.
                            """
                ),
                HumanMessage(content=user_question),
            ]
        else:
            messages.append(HumanMessage(content=user_question))

        aiAnswer = chat(messages).content

        messages.append(SystemMessage(content=aiAnswer))

        self.__update_chat_history(messages)

        return aiAnswer

    def other(self):
        return """
                Sorry, I'm an AI plant assistant. 
                How can I assist you with this categories : ["general question", "cure of disease", "other"]
                """

    def cureOfDisease(self, plantName, diseaseName, hisotry):
        cure = CureDB()
        matchingPagesContent, bol, total_tokens = cure.getCureDocs(plantName, diseaseName)
        return matchingPagesContent

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
    
    def summarize(self , text):
        template = f"""
                Write a well-designed summary with steps based on\
                what you can understand from this {text} to give the user the steps of cure from the management section
                """
        prompt = PromptTemplate(template=template,
                                input_variables=["text"],
                                )
        llm = OpenAI(temperature=0)
        llmChain = LLMChain(prompt=prompt , llm =llm)
        res = llmChain.invoke(
            text=text
        )
        return res

    """
    The most suitable treatment for late blight disease in potato plants is a combination of several management practices. The first step is to avoid introducing the disease into the field by using disease-free seed tubers and destroying any cull or volunteer potatoes. Planting resistant varieties can also help to prevent the disease from spreading.\n\nIn terms of cultural practices, it is important to maintain good plant health by providing adequate air circulation and removing old vines after harvest. Chemical control can also be effective, with fungicides such as chlorothalonil and maneb being recommended for preventative use. Resistance to the disease can also be achieved by planting resistant cultivars such as Mountain Fresh, Mountain Supreme, and Plum Dandy.\n\nLate blight is caused by the fungus Phytophthora infestans, which can survive in potato tubers over the winter and be reintroduced into the field through infected seed potatoes or tomato transplants. The disease is favored by cool, moist weather and can spread rapidly, causing severe damage to foliage and tubers.\n\nSymptoms of late blight include pale-green, water-soaked spots on the leaf edges or tips, which can quickly expand and turn purplish, brownish, or blackish in color. Infected tubers will have brown, dry, sun

    """

    def chat(self, user_question: str):
        question_type = self.classifyQuestion(user_question)

        if question_type == "general question":
            return self.generalQuestion(user_question)
        elif question_type == "cure of disease":
            return self.cureOfDisease(user_question)
        elif question_type == "other":
            return self.other()
        else:
            return "Sorry, I'm an AI plant assistant. How can I assist you with this categories : ['general question', 'cure of disease', 'other']"

    def clearHistory(self):
        self.__clear_chat_history()
        return "Chat history has been cleared successfully."
    