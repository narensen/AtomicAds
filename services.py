from models import State, ResearchPlan, SourceSummary, FinalBrief
from config import init_reasoning_llm, init_fast_llm, get_search_tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import PydanticOutputFunctionsParser
from langchain_core.utils.function_calling import convert_to_openai_function

user_history_store = {}

def context_summarizer_node(state: State):
    if state.get("follow_up") and state["user_id"] in user_history_store:
        previous_briefs = user_history_store[state["user_id"]]
        context_to_summarize = "\n\n".join(
            [f"Topic: {brief.topic}\nSummary: {brief.synthesis}" for brief in previous_briefs]
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert summarizer. Distill the following past research briefs into a concise summary that can inform a new research task."),
            ("user", "Summarize these past briefs:\n\n{context_to_summarize}")
        ])
        
        summarizer_llm = init_fast_llm()
        chain = prompt | summarizer_llm
        summary = chain.invoke({"context_to_summarize": context_to_summarize}).content
        return {"context_summary": summary}
    
    return {"context_summary": None}

def planner_node(state: State):
    planner_llm = init_reasoning_llm().with_structured_output(ResearchPlan)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research assistant. Create a detailed research plan based on the user's topic. Your plan should include specific, targeted search queries."),
        ("user", "Research Topic: {topic}\n\nContext from past research (if any):\n{context}")
    ])
    
    chain = prompt | planner_llm
    plan = chain.invoke({
        "topic": state["topic"],
        "context": state.get("context_summary", "N/A")
    })
    return {"plan": plan}

def search_and_fetch_node(state: State):
    search_tool = get_search_tool()
    search_queries = state["plan"].search_queries
    search_results = search_tool.batch([{"query": q} for q in search_queries])
    return {"search_results": search_results}

def per_source_summarizer_node(state: State):
    summarizer_llm = init_fast_llm().with_structured_output(SourceSummary)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert content summarizer. For the given source, provide its URL, title, a concise summary, and explain its relevance to the research topic."),
        ("user", "Research Topic: {topic}\n\nSource Content:\n{content}")
    ])
    
    chain = prompt | summarizer_llm
    
    summaries = []
    for result_group in state["search_results"]:
        for result in result_group:
            summary = chain.invoke({
                "topic": state["topic"],
                "content": f"URL: {result['url']}\nTitle: {result.get('title', 'N/A')}\nContent: {result['content']}"
            })
            summaries.append(summary)
            
    return {"source_summaries": summaries}

def synthesis_node(state: State):

    synthesis_llm = init_reasoning_llm()

    final_brief_function = convert_to_openai_function(FinalBrief)

    llm_with_tool = synthesis_llm.bind(
        functions=[final_brief_function],
        function_call={"name": "FinalBrief"}
    )
    
    parser = PydanticOutputFunctionsParser(pydantic_schema=FinalBrief)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research writer. Your task is to synthesize the provided source summaries into a comprehensive and well-structured research brief. Create an introduction and a detailed synthesis of the information. You must call the FinalBrief function with the results."),
        ("user", "Research Topic: {topic}\n\nContext from past research (if any):\n{context}\n\nSummarized Sources:\n{sources}")
    ])
    
    chain = prompt | llm_with_tool | parser
    
    source_str = "\n\n".join(
        [f"URL: {s.url}\nTitle: {s.title}\nSummary: {s.summary}\nRelevance: {s.relevance_to_topic}" for s in state["source_summaries"]]
    )
    
    final_brief = chain.invoke({
        "topic": state["topic"],
        "context": state.get("context_summary", "N/A"),
        "sources": source_str
    })
    
    # The rest of the function remains the same
    final_brief.sources = state["source_summaries"]
    final_brief.context_summary = state.get("context_summary")

    return {"final_brief": final_brief}

def save_to_history_node(state: State):
    user_id = state["user_id"]
    if user_id not in user_history_store:
        user_history_store[user_id] = []
    user_history_store[user_id].append(state["final_brief"])
    return {}