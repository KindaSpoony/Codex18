"""Minimal YAML loader stub for tests."""
from __future__ import annotations
from typing import Any, Union, IO
import json


def _parse_value(val: str) -> Any:
    if val.lower() in {"true", "false"}:
        return val.lower() == "true"
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            return val


def safe_load(stream: Union[str, IO[str]]) -> Any:
    """Parse extremely simple YAML or JSON without external deps."""
    if hasattr(stream, "read"):
        text = stream.read()
    else:
        text = str(stream)
    text = text.strip()
    if not text:
        return {}
    if text.startswith("{") and text.endswith("}"):
        try:
            return json.loads(text)
        except Exception:
            pass
    lines = text.splitlines()
    root: Any = {}
    stack: list[tuple[int, Any]] = [(0, root)]
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        while stack and indent < stack[-1][0]:
            stack.pop()
        container = stack[-1][1]
        if line.startswith("- "):
            val = line[2:].strip()
            item: Any
            if ":" in val:
                k, v = val.split(":", 1)
                item = {k.strip(): _parse_value(v.strip())}
            else:
                item = _parse_value(val)
            if isinstance(container, list):
                container.append(item)
            else:
                # start new list for current key placeholder
                lst = []
                stack[-1] = (stack[-1][0], lst)
                lst.append(item)
        elif ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val == "":
                # look ahead to determine container type
                j = i + 1
                next_is_list = False
                while j < len(lines):
                    nxt = lines[j]
                    if not nxt.strip() or nxt.lstrip().startswith("#"):
                        j += 1
                        continue
                    next_is_list = nxt.strip().startswith("- ")
                    break
                new: Any = [] if next_is_list else {}
                if isinstance(container, list):
                    container.append({key: new})
                else:
                    container[key] = new
                stack.append((indent + 2, new))
            else:
                if isinstance(container, list):
                    container.append({key: _parse_value(val)})
                else:
                    container[key] = _parse_value(val)
        i += 1
    return root
