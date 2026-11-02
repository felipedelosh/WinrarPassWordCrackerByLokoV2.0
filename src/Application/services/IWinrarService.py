"""
FelipedelosH
2026
"""
# src\Application\services\IWinrarService.py

from abc import ABC, abstractmethod
from pathlib import Path


class IWinrarService(ABC):
    @abstractmethod
    def load(self, file_path: str) -> Path:
        """
        Load and validate a RAR archive.

        Returns the absolute path of the validated archive.

        Raises:
            FileNotFoundError: Archive does not exist.
            ValueError: Invalid path or unsupported archive.
            OSError: Archive cannot be read.
        """
        pass
