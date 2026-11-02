"""
FelipedelosH
2026
"""
# src\Application\use_cases\ILoadWinrarUseCase.py

from abc import ABC, abstractmethod
from pathlib import Path


class ILoadWinrarUseCase(ABC):
    @abstractmethod
    def execute(self, file_path: str) -> Path:
        """
        Execute the RAR loading operation.

        Returns the validated archive path.
        """
        pass
