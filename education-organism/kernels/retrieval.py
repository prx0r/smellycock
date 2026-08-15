#!/usr/bin/env python3
"""kernels/retrieval.py — the dependency-light retrieval lift (GFM-RAG + RoG adoption, FRONTIER-REVIEW §8.3).

Adopts two frontier retrieval ideas WITHOUT copying their heavy deps:

1. GFM-RAG sparse entity->doc projection rankers
   (`gfmrag/models/gfm_rag_v1/rankers.py`): rank which source document best supports a set of entities
   by projecting entity evidence onto documents through a sparse entity->doc matrix. We mirror
   `SimpleRanker` (pure sparse mat-vec projection) and `IDFWeightedRanker` (per-entity 1/freq weighting),
   but in plain stdlib dicts/lists — no torch, no scipy. A document's score is the sum of the evidence of
   the entities it mentions, optionally attenuated by how common an entity is (IDF = rare entities carry
   more signal).

2. RoG rule-constrained path enumeration + random-walk negative sampling
   (`reasoning-on-graphs/src/utils/graph_utils.py`): `bfs_with_rule` enumerates paths whose edge-type
   sequence matches a target rule, and `get_negative_paths`/`get_random_paths` sample random walks that
   do NOT reach the answer entity (so a contrastive trainer sees genuinely distinct negatives). We keep
   the same contract over a plain adjacency dict (node -> {neighbor: relation}) — no networkx, no `walker`
   dep. Negative paths are guaranteed distinct from any true positive path.

This kernel is wired so the organism can call `rank_sources_for_entities(entities, source_index)` to
pick which source document most supports a learner/query's entity evidence, and `sample_paths` /
`sample_negative_paths` to mine reasoning paths + contrastive negatives over the knowledge graph.

stdlib only. Deterministic given a seed. No external dependencies.
"""
from __future__ import annotations
import random


# ── GFM-RAG sparse entity->doc projection rankers (stdlib mirror) ────────────
def entity_to_doc_rank(entity_scores: dict, doc_entities: dict, *, idf: bool = False) -> dict:
    """Project entity evidence onto documents (GFM-RAG sparse ranker math).

    entity_scores — {entity: evidence_score} (the "entity prediction" of the query/learner).
    doc_entities — {doc_id: iterable-of-entities} (the sparse entity->doc incidence).
    idf — if True, weight each entity by inverse document frequency (1 / #docs mentioning it),
          matching `IDFWeightedRanker`; else pure `SimpleRanker` projection.

    Returns {doc_id: doc_score}. A doc's score is the sum of (idf-scaled) evidence of the entities it
    mentions. A doc that mentions NO query entity scores 0. Ties are broken by doc id for determinism.
    """
    freq = {}
    for ents in doc_entities.values():
        for e in set(ents):
            freq[e] = freq.get(e, 0) + 1
    scores = {doc: 0.0 for doc in doc_entities}
    for doc, ents in doc_entities.items():
        s = 0.0
        for e in set(ents):
            sc = entity_scores.get(e, 0.0)
            if sc == 0.0:
                continue
            w = 1.0
            if idf:
                w = 1.0 / freq.get(e, 0) if freq.get(e, 0) else 0.0
            s += sc * w
        scores[doc] = round(s, 6)
    # drop docs with zero evidence, tie-break by doc id
    return {d: s for d, s in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0])) if s > 0.0}


def rank_sources_for_entities(entities, source_index, *, idf: bool = True) -> list:
    """Rank source ids by how well they support a set of entities (organism-facing).

    entities — iterable of entities (the query/learner's evidence set).
    source_index — {source_id: iterable-of-entities} the source document entity index.
    idf — IDF-weight (default True: rare entities are stronger evidence).
    Returns an ordered list of source ids (best-supporting first). Empty if none support the entities.
    """
    scores = entity_to_doc_rank({e: 1.0 for e in entities}, source_index, idf=idf)
    return list(scores.keys())


