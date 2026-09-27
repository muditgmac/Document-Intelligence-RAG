# LinkedIn Project Description

Just shipped: PDF RAG Knowledge Assistant — a Retrieval-Augmented Generation
API that answers questions from your own PDF documents, with every claim
cited back to a specific file and page.

**Problem:** generic LLM chat can't safely or verifiably answer questions
from private PDF knowledge — contracts, handbooks, manuals.

**Solution:** an ingestion pipeline (chunking + embeddings) backed by
PostgreSQL + pgvector, feeding a provider-agnostic generation layer (OpenAI
or Anthropic Claude) that's instructed to answer only from retrieved context
and cite its sources.

**Stack:** Python, FastAPI, LangChain, PostgreSQL/pgvector, Docker, GitHub Actions CI.

Fully tested, containerized, and documented — code + architecture on GitHub:
YOUR_GITHUB_URL: https://github.com/sohaggain/pdf-rag-knowledge-assistant

#AIEngineering #RAG #LangChain #Python #FastAPI #AIAutomation
