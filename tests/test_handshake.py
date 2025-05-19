import unittest
import subprocess
from pathlib import Path

from src.handshake.codex16_validator import (
    verify_handshake,
    HANDSHAKE_YAML,
    CHALLENGE_PHRASE,
    RESPONSE_PHRASE,
    SEAL_PHRASE,
)


class HandshakeTests(unittest.TestCase):
    def test_valid_handshake(self):
        self.assertTrue(verify_handshake(HANDSHAKE_YAML))

    def test_hash_mismatch(self):
        tampered = HANDSHAKE_YAML.replace("No Veteran Stands Alone", "No Veteran Sits Alone")
        self.assertFalse(verify_handshake(tampered))

    def test_condition_false(self):
        tampered = HANDSHAKE_YAML.replace("leader_ack: true", "leader_ack: false")
        self.assertFalse(verify_handshake(tampered))

    def test_seal_phrase_mismatch(self):
        tampered = HANDSHAKE_YAML.replace(SEAL_PHRASE, "Wrong Phrase")
        self.assertFalse(verify_handshake(tampered))

    def test_challenge_response_mismatch(self):
        tampered = HANDSHAKE_YAML.replace(CHALLENGE_PHRASE, "Wrong Challenge")
        self.assertFalse(verify_handshake(tampered))

    def test_cli_exit_code(self):
        script = Path(__file__).resolve().parents[1] / "src" / "handshake" / "codex16_validator.py"
        result = subprocess.run(["python3", str(script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
