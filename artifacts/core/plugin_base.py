"""
Base plugin interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

class Plugin(ABC):
    @abstractmethod
    def apply(self, context: Dict[str, Any]) -> None:
        """Apply this plugin to the given context (archive root, config, etc.)."""
        raise NotImplementedError
