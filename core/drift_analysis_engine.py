"""
Drift Analysis Engine for Codex18.
Monitors the truth vector of content to detect narrative drift or integrity issues.
"""
from typing import Set
from core.truth_vector import TruthVector


class DriftAnalysisEngine:
    def __init__(self):
        """Initialize the drift analysis engine with a TruthVector processor and no initial baseline."""
        self.truth_vector = TruthVector()
        self.anchor_vector = None
        # Threshold for drift alarms (approx. 2 standard deviations for normalized values).
        # This can be tuned per system requirements or calibrated dynamically.
        self.threshold_vector = [0.20, 0.20, 0.20, 0.20]
        self.drift_alarm_active = False

    def analyze_input(self, quality_score: float, tags: Set[str]):
        """Analyze a new input given its quality score and tags.

        Returns
        -------
        tuple
            (truth_vector, alarm_flag)
        """
        # Compute the 4D truth vector for the input
        vector = self.truth_vector.process_input(quality_score, tags)
        if self.anchor_vector is None:
            # Set the first input's vector as the baseline anchor
            self.anchor_vector = vector
            alarm_flag = False
            self.drift_alarm_active = False
        else:
            # Calculate absolute differences between current vector and baseline
            differences = [abs(vector[i] - self.anchor_vector[i]) for i in range(4)]
            # Check each dimension against its 2-std-dev threshold
            alarm_flags = [diff > self.threshold_vector[i] for i, diff in enumerate(differences)]
            alarm_flag = any(alarm_flags)
            self.drift_alarm_active = alarm_flag
        return vector, alarm_flag

    def rotate_anchor(self, new_anchor: list):
        """Update the baseline (anchor) truth vector to a new value."""
        if len(new_anchor) != 4:
            raise ValueError("Anchor vector must have 4 dimensions.")
        self.anchor_vector = new_anchor

