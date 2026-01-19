from colorama import Fore, Back, Style
import os
from datetime import datetime
from langfuse import get_client, Langfuse
from langfuse.langchain import CallbackHandler

class TracingUtils:

    @staticmethod
    def x(source:str, msg:str, n:int = 10, for_color:str = Fore.WHITE, back_color:str = Fore.MAGENTA, style: str = Style.BRIGHT) -> str | None:
        pass
    
    @staticmethod
    def get_tracing_client():
        return get_client()

    @staticmethod
    def get_tracing_trace_id():
        return Langfuse.create_trace_id()
    
    @staticmethod
    def get_tracing_callback_handler():
        return CallbackHandler()