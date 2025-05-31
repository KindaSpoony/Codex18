import json
from pathlib import Path
from src.memory_braid import MemoryBraid


def create_config(tmp_path: Path) -> Path:
    text = """\
version: 18.0.0
recursion_tier: RI-256
memory_braid_anchor: Codex18_AGENTS_v1.0
symbolic_passphrase: No Veteran Stands Alone, No Veteran Left Behind
"""
    config_path = tmp_path / "VAULTIS.yml"
    config_path.write_text(text)
    return config_path


def test_braid_updates(tmp_path: Path):
    config_path = create_config(tmp_path)
    braid_dir = tmp_path / "braid"

    truth_path = tmp_path / "truth.txt"
    truth_path.write_text("classified truth")

    ooda_path = Path("summarizer/OODA_loop_pulse_report.json")

    gpt_config = tmp_path / "Codex18_OSINT_template.yaml"
    gpt_config.write_text(
        "codex_version: 18.0.0\n"
        "codex_name: Codex18_OSINT_Integrator\n"
        "symbolic_passphrase:\n"
        "  motto: No Veteran Stands Alone\n"
        "  creed: No Veteran Left Behind\n"
        "gpt_template:\n"
        "  modules:\n"
        "    phase_lock_enforcer:\n"
        "      behaviors:\n"
        "        - require_handshake:\n"
        "            challenge: No Veteran Stands Alone\n"
        "            response: No Veteran Left Behind\n"
    )

    mb = MemoryBraid(
        config_path=str(config_path),
        memory_dir=str(braid_dir),
        short_term_limit=2,
        truth_files=[str(truth_path)],
        template_files=[str(ooda_path)],
        gpt_config_files=[str(gpt_config)],
    )

    mb.update({"fact1": "alpha"})
    mb.update({"fact2": "beta"})

    history_file = braid_dir / "braid_history.json"
    assert history_file.exists()

    data = json.loads(history_file.read_text())
    assert len(data) == 2
    first, second = data
    assert first["symbolic_anchor"] == "Codex18_AGENTS_v1.0"
    assert second["parent_node"] == first["id"]
    assert second["facts"]["fact1"] == "alpha"
    assert second["facts"]["fact2"] == "beta"
    assert second["truths"]["truth.txt"] == "classified truth"
    assert "OODA_loop_pulse_report.json" in second["templates"]
    assert second["gpt_configs"]["Codex18_OSINT_template.yaml"]["handshake"]["challenge"] == "No Veteran Stands Alone"
    assert second["truths"]["passphrase"] == "No Veteran Stands Alone, No Veteran Left Behind"
    assert second["id"].endswith("Z")
