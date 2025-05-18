"""
Drift Analysis Engine for Codex18.
Tracks truth vectors and flags narrative drift when inputs deviate significantly from an established baseline.
"""
import json
import os
from datetime import datetime
from typing import List, Optional, Set

from core.truth_vector import TruthVector, SimpleTruthVector


class DriftAnalysisEngine:
    """Monitor truth vectors for significant drift."""

    def __init__(self) -> None:
        """Initialize the drift analysis engine with persistent anchor handling.

        Notes
        -----
        - The first processed input establishes the baseline (anchor) vector.
        - Subsequent inputs are compared against this baseline to detect drift.
        - ``SimpleTruthVector`` is used as a fallback processor if the primary
          ``TruthVector`` encounters errors.
        """
        self.truth_vector = TruthVector()
        self.fallback_vector = SimpleTruthVector()

        self.anchor_path = os.path.join("data", "drift_anchor.json")
        self.latest_report_path = os.path.join("data", "analysis_output", "latest_drift_report.json")
        self.logs_dir = os.path.join("data", "analysis_output", "drift_logs")

        os.makedirs(self.logs_dir, exist_ok=True)

        self.anchor_vector: Optional[List[float]] = self._load_anchor()
        self.last_report_vector: Optional[List[float]] = self._load_last_report()

        self.threshold_vector = [0.20, 0.20, 0.20, 0.20]
        self.drift_alarm_active = False

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------
    def _load_anchor(self) -> Optional[List[float]]:
        """Load the persisted baseline anchor vector from disk."""
        try:
            with open(self.anchor_path, "r") as f:
                data = json.load(f)
                return data.get("baseline_vector")
        except FileNotFoundError:
            return None

    def _save_anchor(self) -> None:
        """Persist the current anchor vector to disk."""
        data = {
            "baseline_vector": self.anchor_vector,
            "timestamp": datetime.utcnow().isoformat(),
        }
        with open(self.anchor_path, "w") as f:
            json.dump(data, f)

    def _load_last_report(self) -> Optional[List[float]]:
        """Load the last processed truth vector from disk."""
        try:
            with open(self.latest_report_path, "r") as f:
                data = json.load(f)
                return data.get("vector")
        except FileNotFoundError:
            return None

    def _save_last_report(self, vector: List[float]) -> None:
        """Persist the provided truth vector as the latest processed report."""
        data = {"vector": vector, "timestamp": datetime.utcnow().isoformat()}
        with open(self.latest_report_path, "w") as f:
            json.dump(data, f)

    def _log_report(
        self,
        vector: List[float],
        diff_anchor: List[float],
        diff_last: Optional[List[float]],
        alarm_flag: bool,
    ) -> None:
        """Write a detailed drift report log to disk."""
        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        path = os.path.join(self.logs_dir, f"drift_log_{ts}.json")
        data = {
            "vector": vector,
            "diff_anchor": diff_anchor,
            "diff_last": diff_last,
            "alarm": alarm_flag,
            "timestamp": datetime.utcnow().isoformat(),
        }
        with open(path, "w") as f:
            json.dump(data, f)

    # ------------------------------------------------------------------
    # Core methods
    # ------------------------------------------------------------------
    def analyze_input(self, quality_score: float, tags: Set[str]):
        """Analyze a new input and update drift state.

        Parameters
        ----------
        quality_score : float
            Normalized quality score between 0.0 (poor quality) and 1.0 (high quality).
        tags : Set[str]
            Set of issue tags describing identified problems (e.g., {"misinformation", "inconsistency"}).

        Returns
        -------
        tuple
            A tuple ``(truth_vector, alarm_flag)`` where ``truth_vector`` is a computed
            4-dimensional list of floats and ``alarm_flag`` indicates if any drift
            thresholds were exceeded.
        """
        try:
            vector = self.truth_vector.process_input(quality_score, tags)
        except Exception:
            # Fallback to SimpleTruthVector on error
            vector = self.fallback_vector.process_input(quality_score, tags)

        if self.anchor_vector is None:
            # Establish baseline anchor vector on first input
            self.anchor_vector = vector
            self._save_anchor()
            differences_anchor = [0.0] * 4
            alarm_flag = False
            self.drift_alarm_active = False
        else:
            differences_anchor = [abs(vector[i] - self.anchor_vector[i]) for i in range(4)]
            alarm_flags = [diff > self.threshold_vector[i] for i, diff in enumerate(differences_anchor)]
            alarm_flag = any(alarm_flags)
            self.drift_alarm_active = alarm_flag

        differences_last = (
            [abs(vector[i] - self.last_report_vector[i]) for i in range(4)]
            if self.last_report_vector else None
        )

        # Persist analysis results
        self._log_report(vector, differences_anchor, differences_last, alarm_flag)
        self._save_last_report(vector)
        self.last_report_vector = vector

        return vector, alarm_flag

    def rotate_anchor(self, new_anchor: Optional[List[float]] = None) -> None:
        """Manually update the baseline (anchor) truth vector.

        Parameters
        ----------
        new_anchor : Optional[List[float]], optional
            Explicit four-dimensional vector to set as the new baseline.
            If ``None``, uses the most recent processed vector.

        Raises
        ------
        ValueError
            If no suitable vector is available or provided vector is invalid.
        """
        if new_anchor is not None:
            if len(new_anchor) != 4:
                raise ValueError("Anchor vector must have exactly 4 dimensions.")
            self.anchor_vector = new_anchor
        elif self.last_report_vector:
            self.anchor_vector = self.last_report_vector
        else:
            raise ValueError("No valid vector available to set as new anchor.")

        self._save_anchor()
