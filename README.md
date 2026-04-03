# Autonomous Research Multi-Agent using LangGraph

An **AI-powered Autonomous Research Agent** built using **LangGraph, LangChain, OpenAI, and Tavily Search API**.

This system automatically researches a topic from the internet by generating search queries, collecting sources, analyzing web pages, summarizing insights, and finally producing a structured research report.

The agent uses a **multi-agent workflow** where each agent performs a specific research task.

---

# Features

• Autonomous topic research  
• AI-generated search queries  
• Real-time web search using Tavily  
• Web content extraction and analysis  
• AI summarization of research materials  
• Structured research report generation  
• Multi-agent workflow using LangGraph  

---

# Agent Workflow

The system consists of **four specialized agents**:

### Planner Agent
Generates multiple search queries related to the research topic.

### Reader Agent
Searches the internet using Tavily API and collects relevant sources.

### Researcher Agent
Loads web pages and extracts key insights from the content.

### Writer Agent
Generates a complete structured research report.

---

# System Architecture

User Input (Research Topic)

↓

Planner Agent  
Generate research queries

↓

Reader Agent  
Search web and collect sources

↓

Researcher Agent  
Read web pages and summarize insights

↓

Writer Agent  
Generate final research report

↓

Final Output

---

# Tech Stack

Python  
LangGraph  
LangChain  
OpenAI GPT-4o-mini  
Tavily Search API  
AsyncIO  
BeautifulSoup (via WebBaseLoader)  
dotenv  

---

