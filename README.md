# Context-Aware Research Brief Generator

This project is a sophisticated, context-aware research assistant that generates structured, evidence-linked research briefs. It is built using LangChain for interacting with LLMs and tools, and LangGraph for orchestrating the complex workflow. The application supports follow-up queries by maintaining user history and exposes its functionality through both a REST API and a Command-Line Interface.

[cite_start]This implementation is a response to the "Gen AI Developer Assignment"[cite: 1].


## Problem Statement and Objective

[cite_start]The primary objective is to design and implement a research assistant system that generates structured, evidence-linked research briefs in response to user topics[cite: 3]. The system must be able to handle conversational context, meaning it can process follow-up questions by summarizing prior interactions and incorporating that context into new research[cite: 4].

[cite_start]The core of the system is a multi-step workflow orchestrated by LangGraph[cite: 5], with strict schema enforcement using Pydantic for all outputs to ensure reliability and predictability[cite: 6]. The final application must be accessible via a deployed HTTP API and a local CLI[cite: 7].

## Graph Architecture

The application's logic is orchestrated as a directed acyclic graph (DAG) using LangGraph. Each node in the graph represents a distinct processing step, passing its output to the next node in a well-defined state object[cite: 10].

### Visual Representation (Mermaid Syntax)

```mermaid
graph TD
    A[Start] --> B(context_summarizer)
    B --> C(planner)
    C --> D(search_and_fetch)
    D --> E(per_source_summarizer)
    E --> F(synthesis)
    F --> G(save_to_history)
    G --> H[End]

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#ccf,stroke:#333,stroke-width:2px
    style E fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#f9f,stroke:#333,stroke-width:2px
    style G fill:#9cf,stroke:#333,stroke-width:2px
