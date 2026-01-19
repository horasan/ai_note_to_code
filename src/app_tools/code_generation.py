import os
import textwrap
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

# 1. Load your API key from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: GOOGLE_API_KEY not found in .env file.")
    exit()

def generate_code_from_plan(plan_content_path: str) -> str:
    # 2. Initialize the model
    # We use 'temperature=0' for coding to ensure output is deterministic and logical
    llm = ChatGoogleGenerativeAI(
        #model="gemini-2.5-flash", 
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0 
    )

    # 3. Define the System and Human prompts (Zero-Filler Version)
    system_prompt = textwrap.dedent("""
        You are a Senior Python Developer AI Agent.
        Return ONLY the raw code. 
        Do NOT include markdown code blocks (no ```python).
        Do NOT include any introductory or concluding text.
        Use strict type hinting and Google-style docstrings.
        Comment out the file name at the top of the code.
    """).strip()

    human_message = "Task: Create a function called 'multiply_two_ints' that takes a and b as integers and returns their product."

    base_dir = Path(__file__).parent.parent.parent / "src" / "self_project_data" / "math_meeting_notes_parsed.json"

    plan_file_full_path = base_dir

    plan_file_full_path = plan_content_path

    # read the plan file and print
    with open(plan_file_full_path, "r") as f:
        plan_content = f.read()

    human_message = f"\n\nHere is the plan in JSON format:\n{plan_content}. \n\nPlease implement the required function as per the plan."


    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    # 4. Invoke the model
    chain = prompt | llm
    try:
        response = chain.invoke({"input": human_message})
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    return response.content

def generate_test_code_from_file(py_file_name: str) -> str:
    # 2. Initialize the model
    # We use 'temperature=0' for coding to ensure output is deterministic and logical
    llm = ChatGoogleGenerativeAI(
        #model="gemini-2.5-flash", 
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0 
    )

    # read the content of the python file
    with open(py_file_name, "r") as f:
        file_content = f.read()
    

    system_prompt = textwrap.dedent("""
        You are a Senior Python Developer AI Agent.
        Return ONLY the raw code. 
        Do NOT include markdown code blocks (no ```python).
        Do NOT include any introductory or concluding text.
        Use strict type hinting and Google-style docstrings.
    """).strip()


    simple_file_name = os.path.basename(py_file_name)

    human_message = f"""
    You are provided with the following Python code:
    {file_content}
    
    The file name:
    {simple_file_name}
    
    Please generate a comprehensive set of unit tests for this code using the unittest framework.
    Ensure that the tests cover all functions and possible edge cases.

    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    # 4. Invoke the model
    chain = prompt | llm
    try:
        response = chain.invoke({"input": human_message})
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    
    return response.content