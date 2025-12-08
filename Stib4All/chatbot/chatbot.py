from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI

MODEL_NAME = "mistral-small-latest"
#MODEL_NAME = "mistral-medium-latest"


class Chatbot:
    messages = []

    def __init__(self):
        load_dotenv(override=True)
        self.llm = ChatMistralAI(
            temperature=0.1,
            model_name=MODEL_NAME
        )

    def chatbot_creation(self):
        system_prompt = """
            You are a chatbot that need to assist disabled people to access public transportation in Bruxelles.\n
            You need to understand the needs of the user to give the best assistance.\n
            You have to proactively ask them questions to understand their difficulties and their needs.\n
            When you think you have all the informations needed, say it out loud in the chat.\n
            Use the tool available to help the user. If they don't exist, tell the user.\n
            You ask the first question.\n
            """
        
        prepromt = SystemMessage(system_prompt)
        self.messages.append(prepromt)
        
        answer = self.llm.invoke(self.messages)
        self.messages.append(answer)
        print(f"Answer : {answer.content}")

    def add_user_message(self, message: str):
        self.messages.append(HumanMessage(message))
        answer = self.llm.invoke(self.messages)
        print(f"\n{answer.content}")