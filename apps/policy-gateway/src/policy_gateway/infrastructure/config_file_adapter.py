from __future__ import annotations

import json
import os
from pathlib import Path

import yaml
from policy_gateway.ports.configuration import ConfigurationPort


class ConfigFileAdapter(ConfigurationPort):
    """Adapter that loads configuration data from a JSON or YAML file."""

    def __init__(self, path: str | os.PathLike[str]):
        self._path = Path(path)

    def load(self) -> dict:
        """Load and parse the configuration file.

        Returns an empty dict for missing files or invalid content so callers can
        safely consume the adapter in tests and runtime.
        """
        if not self._path.exists():
            return {}
        try:
            raw = self._path.read_text(encoding="utf-8")
        except OSError:
            # If the file cannot be read, treat it as missing/empty for safety.
            return {}

        if self._path.suffix in {".yml", ".yaml"}:
            try:
                parsed = yaml.safe_load(raw)
                # yaml.safe_load may return non-dict types for simple values
                # (e.g., a list or string). Ensure we return a dict per API.
                return parsed if isinstance(parsed, dict) else {}
            except yaml.YAMLError:
                return {}

        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}
