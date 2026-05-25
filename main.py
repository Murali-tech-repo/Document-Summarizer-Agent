__import__('pysqlite3')

import sys
import os

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from crewai import Crew, Process

from tools.tools import (
    read_pdf,
    chunk_text
)

from vectordb.chroma_store import (
    store_chunks,
    search_chunks
)

from agents.agents import (
    document_analyzer,
    # memory_agent,
    # summarizer_agent
)

from tasks.tasks import (
    analyze_document_task,
    # memory_search_task,
    # summary_task
)

# =========================================
# CONFIG
# =========================================

PDF_FILE = "documents/tour.pdf"

# =========================================
# READ PDF
# =========================================

text = read_pdf(PDF_FILE)

print(text[:1000])

# =========================================
# CHUNKING
# =========================================

chunks = chunk_text(text)

print(f"\nTotal Chunks: {len(chunks)}")

# =========================================
# STORE IN CHROMADB
# =========================================

print("\nStoring chunks into ChromaDB...\n")

store_chunks(chunks)

# =========================================
# MEMORY SEARCH
# =========================================

query = "important topics and summary"

memory_results = search_chunks(query)

retrieved_context = "\n".join(memory_results)

# =========================================
# CREW SETUP
# =========================================

crew = Crew(
    agents=[
        document_analyzer,
        # memory_agent,
        # summarizer_agent
    ],

    tasks=[
        analyze_document_task,
        # memory_search_task,
        # summary_task
    ],

    process=Process.sequential,
    verbose=True
)

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    result = crew.kickoff(
        inputs={
            "document_content": retrieved_context,
            "query": query
        }
    )

    print("\n========== FINAL SUMMARY ==========")
    print(result)