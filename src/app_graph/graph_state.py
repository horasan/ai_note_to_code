
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Literal
from pydantic import Field
from typing import List, Optional

"""
class WFGraphState(TypedDict):
    messages: Annotated[list, add_messages]
    next_node: Literal["SELF_INFO", "STARWARS", "NONE"] = Field(description="Next node to proceed") # pyright: ignore[reportGeneralTypeIssues]
"""
class PlanTask(TypedDict):
    id: int
    description: str
    status: str  # "pending", "completed", "failed"

class WFGraphState(TypedDict):
    state_id: str
    plan_path: str
    repo_path: str
    #tasks: List[PlanTask]
    #current_task_index: int
    #modified_files: List[str]
    #test_output: Optional[str]
    branch_name: str
    pr_url: Optional[str]
    messages: Annotated[list, add_messages]

