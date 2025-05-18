"""Truth Vector processing module for Codex18.
Provides utilities to compute a multi-dimensional representation of content integrity.
"""
from typing import List, Set


class TruthVector:
    """Compute a 4-dimensional truth vector from quality scores and tags."""

    def __init__(self) -> None:
        pass

    def process_input(self, quality_score: float, tags: Set[str]) -> List[float]:
        """Return a `[v0, v1, v2, v3]` truth vector.

        Parameters
        ----------
        quality_score : float
            Float between 0.0 and 1.0 describing overall content quality.
        tags : Set[str]
            Set of issue tags such as ``{"misinformation", "contradiction"}``.

        Returns
        -------
        list of float
            Four-dimensional truth vector where ``v0`` is the normalized quality
            score and the remaining components reflect factual integrity,
            contextual consistency, and other integrity factors.
        """
        q = max(0.0, min(1.0, quality_score))
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

    def __init__(self) -> None:
        pass

    def process_input(self, quality_score: float, tags: Set[str]) -> List[float]:
        """Return a basic 4-dimensional truth vector.

        Parameters
        ----------
        quality_score : float
            Float between 0.0 and 1.0 describing overall content quality.
        tags : Set[str]
            Issue tags observed in the content.

        Returns
        -------
        list of float
            The normalized quality score followed by three identical integrity
            values. If any tags are present, those values are ``0.5``; otherwise
            they are ``1.0``.
        """
        q = max(0.0, min(1.0, quality_score))
        if tags:
            v1 = v2 = v3 = 0.5
        else:
            v1 = v2 = v3 = 1.0
        return [q, v1, v2, v3]
