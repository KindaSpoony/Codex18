"""Drift Analysis Engine for Codex18.

This component monitors truth vectors to detect narrative drift. It compares
incoming vectors against a persisted baseline **anchor** vector and raises an
alarm if any dimension differs by more than the configured threshold (default
``0.20`` per axis). Every analysis result is saved to
``latest_drift_report.json`` and logged in ``data/analysis_output/drift_logs``
with timestamped filenames.

All timestamps are stored in UTC using the ``YYYY-MM-DDTHH:MM:SSZ`` format.
"""
import json
import os
from datetime import datetime
from typing import List, Optional, Set
from core.truth_vector import TruthVector, SimpleTruthVector


class DriftAnalysisEngine:
    def __init__(self):
        """Initialize the drift analysis engine with persistent anchor handling."""
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
    # Anchor and report persistence helpers
    # ------------------------------------------------------------------
    def _load_anchor(self) -> Optional[List[float]]:
        try:
            with open(self.anchor_path, "r") as f:
                data = json.load(f)
                return data.get("baseline_vector")
        except FileNotFoundError:
            # Fallback to a consolidated drift_results file if present
            try:
                with open(os.path.join("data", "drift_results.json"), "r") as f:
                    data = json.load(f)
                    return data.get("baseline_vector")
            except FileNotFoundError:
                return None

    def _save_anchor(self) -> None:
        timestamp = datetime.utcnow().replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {
            "baseline_vector": self.anchor_vector,
            "timestamp": timestamp,
        }
        with open(self.anchor_path, "w") as f:
            json.dump(data, f)

    def _load_last_report(self) -> Optional[List[float]]:
        try:
            with open(self.latest_report_path, "r") as f:
                text = f.read().strip()
                if not text:
                    return None
                data = json.loads(text)
                return data.get("vector")
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None

    def _save_last_report(self, vector: List[float]) -> None:
        timestamp = datetime.utcnow().replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {"vector": vector, "timestamp": timestamp}
        with open(self.latest_report_path, "w") as f:
            json.dump(data, f)

    def _log_report(
        self,
        vector: List[float],
        diff_anchor: List[float],
        diff_last: Optional[List[float]],
        alarm_flag: bool,
    ) -> None:
        ts = datetime.utcnow().replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
        path = os.path.join(self.logs_dir, f"drift_log_{ts}.json")
        timestamp = ts
        data = {
            "vector": vector,
            "diff_anchor": diff_anchor,
            "diff_last": diff_last,
            "alarm": alarm_flag,
            "timestamp": timestamp,
        }
        with open(path, "w") as f:
            json.dump(data, f)

    def analyze_input(self, quality_score: float, tags: Set[str]):
        """Analyze a new input and update drift state.

        Parameters
        ----------
        quality_score : float
            Normalized overall content quality between 0.0 and 1.0.
        tags : Set[str]
            Set of issue tags describing problems in the content.

        Returns
        -------
        tuple
            ``(truth_vector, alarm_flag)`` where ``truth_vector`` is the
            computed 4-dimensional vector and ``alarm_flag`` indicates if
            drift thresholds were exceeded.
        """
        # Compute the 4D truth vector for the input with robust fallback
        try:
            vector = self.truth_vector.process_input(quality_score, tags)
        except Exception:
            # Any processing error triggers the simpler fallback vector
            vector = self.fallback_vector.process_input(quality_score, tags)

        if self.anchor_vector is None:
            # Establish baseline and persist it
            self.anchor_vector = vector
            self._save_anchor()
            differences_anchor = [0.0] * 4
            alarm_flag = False
            self.drift_alarm_active = False
        else:
            # Calculate absolute differences between current vector and baseline
            differences_anchor = [abs(vector[i] - self.anchor_vector[i]) for i in range(4)]
            alarm_flags = [diff > self.threshold_vector[i] for i, diff in enumerate(differences_anchor)]
            alarm_flag = any(alarm_flags)
            self.drift_alarm_active = alarm_flag

        if self.last_report_vector is None:
            differences_last = None
        else:
            differences_last = [abs(vector[i] - self.last_report_vector[i]) for i in range(4)]

        # Persist report information
        self._log_report(vector, differences_anchor, differences_last, alarm_flag)
        self._save_last_report(vector)
        self.last_report_vector = vector

        return vector, alarm_flag

    def rotate_anchor(self, new_anchor: Optional[List[float]] = None):
        """Manually set a new anchor vector.

        Parameters
        ----------
        new_anchor : Optional[List[float]]
            Custom 4-dimensional vector to use as the new baseline. If
            ``None``, the last report vector becomes the baseline.

        The selected anchor is persisted to ``drift_anchor.json``.
        """
        if new_anchor is not None:
            if len(new_anchor) != 4:
                raise ValueError("Anchor vector must have 4 dimensions.")
            self.anchor_vector = new_anchor
        elif self.last_report_vector is not None:
            self.anchor_vector = self.last_report_vector
        else:
            raise ValueError("No vector available to rotate anchor.")
        self._save_anchor()

