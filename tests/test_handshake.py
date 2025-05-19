import subprocess
from pathlib import Path

from src.handshake.codex16_validator import (
    verify_handshake,
    HANDSHAKE_YAML,
    CHALLENGE_PHRASE,
    RESPONSE_PHRASE,
    SEAL_PHRASE,
)


def test_valid_handshake():
    assert verify_handshake(HANDSHAKE_YAML)


def test_hash_mismatch():
    tampered = HANDSHAKE_YAML.replace("No Veteran Stands Alone", "No Veteran Sits Alone")
    assert not verify_handshake(tampered)


def test_condition_false():
    tampered = HANDSHAKE_YAML.replace("leader_ack: true", "leader_ack: false")
    assert not verify_handshake(tampered)


def test_seal_phrase_mismatch():
    tampered = HANDSHAKE_YAML.replace(SEAL_PHRASE, "Wrong Phrase")
    assert not verify_handshake(tampered)


def test_challenge_response_mismatch():
    tampered = HANDSHAKE_YAML.replace(CHALLENGE_PHRASE, "Wrong Challenge")
    assert not verify_handshake(tampered)


def test_cli_exit_code():
    script = Path(__file__).resolve().parents[1] / "src" / "handshake" / "codex16_validator.py"
    result = subprocess.run(["python", str(script)], capture_output=True, text=True)
    assert result.returncode == 0
