from crewai import Task

from agents.agents import (
    document_analyzer,
    summarizer_agent,
    memory_agent
)


# =========================================
# DOCUMENT ANALYSIS TASK
# =========================================

analyze_document_task = Task(
    description="""
    Analyze the document below and produce a structured report.

    STRICT RULES — read before analyzing:
    - Use ONLY information explicitly stated in the document
    - NEVER add outside knowledge, assumptions, or inferences
    - Preserve exact names, dates, numbers, and terms as written
    - If a section has no relevant content in the document, omit it

    DOCUMENT CONTENT:
    {document_content}

    Structure your output exactly as:
    1. Document Overview — what type of document this is and its purpose
    2. Key Topics — main subjects covered
    3. Important Sections — notable parts of the document
    4. Technical Details — specific data, times, dates, specs mentioned
    5. Critical Information — warnings, confirmations, must-know facts
    6. Actionable Insights — what the reader should do or remember
    """,
    expected_output="""
    Title: Structured Document Analysis Report

    Document Overview:
    [What type of document, its purpose, based strictly on document content]

    Key Topics:
    1. [Topic from document]
    2. [Topic from document]

    Important Sections:
    1. [Section name]: [What it covers, from document only]
    2. ...

    Technical Details:
    1. [Specific detail — dates, times, specs, numbers]
    2. ...

    Critical Information:
    1. [Must-know fact or warning from document]
    2. ...

    Actionable Insights:
    1. [What reader should do, strictly from document]
    2. ...
    """,
    agent=document_analyzer
)

# =========================================
# MEMORY SEARCH TASK
# =========================================

memory_search_task = Task(
    description="""
    Search ChromaDB memory for relevant context
    related to the provided query.

    QUERY:
    {query}
    """,

    expected_output="""
    Relevant contextual information.
    """,

    agent=memory_agent
)


# =========================================
# SUMMARY TASK
# =========================================

summary_task = Task(
    description="""
    Generate a concise and accurate summary
    from the analyzed document.

    CONTENT:
    {document_content}
    """,

    expected_output="""
    Professional document summary.
    """,

    agent=summarizer_agent,
    output_file="outputs/summary.md"
)