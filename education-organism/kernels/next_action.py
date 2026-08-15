"""lib/next_action.py — the deterministic next-action scheduler (GEM 12.3).

GEM 12.3 (migration/v2/GEMS.md): "`patala_next_action()` should CALCULATE, not LLM-guess.
P(v) = w1·D + w2·B + w3·U + w4·Q + w5·R − w6·C
(downstream load, betweenness, uncertainty, question demand, review deficit, cost)."

This is the deterministic prioritizer that decides WHAT the OS works on next — which claim to verify,
which passage to translate, which crux to resolve — by weighted formula, not by asking an LLM to "pick
something useful." It turns the OS from a passive store into an active research scheduler. Grounded in
our kernels: downstream load (staleness blast-radius), betweenness (graph position), uncertainty
(review deficit), question demand (organism), cost (run budget).
"""
from __future__ import annotations


class Task:
    """A schedulable piece of work (verify a claim, translate a passage, resolve a crux)."""
    def __init__(self, task_id, kind, downstream=0, betweenness=0.0, uncertainty=0.0,
                 question_demand=0, review_deficit=0, cost=1.0):
        self.id = task_id
        self.kind = kind
        self.downstream = downstream          # D: claims that collapse if wrong (staleness blast-radius)
        self.betweenness = betweenness        # B: how central in the graph (0..1)
        self.uncertainty = uncertainty        # U: how contested / how weakly verified (0..1)
        self.question_demand = question_demand  # Q: learner/researcher question pressure
        self.review_deficit = review_deficit  # R: how overdue for review (staleness)
        self.cost = cost                      # C: token/run budget (1.0 = cheap)

    def priority(self, w=(2, 1, 3, 2, 2, 1)):
        """P(v) = w1·D + w2·B + w3·U + w4·Q + w5·R − w6·C (GEM 12.3 formula)."""
        w1, w2, w3, w4, w5, w6 = w
        return (w1 * self.downstream + w2 * self.betweenness + w3 * self.uncertainty
                + w4 * self.question_demand + w5 * self.review_deficit - w6 * self.cost)


class NextActionScheduler:
    """Ranks all work by the deterministic formula (no LLM-guessing the next step)."""

    def __init__(self, tasks=None, weights=(2, 1, 3, 2, 2, 1)):
        self.tasks = tasks or []
        self.weights = weights

    def add(self, task):
        self.tasks.append(task)
        return task

    def rank(self):
        """Deterministic ordering of work by priority (the next action is CALCULATED)."""
        scored = [(t.priority(self.weights), t) for t in self.tasks]
        scored.sort(key=lambda x: -x[0])
        return scored

    def next_action(self):
        """The single highest-priority task (what the OS works on now)."""
        ranked = self.rank()
        return ranked[0] if ranked else None
