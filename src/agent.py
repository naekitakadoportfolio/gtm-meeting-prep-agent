"""Sales meeting-prep agent.
Retrieves account context, asks an LLM for a STRUCTURED brief, validates it with guardrails,
and falls back to a deterministic summary (human review flag) when the model is unavailable or output is invalid."""
import json, os, sys, re
from pathlib import Path
from retriever import Retriever

SCHEMA_KEYS = {"summary", "risks", "opportunities", "next_actions", "confidence"}
BLOCKED = re.compile(r"\b(guarantee|discount of \d+%|free forever)\b", re.I)  # no promises to customers

def load_account(acc_id):
    accounts = json.loads((Path(__file__).parent.parent / "data/accounts.json").read_text())
    return next(a for a in accounts if a["id"] == acc_id)

def build_prompt(acc, context):
    return f"""You are a sales meeting-prep assistant. Use ONLY the context below.
Return JSON with keys: summary (string), risks (list), opportunities (list), next_actions (list), confidence (0-1).
Account: {acc['name']} | ARR ${acc['arr']:,} | Renewal {acc['renewal_date']} | Open opps: {acc['open_opps']}
Context:\n- """ + "\n- ".join(context)

def call_llm(prompt):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key: return None
    import anthropic
    msg = anthropic.Anthropic(api_key=key).messages.create(
        model=os.getenv("MODEL", "claude-sonnet-4-5"), max_tokens=800,
        messages=[{"role": "user", "content": prompt + "\nRespond with JSON only."}])
    return msg.content[0].text

def validate(raw):
    """Guardrails: valid JSON, required keys, no customer-facing promises, confidence in range."""
    try: data = json.loads(raw[raw.find("{"): raw.rfind("}") + 1])
    except Exception: return None, "invalid_json"
    if not SCHEMA_KEYS <= data.keys(): return None, "missing_keys"
    if BLOCKED.search(json.dumps(data)): return None, "blocked_language"
    if not 0 <= float(data["confidence"]) <= 1: return None, "bad_confidence"
    return data, None

def fallback(acc, context):
    risks = [c for c in context if re.search(r"left|down|escalation|frustrat|evaluating|failure", c, re.I)]
    return {"summary": f"{acc['name']} renews {acc['renewal_date']} at ${acc['arr']:,} ARR.",
            "risks": risks, "opportunities": [o["name"] for o in acc["open_opps"]],
            "next_actions": ["Review risks with account owner before the meeting"],
            "confidence": 0.4, "needs_human_review": True}

def prep(acc_id, focus="risks renewal budget champion"):
    acc = load_account(acc_id)
    context = Retriever(acc["notes"]).search(focus, k=4)
    raw = call_llm(build_prompt(acc, context))
    if raw:
        data, err = validate(raw)
        if data: return data
        print(f"[guardrail] fallback used: {err}", file=sys.stderr)
    return fallback(acc, context)

if __name__ == "__main__":
    print(json.dumps(prep(sys.argv[1] if len(sys.argv) > 1 else "ACC-102"), indent=2))
