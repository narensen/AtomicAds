import typer
from main import graph
from langgraph.graph import END
import asyncio
import uuid
import json

app = typer.Typer()

@app.command()
def run(
    topic: str = typer.Argument(..., help="The research topic."),
    user_id: str = typer.Option(..., "--user-id", "-u", help="A unique identifier for the user."),
    depth: int = typer.Option(3, "--depth", "-d", help="The number of search results to analyze."),
    follow_up: bool = typer.Option(False, "--follow-up", help="Flag if this is a follow-up query to use context."),
):
    print(f"Starting research for topic: '{topic}' for user: '{user_id}'")

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "topic": topic,
        "depth": depth,
        "follow_up": follow_up,
        "user_id": user_id,
        "messages": [("user", topic)]
    }
    
    async def invoke_graph():
        final_state = None
        async for item in graph.astream(initial_state, config=config):
            node_name = list(item.keys())[0]
            print(f"--- Executing Node: {node_name} ---")
            if END in item:
                final_state = item[END]
        return final_state

    result = asyncio.run(invoke_graph())

    if result and result.get('final_brief'):
        print("\n--- FINAL RESEARCH BRIEF ---")
        print(result['final_brief'].json(indent=2))
    else:
        print("\n--- FAILED TO GENERATE BRIEF ---")
        print(result)

if __name__ == "__main__":
    app()