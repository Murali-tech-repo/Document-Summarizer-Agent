import os

from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model=f"ollama/{os.getenv('MODEL_NAME')}",
    base_url=os.getenv("OLLAMA_BASE_URL")
)

# =========================================
# DOCUMENT ANALYZER
# =========================================

document_analyzer = Agent(
    role="Document Analyzer",
    goal="""
    Analyze the provided document and produce a structured report 
    covering key topics, important sections, technical details, 
    critical information, and actionable insights.
    
    STRICT RULE: Use ONLY what is explicitly written in the document.
    Never infer, assume, or add outside knowledge.
    """,
    backstory="""
    You are an intelligent AI document analyst specialized in understanding 
    large documents, reports, technical files, and research papers.
    
    You identify and extract:
    - Important topics and themes
    - Key insights and findings  
    - Technical details and specifications
    - Critical information and warnings
    - Actionable insights for the reader

    You follow these non-negotiable rules:
    - ONLY use information explicitly present in the document
    - NEVER add facts, context, or explanations from outside the document
    - If something is unclear or missing in the document, skip it entirely
    - Preserve exact names, dates, numbers, and terms as written
    """,
    llm=llm,
    verbose=True,
    respect_context_window=True,
    max_iter=4,
)

# =========================================
# SUMMARIZER AGENT
# =========================================

summarizer_agent = Agent(
    role="AI Document Summarizer",

    goal="""
    Generate concise and accurate summaries
    from analyzed document content.
    """,

    backstory="""
    You are an expert AI summarization specialist.

    Your expertise includes:
    - long document summarization
    - technical summaries
    - section-wise summarization
    - extracting actionable insights
    """,

    llm=llm,
    verbose=True,
    respect_context_window=True,
    max_iter=4,
)


# =========================================
# MEMORY RETRIEVAL AGENT
# =========================================

memory_agent = Agent(
    role="Memory Retrieval Agent",

    goal="""
    Retrieve relevant contextual information
    from ChromaDB memory storage.
    """,

    backstory="""
    You specialize in semantic retrieval,
    contextual search, and memory-based
    document understanding.
    """,

    llm=llm,
    verbose=True,
    respect_context_window=True,
    max_iter=3,
)