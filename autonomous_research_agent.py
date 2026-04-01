from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
import asyncio

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from tavily import TavilyClient
from langchain_community.document_loaders import WebBaseLoader 

load_dotenv()

myclient = ChatOpenAI(model="gpt-4o-mini")

tavilyclient = TavilyClient()


def web_search(query: str):

    response = tavilyclient.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    return response["results"]


class ResearchState(TypedDict):

    topic: str
    queries: List[str]
    sources: List[str]
    notes: List[str]
    report: str


# Planner Agent


def planner_agent(state: ResearchState):

    topic = state["topic"]

    prompt = f"Provide 5 search queries for: {topic}. Return ONLY the queries, one per line."

    response = myclient.invoke([HumanMessage(content=prompt)])

    queries = response.content.split("\n\n\n")

    return {"queries": queries}


def planner_agent(state: ResearchState):
    topic = state["topic"]
    prompt = f"Generate 5 distinct search queries to research {topic}. Return ONLY the queries, one per line, no numbers."
    response = myclient.invoke([HumanMessage(content=prompt)])
    # removing extra spaces, numbers if any
    queries = [
        q.strip().lstrip('0123456789. ') 
        for q in response.content.split("\n") 
        if q.strip()
    ]
    return {"queries": queries}

# Reader Agent

def reader_agent(state: ResearchState):

    queries = state["queries"]

    sources = []

    for q in queries:

        print("Printing Queries")

        print(f">: {q}\n\n\n\n")

        results = web_search(q)

        for r in results:
            sources.append(r["url"])

    return {"sources": sources}


# Researcher Agent

async def researcher_agent(state: ResearchState):
    sources = state["sources"]
    notes = []
    
    for url in sources[:3]:
        try:
           
            loader = WebBaseLoader(url)
            docs = await asyncio.to_thread(loader.load)
            content = docs[0].page_content[:4000] # Limiting characters
            
            prompt = f"Summarize key insights from this text: {content}"
            response = await myclient.ainvoke([HumanMessage(content=prompt)])
            notes.append(response.content)
        except Exception as e:
            print(f"Skipping {url} due to error: {e}")
    print(f"Printing research notes>: {notes}")        
    return {"notes": notes}


# Writer Agent


def writer_agent(state: ResearchState):

    topic = state["topic"]

    notes = "\n".join(state["notes"])

    prompt = f"""Write a detailed research report on:{topic} Using these notes:{notes}"""

    response = myclient.invoke([HumanMessage(content=prompt)])

    report = response.content
    print(f"Printing all report here >: {report}\n\n\n\n")

    return {"report": report}


# Graph Workflow


def build_graph():

    builder = StateGraph(ResearchState)

    builder.add_node("planner", planner_agent)

    builder.add_node("reader", reader_agent)

    builder.add_node("researcher", researcher_agent)

    builder.add_node("writer", writer_agent)

    builder.add_edge(START, "planner")

    builder.add_edge("planner", "reader")

    builder.add_edge("reader", "researcher")

    builder.add_edge("researcher", "writer")

    builder.add_edge("writer", END)

    print("building graph\n\n\n")

    return builder.compile()


graph = build_graph()


# Main Research Function

async def research_topic(topic: str):
    initial_state = {
        "topic": topic,
        "queries": [],
        "sources": [],
        "notes": [],
        "report": ""
    }

    print(f"\n🚀 Starting research on: {topic}\n" + "="*50)

    # Use astream to get updates from each node as they finish
    async for event in graph.astream(initial_state):
        for node_name, output in event.items():
            print(f"\n📍 [Node: {node_name}]")
            
            # Custom feedback based on which node just finished
            if node_name == "planner":
                print(f" Generated {len(output['queries'])} search queries.")
            
            elif node_name == "reader":
                print(f" Found {len(output['sources'])} potential sources.")
            
            elif node_name == "researcher":
                print(f" Analysis complete. Summarized top insights.")
            
            elif node_name == "writer":
                print("\n --- FINAL REPORT --- \n")
                print(output["report"])
                print("\n" + "="*50)

if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    asyncio.run(research_topic(topic))