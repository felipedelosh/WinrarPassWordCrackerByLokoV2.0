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


        
        return {
            "logger": logger,
            "characters": characters,
            "charset": charset
        }
