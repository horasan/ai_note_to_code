from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app_graph.graph_state import WFGraphState
from app_utils.app_utils import GeneralUtils
from app_llm.llm_provider import LLMProvider
from app_prompts.prompt_provider import ROUTER_SYSTEM_PROMT, SELF_INFO_SYSTEM_PROMT, STARWARS_SYSTEM_PROMT
from pathlib import Path
from app_tools.git_ops import checkout_new_local_branch, create_local_temp_file, commit_changes_and_push, create_pull_request
from app_tools.code_generation import generate_code_from_plan, generate_test_code_from_file
from datetime import datetime
import subprocess
import sys

utils = GeneralUtils()
llmProvider = LLMProvider()


def NODE_GATE_OPENER(state: WFGraphState):
    utils.print_n_from_left(source = "NODE_GATE_OPENER", msg = "NODE_GATE_OPENER executed.")
    # from LLM
    no_topic_response_text = "State is initialized."

    base_dir = Path(__file__).parent.parent

    plan_file_full_path = base_dir / state["plan_path"]

    no_topic_response = AIMessage(content = no_topic_response_text)

    existing_messages = state["messages"]
    updated_messages = existing_messages + [no_topic_response]
    new_state = {
        "messages": updated_messages,
        "plan_path": state["plan_path"],
        "repo_path": state["repo_path"],
        "branch_name": state["branch_name"],
        "pr_url": state["pr_url"]
    }
    return new_state

def NODE_PARSE_PLAN(state: WFGraphState):
    utils.print_n_from_left(source = "NODE_PARSE_PLAN", msg = "NODE_PARSE_PLAN executed.")
    # from LLM
    no_topic_response_text = "Mimicked plan parsing completed."
   
    no_topic_response = AIMessage(content = no_topic_response_text)

    existing_messages = state["messages"]
    updated_messages = existing_messages + [no_topic_response]
    new_state = {"messages": updated_messages}
    return new_state

def NODE_CREATE_BRANCH(state: WFGraphState):
    utils.print_n_from_left(source = "NODE_CREATE_BRANCH", msg = "NODE_CREATE_BRANCH executed.")
    # from LLM
    no_topic_response_text = "Branch is created."

    repo_path = state["repo_path"]

    branch_name = state["branch_name"]
    pr_url = state["pr_url"]

    created_branch_name = checkout_new_local_branch(in_local_repo_path=repo_path, branch_name=branch_name, pr_url=pr_url)
    utils.print_n_from_left(source = "NODE_CREATE_BRANCH", msg = f"Created Branch Name: {created_branch_name}")
    
    updated_messages = state["messages"]
    new_state = {"messages": updated_messages}
    return new_state

def NODE_AGENT_CODER(state: WFGraphState):
    utils.print_n_from_left(source = "NODE_AGENT_CODER", msg = "NODE_AGENT_CODER executed.")
    src_directory_path = Path(__file__).parent.parent / "self_project_data"

    # from LLM
    no_topic_response_text = "Agent Coder is working."

    full_plan_path = src_directory_path /state["plan_path"]

    generated_code = generate_code_from_plan( plan_content_path = full_plan_path)    

    state_id = state["state_id"]

    #file_name = f"math_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{state_id}.py"
    file_name = f"math_core.py"
    file_src_directory_path = src_directory_path / "math_project" / file_name

    generated_file_name = create_local_temp_file(file_path = file_src_directory_path, content = generated_code)


    no_topic_response = AIMessage(content = no_topic_response_text)

    existing_messages = state["messages"]
    updated_messages = existing_messages + [no_topic_response]
    new_state = {"messages": updated_messages}
    return new_state


def NODE_VALIDATE_BUILD(state: WFGraphState):
    utils.print_n_from_left(source = "NODE_VALIDATE_BUILD", msg = "NODE_VALIDATE_BUILD executed.")
    # from LLM
    no_topic_response_text = "Build is validated."

    no_topic_response = AIMessage(content = no_topic_response_text)

    existing_messages = state["messages"]
    updated_messages = existing_messages + [no_topic_response]
    new_state = {"messages": updated_messages}
    return new_state

def NODE_AGENT_CODER_TEST(state: WFGraphState):
    utils.print_n_from_left(source = "NODE_AGENT_CODER_TEST", msg = "NODE_AGENT_CODER_TEST executed.")
    src_directory_path = Path(__file__).parent.parent / "self_project_data"
    state_id = state["state_id"]

    # from LLM
    no_topic_response_text = "Agent Test Coder is working."

    py_file_name = src_directory_path / "math_project" / "math_core.py"
    
    generated_test_code = generate_test_code_from_file(py_file_name = py_file_name)
    
    py_test_file_name = src_directory_path / "math_project" / "math_core_test.py"
  
    generated_file_name = create_local_temp_file(file_path = py_test_file_name, content = generated_test_code)

    no_topic_response = AIMessage(content = no_topic_response_text)

    existing_messages = state["messages"]
    updated_messages = existing_messages + [no_topic_response]
    new_state = {"messages": updated_messages}
    return new_state

def NODE_RUN_UNIT_TESTS(state: WFGraphState):
    utils.print_n_from_left(source = "NODE_RUN_UNIT_TESTS", msg = "NODE_RUN_UNIT_TESTS executed.")
    src_directory_path = Path(__file__).parent.parent / "self_project_data"
    state_id = state["state_id"]
  
    no_topic_response_text = "Agent Test Runneris working."

    py_file_name = src_directory_path / "math_project" / "math_core.py"
    
    py_test_file_name = src_directory_path / "math_project" / "math_core_test.py"
  
    # sys.executable points to the current running python.exe
    result = subprocess.run(
        [sys.executable, "-m", "pytest", py_test_file_name, "--verbose"],
        capture_output=True, 
        text=True
    )
    
    """
    if result.returncode == 0:
        return True, result.stdout
    else:
        return False, f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    """

    no_topic_response = AIMessage(content = f"{no_topic_response_text} Test Results: {result.returncode}")

    existing_messages = state["messages"]
    updated_messages = existing_messages + [no_topic_response]
    new_state = {"messages": updated_messages}
    return new_state

def NODE_PUSH_AND_PULL_REQUEST(state: WFGraphState):
    utils.print_n_from_left(source = "NODE_PUSH_AND_PULL_REQUEST", msg = "NODE_PUSH_AND_PULL_REQUEST executed.")
    # from LLM
    no_topic_response_text = "NODE_PUSH_AND_PULL_REQUEST executed."
    
    commit_changes_and_push(commit_message="Automated commit by AI agent.")

    branch_name = state["branch_name"]

    create_pull_request(branch_name=branch_name, title="Automated commit by AI agent.", body="Automated commit by AI agent.")

    no_topic_response = AIMessage(content = no_topic_response_text)

    existing_messages = state["messages"]
    updated_messages = existing_messages + [no_topic_response]
    new_state = {"messages": updated_messages}
    return new_state
