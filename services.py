from typing_extensions import TypedDict
from typing import Annotated, Literal
from models import *
from config import *


llm = init_llm()

def context_summarizer(state: State):
    last_message = state['messages'][-1]
    user_content = last_message.content
    
    llm_structured = llm.with_structured_output(ContextSummarizer)
    
    result = llm_structured.invoke([
        {
            "role": "system",
            "content": "Reduce and summarize the Content"
        },
        {
            "role": "user",
            "content": user_content
        }
    ])
    
    return {"messages": [{"role": "assistant", "content": result.message_process}]}


