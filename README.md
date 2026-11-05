# GTM Meeting-Prep Agent

An AI agent that gets sales reps ready for account meetings in seconds. It pulls the most relevant account notes, asks an LLM for a **structured brief** (summary, risks, opportunities, next actions, confidence), checks the output against **guardrails**, and **hands off to a human** when it can't trust the result.

> All data here is fictional. Built as a portfolio demo by Nae Kitakado.

## Why it matters
Reps spend 15–30 minutes per meeting reading CRM notes, tickets and emails. This agent cuts that to a single command and shows its sources, so managers can trust what reps walk in with.

## What it demonstrates
| Skill | Where |
|---|---|
| Retrieval / knowledge grounding (embeddings, cosine similarity, re-ranking) | `src/retriever.py` |
| Prompt design + structured JSON output | `src/agent.py` → `build_prompt`, `validate` |
| Production guardrails (schema check, blocked customer-facing language, confidence range) | `validate()` |
| Failure handling + human-in-the-loop fallback | `fallback()` sets `needs_human_review` |
| Tests | `tests/test_agent.py` |

## Run it
```bash
pip install -r requirements.txt
python src/agent.py ACC-102          # works offline using the fallback path
export ANTHROPIC_API_KEY=...         # optional: use Claude for the full brief
python src/agent.py ACC-101
pytest -q
```

## Example output (offline mode)
```json
{
  "summary": "Brightline Logistics renews 2026-12-15 at $96,000 ARR.",
  "risks": ["2026-11-03 Email: Champion Dev Patel left the company.", "..."],
  "needs_human_review": true
}
```

## Production next steps
Swap the TF-IDF retriever for a vector database, pull notes live from Salesforce/HubSpot, and log every brief so adoption and accuracy can be measured.
