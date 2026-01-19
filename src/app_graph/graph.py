from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from app_graph.nodes import NODE_GATE_OPENER, NODE_PARSE_PLAN, NODE_CREATE_BRANCH, NODE_AGENT_CODER, NODE_VALIDATE_BUILD, NODE_PUSH_AND_PULL_REQUEST, NODE_AGENT_CODER_TEST, NODE_RUN_UNIT_TESTS

from app_graph.graph_state import WFGraphState

in_mem_checkpointer = InMemorySaver()

graph_with_router_builder = StateGraph(WFGraphState)


graph_with_router_builder.add_node("NODE_GATE_OPENER", NODE_GATE_OPENER);
graph_with_router_builder.add_node("NODE_PARSE_PLAN", NODE_PARSE_PLAN);
graph_with_router_builder.add_node("NODE_CREATE_BRANCH", NODE_CREATE_BRANCH);
graph_with_router_builder.add_node("NODE_AGENT_CODER", NODE_AGENT_CODER);
graph_with_router_builder.add_node("NODE_VALIDATE_BUILD", NODE_VALIDATE_BUILD);
graph_with_router_builder.add_node("NODE_PUSH_AND_PULL_REQUEST", NODE_PUSH_AND_PULL_REQUEST);
graph_with_router_builder.add_node("NODE_AGENT_CODER_TEST", NODE_AGENT_CODER_TEST);
graph_with_router_builder.add_node("NODE_RUN_UNIT_TESTS", NODE_RUN_UNIT_TESTS);

graph_with_router_builder.add_edge(START, "NODE_GATE_OPENER")
graph_with_router_builder.add_edge("NODE_GATE_OPENER", "NODE_PARSE_PLAN")
graph_with_router_builder.add_edge("NODE_PARSE_PLAN", "NODE_CREATE_BRANCH")
graph_with_router_builder.add_edge("NODE_CREATE_BRANCH", "NODE_AGENT_CODER")
graph_with_router_builder.add_edge("NODE_AGENT_CODER", "NODE_VALIDATE_BUILD")
graph_with_router_builder.add_edge("NODE_VALIDATE_BUILD", "NODE_AGENT_CODER_TEST")
graph_with_router_builder.add_edge("NODE_AGENT_CODER_TEST", "NODE_RUN_UNIT_TESTS")
graph_with_router_builder.add_edge("NODE_RUN_UNIT_TESTS", "NODE_PUSH_AND_PULL_REQUEST")

graph_with_router_builder.add_edge("NODE_PUSH_AND_PULL_REQUEST", END)

GRAPH_ROUTER = graph_with_router_builder.compile(checkpointer=in_mem_checkpointer)














