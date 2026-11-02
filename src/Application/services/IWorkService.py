"""
FelipedelosH
2026
"""
# src\Application\services\IWorkService.py
from abc import ABC, abstractmethod
from pathlib import Path
from src.Models.Entities.WorkState import WorkState


class IWorkService(ABC):

    @abstractmethod
    def create(
        self,
        rar_path: Path,
        charset: str,
        min_len: int,
        max_len: int,
        attack_mode: str
    ) -> WorkState:
        pass