# ── RoG path enumeration + negative sampling (stdlib mirror) ─────────────────
def _neighbors(adjacency, node) -> list:
    """Return [(neighbor, relation)] for a node over an adjacency dict."""
    nb = adjacency.get(node, {})
    if isinstance(nb, dict):
        return list(nb.items())
    if isinstance(nb, (set, list, tuple)):
        # unweighted adjacency {node: [neighbor...]} -> relation None
        return [(n, None) for n in nb]
    return []


def bfs_with_rule(adjacency, start_node, target_rule, max_paths: int = 10) -> list:
    """RoG `bfs_with_rule`: enumerate paths from start whose edge-type sequence == target_rule.

    adjacency — {node: {neighbor: relation}} (or {node: [neighbors]}).
    target_rule — a list of relation types; a path matches when its relation sequence equals it.
    Returns a list of paths, each path = [(start, rel, next), ...].
    """
    results = []
    queue = [(start_node, [])]
    while queue:
        current, path = queue.pop(0)
        if len(path) == len(target_rule):
            results.append(path)
            if len(results) >= max_paths:
                return results
        if len(path) < len(target_rule):
            rel_expected = target_rule[len(path)]
            for neighbor, rel in _neighbors(adjacency, current):
                if rel != rel_expected:
                    continue
                queue.append((neighbor, path + [(current, rel, neighbor)]))
    return results


def sample_paths(adjacency, start_node, target_rule, *, n: int = 3, max_paths: int = 10,
                 seed: int | None = None) -> list:
    """Sample up to `n` distinct rule-matching paths from start (RoG-style evidence paths)."""
    rng = random.Random(seed)
    paths = bfs_with_rule(adjacency, start_node, target_rule, max_paths=max_paths)
    if len(paths) <= n:
        return paths
    return rng.sample(paths, n)


def _random_walk(adjacency, start, hop: int, rng: random.Random) -> list:
    """A single random walk of length `hop` over the adjacency dict (RoG `walker.random_walks`)."""
    walk = []
    node = start
    for _ in range(hop):
        nb = _neighbors(adjacency, node)
        if not nb:
            break
        neighbor, rel = rng.choice(nb)
        walk.append((node, rel, neighbor))
        node = neighbor
    return walk


def sample_negative_paths(adjacency, start_node, answer_node, *, n_neg: int = 3, hop: int = 2,
                          seed: int | None = None) -> list:
    """RoG `get_negative_paths`: random walks that do NOT terminate at the answer entity.

    Returns a list of negative paths, each = [(u, rel, v), ...]. A path is rejected if it reaches
    `answer_node` as its final node, so the negatives are genuinely distinct from a positive path that
    ends at the answer. Deduplicated; returns as many distinct negatives as found (up to n_neg).
    """
    rng = random.Random(seed)
    seen = set()
    negs = []
    guard = 0
    while len(negs) < n_neg and guard < n_neg * 200:
        guard += 1
        path = _random_walk(adjacency, start_node, hop, rng)
        if not path:
            continue
        if path[-1][2] == answer_node:
            continue  # ends at the answer → not negative
        key = tuple(path)
        if key in seen:
            continue
        seen.add(key)
        negs.append(path)
    return negs


def positives_from_start(adjacency, start_node, target_rule, *, seed: int | None = None) -> list:
    """All positive (rule-matching) paths from start, for contrast (used by tests/consumers)."""
    return bfs_with_rule(adjacency, start_node, target_rule)


if __name__ == "__main__":
    idx = {
        "doc1": {"the-flashing", "the-order", "order-less-support"},
        "doc2": {"recognition", "re-cognition", "self"},
    }
    print("rank:", rank_sources_for_entities(["the-flashing", "the-order"], idx))
    adj = {
        "A": {"B": "cites", "C": "contradicts"},
        "B": {"D": "cites"},
        "C": {"D": "contradicts"},
    }
    print("paths:", sample_paths(adj, "A", ["contradicts", "contradicts"], n=5))
    print("negs:", sample_negative_paths(adj, "A", "D", n_neg=5, hop=2, seed=1))
