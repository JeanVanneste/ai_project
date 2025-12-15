import os, inspect, json

from typing import Callable, List

from dotenv import load_dotenv

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI

from .tools import gmaps

MODEL_NAME = "mistral-small-latest"
#MODEL_NAME = "mistral-medium-latest"


class Chatbot:
    tools = [
        gmaps.get_coordinates,
    ]

    def __init__(self):
        load_dotenv(override=True)
        self.llm = ChatMistralAI(
            temperature=0.1,
            model_name=MODEL_NAME
        )
        self.chatbotTools = []
        for tool in Chatbot.tools:
            self.chatbotTools.append(self.build_tool_spec(tool))

        self.llm_with_tools = self.llm.bind_tools(self.chatbotTools)

    def build_tool_spec(self, func: Callable):
        """Build a tool spec dict from a plain python function.
        Assumes all parameters are strings unless type annotation gives something else.
        """
        sig = inspect.signature(func)
        props = {}
        required = []
        for name, param in sig.parameters.items():
            ann = param.annotation
            ann_type = "string"
            if ann in (int, float):
                ann_type = "number"
            props[name] = {"type": ann_type}
            if param.default is inspect._empty:
                required.append(name)
        return {
            "type": "function",
            "function": {
                "name": func.__name__,
                "description": (func.__doc__ or "").strip()[:800],
                "parameters": {
                    "type": "object",
                    "properties": props,
                    "required": required
                }
            }
        }

    def chatbot_creation(self):
        

        self.messages = []

        system_prompt = """
            You are a chatbot that need to assist disabled people to access public transportation in Bruxelles.\n
            You need to understand the needs of the user to give the best assistance.\n
            You have to proactively ask them questions to understand their difficulties and their needs.\n
            When you think you have all the informations needed, say it out loud in the chat.\n
            You ask the first question.\n
            """
        
        prepromt = SystemMessage(system_prompt)
        self.messages.append(prepromt)
        
        answer = self.llm.invoke(self.messages)
        self.messages.append(answer)
        print(f"Answer : {answer.content}")

    def add_user_message(self, message: str):
        self.messages.append(HumanMessage(message))
        answer = self.llm.invoke(self.messages, tools=self.chatbotTools)
        self.messages.append(answer)
        print(f"\n{answer.content}")


if __name__ == "__main__":
    bot = Chatbot()
    print(bot.build_tool_spec(gmaps.get_coordinates))