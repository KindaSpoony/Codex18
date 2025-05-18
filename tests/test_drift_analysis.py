from core.drift_analysis_engine import DriftAnalysisEngine


def test_alarm_activation():
    engine = DriftAnalysisEngine()
    vec1, alarm1 = engine.analyze_input(1.0, set())
    assert alarm1 is False
    vec2, alarm2 = engine.analyze_input(0.5, set())
    assert alarm2 is True


def test_rotate_anchor():
    engine = DriftAnalysisEngine()
    engine.analyze_input(0.9, set())
    new_anchor = [0.1, 0.1, 0.1, 0.1]
    engine.rotate_anchor(new_anchor)
    assert engine.anchor_vector == new_anchor

    # rotating with None should use last report vector
    engine.analyze_input(0.8, {"misinformation"})
    last_vector = engine.last_report_vector
    engine.rotate_anchor()
    assert engine.anchor_vector == last_vector
