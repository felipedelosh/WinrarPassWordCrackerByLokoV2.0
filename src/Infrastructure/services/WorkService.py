"""
FelipedelosH
2026
"""
# src\Infrastructure\services\WorkService.py
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from src.Application.repositories.IWorkRepository import IWorkRepository
from src.Application.services.IWorkService import IWorkService
from src.Models.Entities.WorkState import WorkState


class WorkService(IWorkService):
    def __init__(self, repository: IWorkRepository):
        self.repository = repository

    def create(
        self,
        rar_path: Path,
        charset: str,
        min_len: int,
        max_len: int,
        attack_mode: str
    ) -> WorkState:

        rar_path = Path(rar_path).resolve()

        if not rar_path.is_file():
            raise FileNotFoundError(
                f"RAR file not found: {rar_path}"
            )

        if not charset:
            raise ValueError("Charset cannot be empty.")

        if not isinstance(min_len, int) or not isinstance(max_len, int):
            raise ValueError("Password lengths must be integers.")

        if min_len < 1 or max_len < min_len:
            raise ValueError("Invalid password length range.")

        if not attack_mode or not str(attack_mode).strip():
            raise ValueError("Attack mode cannot be empty.")

        digest = hashlib.sha256()

        with rar_path.open("rb") as file:
            for chunk in iter(lambda: file.read(65536), b""):
                digest.update(chunk)

        sha256 = digest.hexdigest()
        mode = str(attack_mode).strip()

        total = sum(
            len(charset) ** length
            for length in range(min_len, max_len + 1)
        )

        if self.repository.exists():
            previous = self.repository.load()

            if previous is None:
                raise ValueError(
                    "The work file exists but cannot be loaded."
                )

            same_job = (
                previous.rar_sha256 == sha256
                and previous.charset == charset
                and previous.min_len == min_len
                and previous.max_len == max_len
                and previous.attack_mode == mode
            )

            if not same_job:
                raise ValueError(
                    "TEMP/work.json belongs to another configuration. "
                    "Back it up explicitly before creating a different job."
                )

            return previous

        created_at = datetime.now(timezone.utc).isoformat()

        state = WorkState(
            password_found=False,
            rar_file=rar_path.name,
            rar_sha256=sha256,
            rar_size_bytes=rar_path.stat().st_size,
            charset=charset,
            min_len=min_len,
            max_len=max_len,
            attack_mode=mode,
            created_at=created_at,
            updated_at=None,
            status="NEW",
            total_colonies=max_len - min_len + 1,
            total_combinations=total
        )

        self.repository.save(state)

        return state
