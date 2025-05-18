"""
Truth Vector Framework Module.
Provides the TruthVector class to compute a multi-dimensional representation of truthfulness.
"""
from typing import List, Set


class TruthVector:
    """Computes a 4-dimensional truth vector for given input analysis data."""

    def __init__(self):
        # Optional anchor for baseline truth vector (not used unless future extension requires it)
        # self.current_anchor = None
        pass

    def process_input(self, quality_score: float, tags: Set[str]) -> List[float]:
        """Convert a quality score and associated tags into a 4-dimensional truth vector.

        Parameters
        ----------
        quality_score : float
            Float between 0.0 and 1.0 indicating overall content quality/truthfulness.
        tags : Set[str]
            Set of strings indicating content issue tags.

        Returns
        -------
        List[float]
            [v0, v1, v2, v3] truth vector where:
            v0 = overall truthfulness/quality (normalized quality_score).
            v1 = factual integrity axis (1.0 if no factual errors; lower if factual issues present).
            v2 = contextual consistency axis (1.0 if context is consistent; lower if context issues present).
            v3 = other integrity factors axis (1.0 if no other issues like speculation/irrelevance; lower otherwise).
        """
        # Normalize quality_score to [0,1]
        q = max(0.0, min(1.0, quality_score))
        # Define tag categories for each axis (case-insensitive matching)
        factual_issues = {"misinformation", "fabrication", "false", "inaccurate", "error", "incorrect"}
        context_issues = {"contradiction", "inconsistency", "context", "omission", "discrepancy", "incoherent"}
        other_issues = {"speculative", "unverified", "ambiguous", "irrelevant", "off-topic", "style"}
        total = len(tags)
        if total == 0:
            # If no issue tags, all specific integrity dimensions are ideal (1.0)
            v1 = 1.0
            v2 = 1.0
            v3 = 1.0
        else:
            # Count tags in each category
            cf = sum(1 for t in tags if t.lower() in factual_issues)
            cc = sum(1 for t in tags if t.lower() in context_issues)
            categorized = cf + cc
            co = total - categorized  # remaining tags count as "other"
            if co < 0:
                co = 0
            # Compute each dimension as 1 minus the fraction of tags in that category (higher = better integrity)
            v1 = 1.0 - (cf / total)
            v2 = 1.0 - (cc / total)
            v3 = 1.0 - (co / total)
            # Clamp values to [0,1] to handle edge cases
            v1 = max(0.0, min(1.0, v1))
            v2 = max(0.0, min(1.0, v2))
            v3 = max(0.0, min(1.0, v3))
        v0 = q
        return [v0, v1, v2, v3]
