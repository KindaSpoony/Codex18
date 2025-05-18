"""
Truth Vector processing module for Codex18.
Provides utilities to compute a multi-dimensional representation of content integrity.
"""
from typing import List, Set


class TruthVector:
    """Compute a proportional 4-dimensional truth vector.

    Each integrity dimension is proportionally reduced by the presence of issue tags.
    """

    def __init__(self) -> None:
        """Construct a TruthVector processor."""
        pass

    def process_input(self, quality_score: float, tags: Set[str]) -> List[float]:
        """Compute proportional truth vector from input.

        Parameters
        ----------
        quality_score : float
            Normalized quality score between 0.0 and 1.0.
        tags : Set[str]
            Set of issue tags describing identified problems.

        Returns
        -------
        List[float]
            Four-dimensional vector ``[v0, v1, v2, v3]`` representing overall quality,
            factual integrity, contextual integrity, and other factors.
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
            co = total - (cf + cc)
            v1 = 1.0 - cf / total
            v2 = 1.0 - cc / total
            v3 = 1.0 - co / total
        return [q, v1, v2, v3]


class SimpleTruthVector:
    """Fallback truth vector processor.

    Assigns fixed scores if any issues are detected.
    """

    def __init__(self) -> None:
        """Construct a SimpleTruthVector processor."""
        pass

    def process_input(self, quality_score: float, tags: Set[str]) -> List[float]:
        """Compute simplified fallback truth vector.

        Parameters
        ----------
        quality_score : float
            Normalized quality score between 0.0 and 1.0.
        tags : Set[str]
            Set of issue tags describing identified problems.

        Returns
        -------
        List[float]
            Simplified 4-dimensional vector with uniform reduction when tags exist.
        """
        q = max(0.0, min(1.0, quality_score))
        v1 = v2 = v3 = 0.5 if tags else 1.0
        return [q, v1, v2, v3]
