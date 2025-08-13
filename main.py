from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from services import *
from config import *
from models import *
import os

llm = init_llm()

graph_builder = StateGraph(State)

graph_builder.add_node("summarizer", context_summarizer)
graph_builder.add_edge(START, "summarizer")
graph_builder.add_edge("summarizer", END)

graph = graph_builder.compile()

user_input = input("Enter Message: ")
state = graph.invoke({"messages" : {"role" : "user", "content" : user_input}})


print(state["messages"][-1].content)

