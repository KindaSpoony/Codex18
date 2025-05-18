import math
from core.truth_vector import TruthVector
from core.drift_analysis_engine import DriftAnalysisEngine


def test_truth_vector_basic():
    tv = TruthVector()
    vec = tv.process_input(0.8, set())
    assert vec == [0.8, 1.0, 1.0, 1.0]


def test_truth_vector_tags():
    tv = TruthVector()
    tags = {"misinformation", "contradiction", "speculative"}
    vec = tv.process_input(0.5, tags)
    expected = [0.5, 2/3, 2/3, 2/3]
    assert all(math.isclose(a, b, rel_tol=1e-6) for a, b in zip(vec, expected))


def test_drift_analysis_engine():
    engine = DriftAnalysisEngine()
    vec1, alarm1 = engine.analyze_input(1.0, set())
    assert alarm1 is False
    vec2, alarm2 = engine.analyze_input(1.0, set())
    assert alarm2 is False
    vec3, alarm3 = engine.analyze_input(0.0, {"misinformation", "inconsistency"})
    assert alarm3 is True

    # Test rotate_anchor
    engine.rotate_anchor([1.0, 1.0, 1.0, 1.0])
    assert engine.anchor_vector == [1.0, 1.0, 1.0, 1.0]
