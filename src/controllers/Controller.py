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

    def crackPassWordBruteForce(self):
        try:
            self.logger.info("Controller::crackPassWordBruteForce::TRY")
            winrar_loader = self._loadWinrar()
            worker_loader = self._loadWork(winrar_loader)


        except Exception as e:
            self.logger.error(f"Controller::crackPassWordBruteForce::ERROR::{str(e)}")


    def _loadWinrar(self):
        try:
            self.logger.info("Controller::_loadWinrar::TRY")
            rar_file = self.config.getConfig("RAR_FILE_TO_CRACK")

            if not rar_file:
                self.logger.error(f"Controller::_loadWinrar::ERROR::NOT_FILE::{rar_file}")
                return

            rar_path = os.path.join(self.path, rar_file)
            self.logger.info(f"Controller::_loadWinrar::{rar_path}")
            use_case = self.dependencies["load_winrar_use_case"]
            result = use_case.execute(rar_path)

            self.logger.info("Controller::_loadWinrar::OK")
            return result
        except Exception as e:
            self.logger.error(f"Controller::_loadWinrar::ERROR::{str(e)}")
            return None


    def _loadWork(self, rar_path):
        try:
            self.logger.info("Controller::_loadWork::TRY")

            state = self.dependencies["create_work_use_case"].execute(
                rar_path=rar_path,
                charset=self.dependencies["charset"],
                min_len=self.config.getConfig(
                    "GEN_CONFIG_LEN_MIN_SIZE_CHAR_SELECT_TO_CRACK"
                ),
                max_len=self.config.getConfig(
                    "GEN_CONFIG_LEN_MAX_SIZE_CHAR_SELECT_TO_CRACK"
                ),
                attack_mode=self.config.getConfig(
                    "GEN_CONFIG_ATTACK_MODE"
                )
            )

            # CREATE? LOADED? CONTINUE PREVIUS?

        except Exception as e:
            self.logger.error(f"Controller::_loadWork::ERROR::{str(e)}")
            return None

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
