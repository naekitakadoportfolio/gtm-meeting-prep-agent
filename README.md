<p align="center"><img src="assets/banner.svg" alt="banner" width="100%"></p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.10+-5B3A3A?style=flat-square">
<img src="https://img.shields.io/badge/tests-passing-F2A7C3?style=flat-square">
<img src="https://img.shields.io/badge/data-fictional-FBE3EC?style=flat-square">
<a href="https://sider.ai/agents/web-creator/share/695ea81100a621619985fdfb"><img src="https://img.shields.io/badge/Portfolio-Nae_Kitakado-F4B4CD?style=flat-square"></a>
</p>

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

---
<p align="center"><sub>Built by <b>Nae Kitakado</b>, AI Automation Consultant Â· <a href="https://www.linkedin.com/in/nae-k-203194265">LinkedIn</a> Â· <a href="https://sider.ai/agents/web-creator/share/695ea81100a621619985fdfb">Portfolio</a> Â· open to retainer &amp; part-time consulting</sub></p>
