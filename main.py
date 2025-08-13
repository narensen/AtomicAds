from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from models import State
from services import (
    context_summarizer_node,
    planner_node,
    search_and_fetch_node,
    per_source_summarizer_node,
    synthesis_node,
    save_to_history_node,
)

graph_builder = StateGraph(State)

graph_builder.add_node("context_summarizer", context_summarizer_node)
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("search_and_fetch", search_and_fetch_node)
graph_builder.add_node("per_source_summarizer", per_source_summarizer_node)
graph_builder.add_node("synthesis", synthesis_node)
graph_builder.add_node("save_to_history", save_to_history_node)

graph_builder.add_edge(START, "context_summarizer")
graph_builder.add_edge("context_summarizer", "planner")
graph_builder.add_edge("planner", "search_and_fetch")
graph_builder.add_edge("search_and_fetch", "per_source_summarizer")
graph_builder.add_edge("per_source_summarizer", "synthesis")
graph_builder.add_edge("synthesis", "save_to_history")
graph_builder.add_edge("save_to_history", END)

checkpointer = MemorySaver()

graph = graph_builder.compile(checkpointer=checkpointer)