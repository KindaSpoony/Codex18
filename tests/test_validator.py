import json
import hashlib
from src.validator import Validator


def make_node(id="2025-05-25T1845Z-Node1", version="v18.0.1", layer="RI-256", anchor="No Veteran Left Behind", parent="2025-05-25T1815Z-Node0"):
    base = {
        "id": id,
        "version_anchor": version,
        "recursion_layer": layer,
        "symbolic_anchor": anchor,
        "parent_node": parent,
    }
    serialized = json.dumps(base, sort_keys=True).encode("utf-8")
    base["truth_vector_hash"] = hashlib.sha256(serialized).hexdigest()
    return base


def test_valid_node():
    node = make_node()
    assert Validator().validate(node) is True


def test_missing_field():
    node = make_node()
    node.pop("symbolic_anchor")
    assert Validator().validate(node) is False


def test_anchor_mismatch():
    node = make_node(anchor="Wrong Anchor")
    assert Validator().validate(node) is False


def test_hash_mismatch():
    node = make_node()
    node["truth_vector_hash"] = "bad" * 10
    assert Validator().validate(node) is False
