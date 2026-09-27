# Portfolio Content — sohaggain.com

### Project Title
PDF RAG Knowledge Assistant

### One-line description
A citation-grounded RAG chatbot API that answers questions from your own PDF
documents, built with FastAPI, LangChain, and PostgreSQL + pgvector.

### Problem
Teams accumulate large volumes of PDF knowledge that's slow to search and
risky to hand to a generic LLM without a verifiable source for its answers.

### Solution
An API that ingests PDFs into a vector database and constrains an LLM to
answer only from retrieved passages — every claim is traceable to a specific
file and page, reducing hallucination risk.

### Key Features
- PDF upload, chunking, and embedding pipeline
- PostgreSQL + pgvector similarity search
- Citation-grounded, provider-agnostic generation (OpenAI or Anthropic)
- API key auth, rate limiting, structured logging
- Full test suite (unit + integration + optional e2e), Dockerized, CI-tested

### Tech Stack
Python, FastAPI, LangChain, OpenAI, Anthropic Claude, PostgreSQL, pgvector,
Docker, GitHub Actions

### Architecture Summary
PDF → chunk → embed → pgvector store → similarity retrieval → grounded LLM
generation → cited answer. See full architecture diagram in the repository README.

### Business Value
Designed to reduce manual document search time and provide traceable,
source-cited answers for internal knowledge base, contract review, and
support use cases.

### GitHub link
YOUR_GITHUB_URL: https://github.com/sohaggain/pdf-rag-knowledge-assistant

### Live Demo
Not publicly deployed yet.

### Demo Video
To be added after implementation is deployed.

### Project Category
AI Application / RAG Application

### Difficulty
Intermediate–Advanced

### Skills Demonstrated
RAG system design, vector database integration, prompt engineering with
guardrails, provider-agnostic AI architecture, FastAPI backend engineering,
Docker/CI, testing strategy for AI systems.
