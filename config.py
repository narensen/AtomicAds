import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from models import *

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def init_llm():

    return init_chat_model(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        model_provider="groq",
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com"
    )

def search_tool(query : str):

    return TavilySearch(
    max_results=5,
    topic="general",
    include_answer=False,
)