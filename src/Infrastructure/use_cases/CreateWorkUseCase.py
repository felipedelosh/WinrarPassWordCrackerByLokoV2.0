"""
FelipedelosH
2026
"""
# src\Infrastructure\use_cases\CreateWorkUseCase.py
from pathlib import Path
from src.Application.services.IWorkService import IWorkService
from src.Application.use_cases.ICreateWorkUseCase import ICreateWorkUseCase
from src.Models.Entities.WorkState import WorkState


class CreateWorkUseCase(ICreateWorkUseCase):
    def __init__(self, work_service: IWorkService):
        self.work_service = work_service

    def execute(
        self,
        rar_path: Path,
        charset: str,
        min_len: int,
        max_len: int,
        attack_mode: str
    ) -> WorkState:
        return self.work_service.create(
            rar_path=rar_path,
            charset=charset,
            min_len=min_len,
            max_len=max_len,
            attack_mode=attack_mode
        )
