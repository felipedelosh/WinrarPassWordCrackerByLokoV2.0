"""
FelipedelosH
2026

Main application controller responsible for orchestrating
brute-force strategies, initializing required resources,
managing dependencies, and saving execution logs.
"""
import os
from datetime import datetime

from src.CORE.Config import Config
from src.CORE.FolderController import FolderController

class Controller:
    def __init__(self, path: str, config: Config, dependencies: dict):
        self.path = path
        self.dependencies = dependencies
        self.output_path = os.path.join(self.path, "OUTPUT")
        self.currentDate = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.config = config
        self.logger = self.dependencies["logger"]
        self.logger.info(f"Controller::__init__::START_AT::{self.currentDate}")
        FolderController.createInitalFolders(self.path, self.logger)

        # VARS


    def saveLogs(self):
        try:
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
            filename = f"logs_{timestamp}.log"
            full_path = os.path.join(self.output_path, filename)

            with open(full_path, "w", encoding="UTF-8") as f:
                f.write(self.logger.log)
            print(f"LOGs: {full_path}")
        except Exception as e:
            print(f"ERROR FATAL IN saveLogs: {e}")
