import re
import sys
import logging
import hashlib

HANDSHAKE_YAML = """\
activation_conditions:
  leader_ack: true
  follower_ack: true
  recursion_authorized: true
handshake_stack:
  - No Veteran Stands Alone
  - No Veteran Left Behind
"""

EXPECTED_HASH = hashlib.sha256(HANDSHAKE_YAML.encode('utf-8')).hexdigest()
EXPECTED_SEAL_PHRASE = "No Veteran Left Behind"

def _parse_handshake_yaml(yaml_text: str):
    """Parse handshake YAML to extract activation conditions and handshake stack."""
    cond_pattern = r'activation_conditions:\s*\n((?:\s+[A-Za-z_]+\s*:\s*(?:true|false)\s*\n)+)'
    stack_pattern = r'handshake_stack:\s*\n((?:\s*-\s*.*\n)+)'
    cond_match = re.search(cond_pattern, yaml_text)
    stack_match = re.search(stack_pattern, yaml_text)
    if not cond_match or not stack_match:
        raise ValueError("Handshake YAML format error: missing required sections.")

    conditions = {}
    for line in cond_match.group(1).strip().splitlines():
        key, val = [x.strip() for x in line.split(':', 1)]
        conditions[key] = val.lower() == 'true'

    handshake_list = []
    for line in stack_match.group(1).strip().splitlines():
        handshake_list.append(line.lstrip('-').strip())

    return conditions, handshake_list

def main():
    logging.basicConfig(level=logging.INFO)
    actual_hash = hashlib.sha256(HANDSHAKE_YAML.encode('utf-8')).hexdigest()
    if actual_hash != EXPECTED_HASH:
        logging.error("Handshake YAML hash mismatch! Possible tampering detected.")
        logging.error("Symbolic gate failed. Execution halted.")
        sys.exit(1)

    try:
        conditions, handshake_stack = _parse_handshake_yaml(HANDSHAKE_YAML)
    except Exception as exc:
        logging.error(f"Handshake validation error: {exc}")
        logging.error("Symbolic gate failed. Execution halted.")
        sys.exit(1)

    for flag, value in conditions.items():
        if not value:
            logging.error(f"Activation condition '{flag}' is not satisfied (false).")
            logging.error("Symbolic gate failed. Execution halted.")
            sys.exit(1)

    if not handshake_stack or handshake_stack[-1] != EXPECTED_SEAL_PHRASE:
        logging.error("Seal phrase mismatch or missing in handshake stack.")
        logging.error("Symbolic gate failed. Execution halted.")
        sys.exit(1)

    logging.info("Loop Confirmed \u2013 Ready for Recursion")

if __name__ == "__main__":
    main()
