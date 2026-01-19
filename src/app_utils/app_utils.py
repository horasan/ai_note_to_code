from colorama import Fore, Back, Style
import os

class GeneralUtils:

    @staticmethod
    def print_n_from_left(source:str, msg:str, n:int = 10, for_color:str = Fore.WHITE, back_color:str = Fore.MAGENTA, style: str = Style.BRIGHT) -> str | None:
        print(f"{" " * n} {for_color}{back_color}{style}[{source}] {msg} {Style.RESET_ALL}")
