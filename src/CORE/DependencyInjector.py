"""
FelipedelosH
2026

Centralized Dependency Injector.
"""
# src\CORE\DependencyInjector.py
import os
from src.CORE.Config import Config
from src.CORE.Logger import Logger

class DependencyInjector:
    @staticmethod
    def build_dependencies(path: str, config: Config) -> dict:

        
        # LOGGER
        logger = Logger(config.getConfig("GEN_CONFIG_DISPLAY_LOGS"))

        return {
            "logger": logger
        }
