"""
FelipedelosH
2026
"""
# src\Models\Entities\WorkState.py
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkState:
    version: int = 1
    password_found: bool = False

    rar_file: str = ""
    rar_sha256: str = ""
    rar_size_bytes: int = 0

    charset: str = ""
    min_len: int = 0
    max_len: int = 0
    attack_mode: str = ""

    created_at: str = ""
    updated_at: Optional[str] = None

    status: str = "NEW"

    completed_colonies: List[int] = field(default_factory=list)
    current_colony: Optional[int] = None
    current_colony_index: int = -1

    total_colonies: int = 0
    total_combinations: int = 0
    total_combinations_tried: int = 0

    completed_at: Optional[str] = None
    flush_interval: int = 100

    extra: Dict[str, Any] = field(default_factory=dict)
