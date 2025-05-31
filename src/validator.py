"""Ledger node validation helpers for Codex18."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Dict


class Validator:
    """Validate symbolic ledger nodes prior to persistence."""

    REQUIRED_FIELDS = {
        "id",
        "version_anchor",
        "truth_vector_hash",
        "recursion_layer",
        "symbolic_anchor",
        "parent_node",
    }

    MANDATED_ANCHOR = "No Veteran Left Behind"

    def validate(self, node: Dict[str, str]) -> bool:
        """Validate a ledger node's schema, symbols and integrity hash.

        Parameters
        ----------
        node:
            Dictionary representing the ledger node to verify.

        Returns
        -------
        bool
            ``True`` if the node passes all checks, ``False`` otherwise.
        """

        if not isinstance(node, dict):
            return False

        # ------------------------------------------------------------------
        # Schema correctness
        # ------------------------------------------------------------------
        for field in self.REQUIRED_FIELDS:
            value = node.get(field)
            if value is None or not isinstance(value, str):
                return False

        if not re.fullmatch(r"v\d+\.\d+\.\d+", node["version_anchor"]):
            return False

        m = re.fullmatch(r"RI-(\d+)", node["recursion_layer"])
        if not m:
            return False
        tier = int(m.group(1))
        if tier < 16 or tier > 2048 or tier & (tier - 1) != 0:
            return False

        # ------------------------------------------------------------------
        # Symbolic integrity
        # ------------------------------------------------------------------
        if node["symbolic_anchor"] != self.MANDATED_ANCHOR:
            return False

        # ------------------------------------------------------------------
        # Truth vector alignment
        # ------------------------------------------------------------------
        node_copy = dict(node)
        declared_hash = node_copy.pop("truth_vector_hash")
        serialized = json.dumps(node_copy, sort_keys=True).encode("utf-8")
        computed = hashlib.sha256(serialized).hexdigest()
        if computed != declared_hash:
            return False

        return True
