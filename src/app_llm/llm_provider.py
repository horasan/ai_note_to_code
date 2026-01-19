from dotenv import load_dotenv
import os
from openai import OpenAI
import getpass
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import Optional
from typing import TypedDict, Annotated, Literal

class NodeRouterOutput(BaseModel):
    """This class is the output structure for NODE_ROUTER"""
    user_intent: Literal["SELF_INFO", "STARWARS", "NONE"] = Field(description="User intent in the user query.")

class LLMProvider:

    llm_client = None
    llm_client_for_node_router = None

    def __init__(self) -> None:
        self.prepare_llm_client()
        self.prepare_llm_client_for_node_router()
 

    def prepare_llm_client(self):
        load_dotenv()

        OpenAI_API_KEY = os.getenv("OPENAI_API_KEY")

        if not OpenAI_API_KEY:
            raise ValueError("OpenAI_API_KEY is not set in the .env file.")

        self.llm_client = init_chat_model("gpt-4o-mini", model_provider="openai")

    def prepare_llm_client_for_node_router(self):
        load_dotenv()

        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OpenAI_API_KEY is not set in the .env file.")

        llm_chat_model = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.llm_client_for_node_router = llm_chat_model.with_structured_output(NodeRouterOutput)


    def get_llm_client_for_node_router(self):
        return self.llm_client_for_node_router


    def get_expensive_llm_client(self):
        return self.llm_client
    
    def get_cheap_llm_client(self):
        """Assume this one is cheap!"""
        return self.llm_client


