# AI Architecture

## Models

| Purpose | Provider | Model | Notes |
|---|---|---|---|
| Embeddings | OpenAI | `text-embedding-3-small` | 1536 dimensions, used for both ingestion and query embedding |
| Generation | OpenAI or Anthropic | `gpt-4o-mini` or `claude-sonnet-4-6` | Selected via `PRIMARY_LLM_PROVIDER` |

## Prompt Strategy

A fixed system prompt (`prompts/system_prompt.txt`) establishes the model's
role and constraints once; the per-request user prompt
(`generation/prompt_builder.py::build_user_prompt`) injects the retrieved
context and the user's question. Separating these lets the system prompt be
reviewed/audited independently of any single request.

## Context Strategy

Retrieved chunks are formatted as explicitly numbered excerpts:
```text
[Excerpt 1 - handbook.pdf, p.7]
<chunk text>

[Excerpt 2 - handbook.pdf, p.12]
<chunk text>
```
This format was chosen so the model can attribute claims to a specific
excerpt/page rather than blending sources ambiguously.

## Tool Calling / Structured Output

Not used in v0.1 — generation is plain text with an expected citation format.
`ChatResponse`'s `citations` list is derived from the retrieval layer's
metadata (source file, page, score), **not** parsed out of the LLM's free text,
which avoids relying on the model to format structured data correctly.

## Memory

Stateless per-request — no conversation history is maintained across calls.
Each `/chat/ask` call is independent. Multi-turn conversational memory is a
natural extension (see Future Improvements).

## Guardrails

- System prompt forbids outside knowledge and requires citations.
- System prompt instructs the model to treat retrieved document text as data,
  not instructions (partial mitigation for prompt injection via malicious PDFs).
- If retrieval returns zero chunks above the relevance threshold, the LLM is
  never called — the API returns a fixed "not enough information" message.
  This avoids paying for and receiving a hallucinated answer with no
  supporting context.

## Evaluation

Not yet implemented as an automated harness. Manual evaluation approach:
compare returned citations' page numbers against the actual source PDF to
confirm the answer is grounded. An automated evaluation harness (e.g.
retrieval precision/recall against a labeled question set, or LLM-as-judge
faithfulness scoring) is listed under Future Improvements.
