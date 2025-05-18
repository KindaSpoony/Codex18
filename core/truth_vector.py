from typing import Set, List

class TruthVector:
    """Simple truth vector processor."""

    def process_input(self, quality_score: float, tags: Set[str]) -> List[float]:
        """Return a four dimensional truth vector.

        The first dimension is the normalized quality score. The remaining
        dimensions reflect narrative checks, cognitive bias, and deception
        alerts as indicated by tags.
        """
        # normalize quality score to 0-1
        q = quality_score / 100.0 if quality_score > 1 else quality_score
        q = max(0.0, min(1.0, q))
        narrative = 1.0 if "narrative_check" in tags else 0.0
        bias = 1.0 if "cognitive_bias" in tags else 0.0
        deception = 1.0 if "deception_alert" in tags else 0.0
        return [q, narrative, bias, deception]
