"""
Module: memory_braid – Maintains continuity of facts and themes across interactions.
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional


class MemoryBraid:
    """Maintain short-term and long-term memory nodes.

    The braid integrates new facts across agent interactions while preserving a
    chain of symbolic anchors defined in ``VAULTIS.yml``.  Long-term state is
    stored as a sequence of nodes in ``braid_history.json``.
    """

    def __init__(
        self,
        config_path: str = "VAULTIS.yml",
        memory_dir: str = os.path.join("data", "memory_braid"),
        short_term_limit: int = 5,
        truth_files: Optional[List[str]] | None = None,
        template_files: Optional[List[str]] | None = None,
        gpt_config_files: Optional[List[str]] | None = None,
    ) -> None:
        self.memory_dir = memory_dir
        self.short_term_limit = short_term_limit

        self.truth_files = truth_files or []
        self.template_files = template_files or []
        self.gpt_config_files = gpt_config_files or []

        os.makedirs(self.memory_dir, exist_ok=True)

        self.config = self._load_config(config_path)
        self.version_anchor = str(
            self.config.get("version")
            or self.config.get("codex_version")
            or "v0.0.0"
        )
        self.recursion_layer = self.config.get("recursion_tier", "RI-256")
        self.symbolic_anchor = self.config.get(
            "memory_braid_anchor", "Codex18_AGENTS_v1.0"
        )

        self.short_term: List[Dict] = []
        self.history_path = os.path.join(self.memory_dir, "braid_history.json")
        self.long_term: List[Dict] = self._load_history()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_config(self, path: str) -> Dict:
        try:
            import yaml

            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    def _load_history(self) -> List[Dict]:
        try:
            with open(self.history_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except Exception:
            pass
        return []

    def _load_files(self, paths: List[str]) -> Dict[str, str]:
        """Return mapping of basename -> file contents for ``paths``."""
        data: Dict[str, str] = {}
        for p in paths:
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data[os.path.basename(p)] = f.read()
            except Exception:
                data[os.path.basename(p)] = ""
        return data

    def _extract_handshake(self, cfg: Dict) -> Dict[str, str]:
        try:
            behaviors = cfg["gpt_template"]["modules"]["phase_lock_enforcer"]["behaviors"]
            for idx, b in enumerate(behaviors):
                if isinstance(b, dict) and "require_handshake" in b:
                    data = b["require_handshake"]
                    if isinstance(data, dict):
                        return data
                    # handle split representation
                    handshake: Dict[str, str] = {}
                    for extra in behaviors[idx + 1 : idx + 3]:
                        if isinstance(extra, dict):
                            handshake.update(extra)
                    if handshake:
                        return handshake
        except Exception:
            pass
        return {}

    def _current_time(self) -> str:
        return (
            datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )

    def _save_history(self) -> None:
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(self.long_term, f, indent=2)

    def _latest_node(self) -> Dict:
        return self.long_term[-1] if self.long_term else {}

    def _hash_node(self, node: Dict) -> str:
        copy = dict(node)
        copy.pop("truth_vector_hash", None)
        serialized = json.dumps(copy, sort_keys=True).encode("utf-8")
        return hashlib.sha256(serialized).hexdigest()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update(
        self,
        new_facts: Dict,
        *,
        truth_files: Optional[List[str]] | None = None,
        template_files: Optional[List[str]] | None = None,
        gpt_config_files: Optional[List[str]] | None = None,
    ) -> None:
        """Integrate ``new_facts`` into short-term and long-term memory."""

        if not isinstance(new_facts, dict):
            raise TypeError("new_facts must be a dictionary")

        self.short_term.append(new_facts)
        if len(self.short_term) > self.short_term_limit:
            self.short_term = self.short_term[-self.short_term_limit :]

        context: Dict = {}
        context.update(self._latest_node().get("facts", {}))
        for item in self.short_term:
            context.update(item)

        parent_id = self._latest_node().get("id")
        timestamp = self._current_time()
        node = {
            "id": timestamp,
            "version_anchor": self.version_anchor,
            "recursion_layer": self.recursion_layer,
            "symbolic_anchor": self.symbolic_anchor,
            "parent_node": parent_id,
            "facts": context,
        }

        tpaths = truth_files if truth_files is not None else self.truth_files
        tpl_paths = template_files if template_files is not None else self.template_files
        cfg_paths = gpt_config_files if gpt_config_files is not None else self.gpt_config_files

        truths = self._load_files(tpaths)
        if self.config.get("symbolic_passphrase"):
            truths["passphrase"] = self.config["symbolic_passphrase"]
        if truths:
            node["truths"] = truths

        templates = self._load_files(tpl_paths)
        if templates:
            node["templates"] = templates

        if cfg_paths:
            import yaml

            configs: Dict[str, Dict] = {}
            raw_configs = self._load_files(cfg_paths)
            for name, text in raw_configs.items():
                try:
                    data = yaml.safe_load(text) if text else {}
                except Exception:
                    data = {}
                handshake = self._extract_handshake(data)
                configs[name] = {"config": data, "handshake": handshake}
            if configs:
                node["gpt_configs"] = configs

        node["truth_vector_hash"] = self._hash_node(node)

        self.long_term.append(node)
        self._save_history()
