# Screenshot Plan

Capture these once the app is running locally (`docker compose up --build`),
save into `docs/screenshots/` with the exact filenames below, and reference
them from the README's Screenshots section.

1. `01-swagger-docs.png` — `/docs` Swagger UI showing both endpoints.
2. `02-upload-request.png` — Swagger "Try it out" for `/documents/upload` with a PDF selected.
3. `03-upload-response.png` — the JSON response showing `pages_processed` / `chunks_created`.
4. `04-chat-question.png` — Swagger "Try it out" for `/chat/ask` with a sample question filled in.
5. `05-chat-answer-with-citations.png` — the JSON response showing the answer + citations array.
6. `06-error-handling.png` — an example error response (e.g. uploading a non-PDF file, showing the 400 response).
7. `07-database-table.png` — a `psql` or DB GUI screenshot showing rows in `langchain_pg_embedding` after ingesting a document.

None of these exist yet — they are TODO once the project is run locally.
