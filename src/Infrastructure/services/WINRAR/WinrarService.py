"""
FelipedelosH
2026
"""
# src\Infrastructure\services\WINRAR\WinrarService.py
from pathlib import Path
from src.Application.services.IWinrarService import IWinrarService


class WinrarService(IWinrarService):
    RAR4_SIGNATURE = b"Rar!\x1a\x07\x00"
    RAR5_SIGNATURE = b"Rar!\x1a\x07\x01\x00"

    def load(self, file_path: str) -> Path:
        if not file_path or not file_path.strip():
            raise ValueError("RAR file path cannot be empty.")

        rar_path = Path(file_path).expanduser().resolve()

        if not rar_path.is_file():
            raise FileNotFoundError(
                f"RAR file not found: {rar_path}"
            )

        if rar_path.suffix.lower() != ".rar":
            raise ValueError(
                f"Invalid RAR extension: {rar_path.name}"
            )

        with rar_path.open("rb") as file:
            signature = file.read(8)

        if not (
            signature.startswith(self.RAR4_SIGNATURE)
            or signature == self.RAR5_SIGNATURE
        ):
            raise ValueError(
                f"Invalid or unsupported RAR archive: {rar_path}"
            )

        return rar_path
