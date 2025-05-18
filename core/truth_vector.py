"""Truth Vector processing module for Codex18.
Provides utilities to compute a multi-dimensional representation of content integrity.
"""
from typing import List, Set


class TruthVector:
    """Compute a 4-dimensional truth vector from quality scores and tags."""

    def __init__(self) -> None:
        # Placeholder for future baseline handling
        pass

    def process_input(self, quality_score: float, tags: Set[str]) -> List[float]:
        """Convert a quality score and tags into a [v0, v1, v2, v3] truth vector.

        Parameters
        ----------
        quality_score : float
            Overall content quality or truthfulness between 0.0 and 1.0.
        tags : Set[str]
            Issue tags such as ``{"misinformation", "contradiction"}``.

        Returns
        -------
        List[float]
            The truth vector ``[v0, v1, v2, v3]`` where higher values indicate
            better factual integrity and contextual consistency.
        """
        # Normalize quality score to [0, 1]
        q = max(0.0, min(1.0, quality_score))
        # Tag categories for integrity axes
        factual_issues = {"misinformation", "fabrication", "false", "inaccurate", "error", "incorrect"}
        context_issues = {"contradiction", "inconsistency", "context", "omission", "discrepancy", "incoherent"}
        other_issues = {"speculative", "unverified", "ambiguous", "irrelevant", "off-topic", "style"}

        total = len(tags)
        if total == 0:
            v1 = v2 = v3 = 1.0
        else:
            cf = sum(1 for t in tags if t.lower() in factual_issues)
            cc = sum(1 for t in tags if t.lower() in context_issues)
            categorized = cf + cc
            co = total - categorized
            if co < 0:
                co = 0
            v1 = 1.0 - (cf / total)
            v2 = 1.0 - (cc / total)
            v3 = 1.0 - (co / total)
            v1 = max(0.0, min(1.0, v1))
            v2 = max(0.0, min(1.0, v2))
            v3 = max(0.0, min(1.0, v3))
        return [q, v1, v2, v3]


class SimpleTruthVector:
    """Simplified fallback truth vector processor."""

    def process_input(self, quality_score: float, tags: Set[str]) -> List[float]:
        """Return a basic 4-dimensional truth vector.

        This fallback version reduces all integrity dimensions equally when any
        issue tags are present.
        """
        q = max(0.0, min(1.0, quality_score))
        if tags:
            v1 = v2 = v3 = 0.5
        else:
            v1 = v2 = v3 = 1.0
        return [q, v1, v2, v3]
