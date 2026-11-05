"""Tiny local retriever: TF-IDF embeddings + cosine similarity + simple re-ranking by recency.
No external services needed, so the demo runs anywhere."""
import math, re
from collections import Counter

def _tokens(t): return re.findall(r"[a-z0-9]+", t.lower())

class Retriever:
    def __init__(self, docs):
        self.docs = docs
        self.df = Counter(w for d in docs for w in set(_tokens(d)))
        self.vecs = [self._vec(d) for d in docs]

    def _vec(self, text):
        tf = Counter(_tokens(text)); n = len(self.docs)
        return {w: c * math.log((n + 1) / (self.df.get(w, 0) + 1) + 1) for w, c in tf.items()}

    @staticmethod
    def _cos(a, b):
        dot = sum(a[w] * b.get(w, 0) for w in a)
        na = math.sqrt(sum(v * v for v in a.values())); nb = math.sqrt(sum(v * v for v in b.values()))
        return dot / (na * nb) if na and nb else 0.0

    def search(self, query, k=3):
        q = self._vec(query)
        scored = [(self._cos(q, v), i) for i, v in enumerate(self.vecs)]
        # re-rank: small boost for more recent notes (docs start with ISO dates)
        scored = [(s + 0.01 * i / max(len(self.docs), 1), i) for s, i in scored]
        return [self.docs[i] for s, i in sorted(scored, reverse=True)[:k] if s > 0]
