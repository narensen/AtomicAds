import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def init_reasoning_llm():
    return ChatGroq(
        model="llama3-70b-8192",
        api_key=GROQ_API_KEY,
    )

def init_fast_llm():
    return ChatGroq(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        api_key=GROQ_API_KEY,
    )

def get_search_tool():
    return TavilySearchResults(
        max_results=5,
        api_key=TAVILY_API_KEY
    )