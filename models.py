from typing import Annotated, List, TypedDict, Optional
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

class ResearchPlan(BaseModel):
    topic: str = Field(description="The original research topic.")
    search_queries: List[str] = Field(description="A list of targeted search queries for the web.")
    research_steps: List[str] = Field(description="A step-by-step plan for the research process.")

class SourceSummary(BaseModel):
    url: str = Field(description="The URL of the source.")
    title: str = Field(description="The title of the source.")
    summary: str = Field(description="A concise summary of the source's content.")
    relevance_to_topic: str = Field(description="A brief explanation of why this source is relevant to the topic.")

class FinalBrief(BaseModel):
    topic: str = Field(description="The research topic provided by the user.")
    introduction: str = Field(description="A brief introduction to the research topic.")
    synthesis: str = Field(description="A detailed synthesis of information from all sources, structured into a coherent narrative.")
    sources: List[SourceSummary] = Field(description="A list of all the summarized sources.")
    context_summary: Optional[str] = Field(None, description="A summary of previous interactions if this was a follow-up query.")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    topic: str
    depth: int
    follow_up: bool
    context_summary: Optional[str]
    plan: Optional[ResearchPlan]
    search_results: Optional[List[dict]]
    source_summaries: Optional[List[SourceSummary]]
    final_brief: Optional[FinalBrief]