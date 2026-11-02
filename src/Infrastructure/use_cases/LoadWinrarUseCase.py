"""
FelipedelosH
2026
"""
# src\Infrastructure\use_cases\LoadWinrarUseCase.py
from pathlib import Path

from src.Application.services.IWinrarService import IWinrarService
from src.Application.use_cases.ILoadWinrarUseCase import ILoadWinrarUseCase


class LoadWinrarUseCase(ILoadWinrarUseCase):
    def __init__(self, winrar_service: IWinrarService):
        self.winrar_service = winrar_service

    def execute(self, file_path: str) -> Path:
        return self.winrar_service.load(file_path)
