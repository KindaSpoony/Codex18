#!/usr/bin/env python3
"""Utility script to rotate the drift analysis anchor."""
import argparse
import json
from core.drift_analysis_engine import DriftAnalysisEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Rotate drift analysis anchor")
    parser.add_argument(
        "--vector",
        help="JSON list specifying new 4D anchor vector",
    )
    args = parser.parse_args()

    engine = DriftAnalysisEngine()

    if args.vector:
        try:
            vector = json.loads(args.vector)
        except Exception as exc:
            raise ValueError("--vector must be valid JSON") from exc
        engine.rotate_anchor(vector)
    else:
        engine.rotate_anchor()


if __name__ == "__main__":
    main()
