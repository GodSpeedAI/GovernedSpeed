from __future__ import annotations

from typing import Protocol


class ConfigurationPort(Protocol):
    """Abstract port responsible for providing the policy configuration."""

    def load(self) -> dict:
        """Return the latest configuration data for the gateway."""
        ...
