"""
FelipedelosH
2026

Centralized Dependency Injector.
"""
# src\CORE\DependencyInjector.py
import os
from src.CORE.Config import Config
from src.CORE.Logger import Logger

# REPOSITORIES
from src.Infrastructure.repositories.JsonWorkRepository import JsonWorkRepository
# SERVICES
from src.Infrastructure.services.WINRAR.WinrarService import WinrarService
from src.Infrastructure.services.WorkService import WorkService
# USE CASES
from src.Infrastructure.use_cases.LoadWinrarUseCase import LoadWinrarUseCase
from src.Infrastructure.use_cases.CreateWorkUseCase import CreateWorkUseCase

class DependencyInjector:
    @staticmethod
    def build_dependencies(path: str, config: Config) -> dict:
        # LOGGER
        logger = Logger(config.getConfig("GEN_CONFIG_DISPLAY_LOGS"))

        # Get Attack Characters
        characters_file = config.getConfig("GEN_CONFIG_CHARACTERS_ARR_INPUT_FILE")
        if not characters_file:
            raise ValueError("GEN_CONFIG_CHARACTERS_ARR_INPUT_FILE is not configured.")

        characters_path = os.path.abspath(os.path.join(path, characters_file))
        if not os.path.isfile(characters_path):
            raise FileNotFoundError(f"Characters file not found: {characters_path}")

        with open(characters_path, "r", encoding="utf-8-sig") as file:
            content = file.read()
        charset = "".join(
            char for char in content
            if char not in ", \n\r\t"
        )
        # Remove duplicate characters, preserving order.
        charset = "".join(dict.fromkeys(charset))
        if not charset:
            raise ValueError("The characters file does not contain valid characters.")
        characters = list(charset)
        logger.info(f"DependencyInjector::CHARACTERS_LOADED::QTY::{len(characters)}")

        # REPOSITORES
        work_repository = JsonWorkRepository(os.path.join(path, "TEMP", "work.json"))

        # SERVICES
        winrar_service = WinrarService()
        work_service = WorkService(repository=work_repository)

        # USE CASES
        load_winrar_use_case = LoadWinrarUseCase(
            winrar_service=winrar_service
        )

        create_work_use_case = CreateWorkUseCase(
            work_service=work_service
        )
        
        return {
            "logger": logger,
            "characters": characters,
            "charset": charset,
            "load_winrar_use_case": load_winrar_use_case,
            "create_work_use_case": create_work_use_case
        }
