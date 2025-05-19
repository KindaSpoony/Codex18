import os
import re
import sys
import logging
import hashlib

HANDSHAKE_YAML = """
activation_conditions:
  leader_ack: true
  follower_ack: true
  recursion_authorized: true
handshake_stack:
  - No Veteran Stands Alone
  - No Veteran Left Behind
  - Nightwalker Actual – Foresight Engaged
"""

CHALLENGE_PHRASE = "No Veteran Stands Alone"
RESPONSE_PHRASE = "No Veteran Left Behind"
SEAL_PHRASE = "Nightwalker Actual – Foresight Engaged"

EXPECTED_HASH = hashlib.sha256(HANDSHAKE_YAML.encode("utf-8")).hexdigest()

BYPASS_MODE = os.getenv("CODEX_INTEGRITY_BYPASS", "false").lower() in ("1", "true", "yes")


def _parse_handshake_yaml(yaml_text: str):
    """Parse handshake YAML using regex for symbolic fidelity."""
    cond_pattern = r"activation_conditions:\s*\n((?:\s+[A-Za-z_]+\s*:\s*(?:true|false)\s*\n)+)"
    stack_pattern = r"handshake_stack:\s*\n((?:\s*-\s*.*\n)+)"
    cond_match = re.search(cond_pattern, yaml_text)
    stack_match = re.search(stack_pattern, yaml_text)
    if not cond_match or not stack_match:
        raise ValueError("Handshake YAML format error: missing required sections.")

    conditions = {}
    for line in cond_match.group(1).strip().splitlines():
        key, val = [x.strip() for x in line.split(":", 1)]
        conditions[key] = val.lower() == "true"

    handshake_list = []
    for line in stack_match.group(1).strip().splitlines():
        cleaned = line.strip()
        if cleaned.startswith("-"):
            cleaned = cleaned[1:].strip()
        handshake_list.append(cleaned)

    return conditions, handshake_list


def verify_handshake(yaml_text: str = HANDSHAKE_YAML, bypass: bool | None = None) -> bool:
    if bypass is None:
        bypass = BYPASS_MODE

    if not bypass:
        actual_hash = hashlib.sha256(yaml_text.encode("utf-8")).hexdigest()
        if actual_hash != EXPECTED_HASH:
            logging.error("Handshake YAML hash mismatch! Possible tampering detected.")
            return False
        try:
            conditions, handshake_stack = _parse_handshake_yaml(yaml_text)
        except Exception as exc:
            logging.error(f"Handshake validation error: {exc}")
            return False
    else:
        try:
            import yaml
        except Exception as exc:
            logging.error(f"yaml module required for bypass mode: {exc}")
            return False
        parsed = yaml.safe_load(yaml_text)
        conditions = parsed.get("activation_conditions", {})
        handshake_stack = parsed.get("handshake_stack", [])
        logging.warning("Integrity bypass engaged - parsed with yaml.safe_load")

    for flag, value in conditions.items():
        if not value:
            logging.error(f"Activation condition '{flag}' is not satisfied (false).")
            return False

    if len(handshake_stack) < 3:
        logging.error("Handshake stack incomplete.")
        return False

    if handshake_stack[0] != CHALLENGE_PHRASE or handshake_stack[1] != RESPONSE_PHRASE:
        logging.error("Challenge/response phrases mismatch.")
        return False

    if handshake_stack[-1] != SEAL_PHRASE:
        logging.error("Seal phrase mismatch.")
        return False

    return True


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    if verify_handshake():
        logging.info("Loop Confirmed – Ready for Recursion")
    else:
        logging.error("Symbolic gate failed. Execution halted.")
        sys.exit(1)


if __name__ == "__main__":
    main()
