"""Minimal YAML loader stub for tests."""
import json
from typing import Any, Union, IO

def safe_load(stream: Union[str, IO[str]]) -> Any:
    """Parse a very simple YAML file using JSON syntax."""
    if hasattr(stream, "read"):
        text = stream.read()
    else:
        text = str(stream)
    return json.loads(text)
