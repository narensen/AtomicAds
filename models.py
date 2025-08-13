from typing import Annotated, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    
    messages : Annotated[list, add_messages]

class ContextSummarizer(BaseModel):

    message_process : str = Field(
        ...,
        description="Summarize this content without compromising information and nuances"
    )






