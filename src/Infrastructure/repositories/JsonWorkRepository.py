"""
FelipedelosH
2026
"""
# src\Infrastructure\repositories\JsonWorkRepository.py
import json
import os
from dataclasses import asdict
from datetime import datetime
from typing import Optional
from src.Application.repositories.IWorkRepository import IWorkRepository
from src.Models.Entities.WorkState import WorkState


class JsonWorkRepository(IWorkRepository):

    def __init__(self, work_path: str):
        self.work_path = os.path.abspath(work_path)

    def exists(self) -> bool:
        return os.path.isfile(self.work_path)

    def load(self) -> Optional[WorkState]:
        if not self.exists():
            return None

        with open(self.work_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid work.json structure.")

        if data.get("version") != 1:
            raise ValueError(
                "Unsupported work.json version; migration is required."
            )

        return WorkState(**data)

    def save(self, state: WorkState) -> None:
        directory = os.path.dirname(self.work_path)
        os.makedirs(directory, exist_ok=True)

        temp_path = self.work_path + ".tmp"

        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(
                    asdict(state),
                    file,
                    indent=4,
                    ensure_ascii=False
                )
                file.flush()
                os.fsync(file.fileno())

            os.replace(temp_path, self.work_path)

        finally:
            if os.path.isfile(temp_path):
                os.remove(temp_path)

    def archive(self) -> Optional[str]:
        return self._move("archived")

    def backupCorrupt(self) -> Optional[str]:
        return self._move("corrupt")

    def _move(self, label: str) -> Optional[str]:
        if not self.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        destination = os.path.join(
            os.path.dirname(self.work_path),
            f"work.{label}.{timestamp}.json"
        )

        os.replace(self.work_path, destination)
        return destination
