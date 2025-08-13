from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from main import graph
from langgraph.graph import END
from models import FinalBrief
import uuid

app = FastAPI(
    title="Context-Aware Research Brief Generator",
    description="An API for generating evidence-linked research briefs using LangGraph.",
    version="1.0.0"
)

class BriefRequest(BaseModel):
    topic: str = Field(..., example="The future of renewable energy.")
    depth: int = Field(3, ge=1, le=5, example=3)
    follow_up: bool = Field(False, example=False)
    user_id: str = Field(..., example="user-12345")

@app.post("/brief", response_model=FinalBrief, tags=["Research"])
async def create_brief(request: BriefRequest):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "topic": request.topic,
        "depth": request.depth,
        "follow_up": request.follow_up,
        "user_id": request.user_id,
        "messages": [("user", request.topic)]
    }

    try:
        final_state = None
        async for item in graph.astream(initial_state, config=config):
            if END in item:
                final_state = item[END]
        
        if not final_state or 'final_brief' not in final_state:
            raise HTTPException(status_code=500, detail="Failed to generate the final brief.")
            
        return final_state['final_brief']
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)