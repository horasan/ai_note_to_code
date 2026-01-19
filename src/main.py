from app_graph.graph import GRAPH_ROUTER
from app_graph.graph_state import WFGraphState
import typer
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os
from openai import OpenAI
from uuid import uuid4
from app_tracing.app_tracing import TracingUtils
from datetime import datetime
from dotenv import load_dotenv

gr = GRAPH_ROUTER
tracing_utils = TracingUtils()
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

#print(gr.get_graph().print_ascii())
USER_NAME = "John"
BOT_NAME = "minusten"
HELLO_MESSAGE = f"Hello! I am {BOT_NAME}, your AI assistant. How can I help you today?"


def typer_main():

    tracing_langfuse_client = tracing_utils.get_tracing_client()
    tracing_langfuse_callback_handler = tracing_utils.get_tracing_callback_handler()
    tracing_trace_id = tracing_utils.get_tracing_trace_id()
    first_run = True
    
    while True:
        
        # Start with new thread_id
        thread_id = str(uuid4())
        wf_config = {
            "configurable": {"thread_id": thread_id},
            "callbacks": [tracing_langfuse_callback_handler]
        }

        if first_run:
            typer.echo(f"{BOT_NAME}: {HELLO_MESSAGE}")
            typer.echo(f"{BOT_NAME}: Enter the parsed meeting notes filepath:")
            parsed_project_file_path = typer.prompt(USER_NAME)
            typer.echo(f"{BOT_NAME}: Enter the local repo path:")
            local_repo_path = typer.prompt(USER_NAME)
            typer.echo(f"{BOT_NAME}: Enter the git repo name:")
            git_repo_name = typer.prompt(USER_NAME)
            first_run = False
        
        # initialize base state with all the elements for WFGraphState
        b_s: WFGraphState = {
            "plan_path": parsed_project_file_path,
            "repo_path": local_repo_path,
            "branch_name": f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{tracing_trace_id}",
            "pr_url":  f"https://{GITHUB_TOKEN}@github.com/horasan/{git_repo_name}",
            "messages": [],
            "state_id": tracing_trace_id
        }

        user_input = typer.prompt(USER_NAME)
        if user_input.lower() in ["exit", "quit"]:
            typer.echo(f"{BOT_NAME}: You can trace the chat with trace_id: {tracing_trace_id} . \nBye ...")
            break
        
        with tracing_langfuse_client.start_as_current_span(
            name=f"{BOT_NAME}-agent",
            trace_context={"trace_id":tracing_trace_id}
            ) as span:
            span.update_trace(input=user_input)

            human_message = HumanMessage(content = user_input)
            b_s["messages"].append(human_message)

            gr_response = gr.invoke(input=b_s, config=wf_config)

            bot_reply = gr_response["messages"][-1].content

            typer.echo(f"{BOT_NAME}: {bot_reply}")

            span.update_trace(input=bot_reply)

if __name__ == "__main__":
    typer.run(typer_main)
