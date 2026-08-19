"""
Content-similarity message grouping.

Groups ads (active and inactive) that carry the *same message* even when the
wording differs, so we can measure how long a message has really been running.
This replaces exact-keyword matching with TF-IDF cosine similarity: each ad
becomes a vector weighted by how distinctive its words are, and two ads are the
same message if their vectors point in nearly the same direction.

It is not deep-neural semantics (that needs a model or an API); it is a
self-contained, transparent step up from "does this exact phrase appear."
"""

from __future__ import annotations

import math
import re

import numpy as np

_STOP = set("a an the and or of to for with in on your you our we is are be it "
            "that this so as at by from into out up down not no more less".split())


def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", (text or "").lower())
            if t not in _STOP and len(t) > 2]


def _tfidf(docs: list[str]) -> np.ndarray:
    """Rows = documents, unit-normalized TF-IDF vectors."""
    toks = [_tokens(d) for d in docs]
    df: dict[str, int] = {}
    for t in toks:
        for w in set(t):
            df[w] = df.get(w, 0) + 1
    vocab = {w: i for i, w in enumerate(df)}
    n = len(docs)
    idf = np.array([math.log((n + 1) / (df[w] + 1)) + 1.0 for w in vocab])
    mat = np.zeros((n, len(vocab)), dtype=np.float32)
    for r, t in enumerate(toks):
        if not t:
            continue
        for w in t:
            mat[r, vocab[w]] += 1.0
        mat[r] /= len(t)                 # term frequency
    mat *= idf                            # inverse document frequency
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return mat / norms


def cluster(docs: list[str], threshold: float = 0.45) -> list[int]:
    """Greedy single-pass clustering by cosine similarity.

    Each doc joins the most similar existing cluster whose seed it exceeds the
    threshold with; otherwise it starts a new cluster. Returns a cluster id per
    doc. Order-dependent but fast and good enough to chain re-issued versions of
    one message together.
    """
    if not docs:
        return []
    m = _tfidf(docs)
    seeds: list[int] = []
    labels = [-1] * len(docs)
    for i in range(len(docs)):
        best_c, best_sim = -1, threshold
        for ci, si in enumerate(seeds):
            sim = float(m[i] @ m[si])
            if sim >= best_sim:
                best_sim, best_c = sim, ci
        if best_c == -1:
            labels[i] = len(seeds)
            seeds.append(i)
        else:
            labels[i] = best_c
    return labels
