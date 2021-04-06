import os
import logging

from shweb.config import Config
from shweb.log import get_logger


class Environment:
    service_name: str = "service-sample-creator"
    path_env_var: str = "SERVICE_CONFIG_PATH"
    config: Config = Config()
    logger = logging.getLogger(service_name)

    def __init__(self):
        self.init_logger()
        self.config.load(os.environ.get(self.path_env_var, None), "env")

    def info(self) -> None:
        for par_name in self.config.mapping:
            self.logger.info(f"{par_name.upper()}: {getattr(self.config, par_name)}")

    def init_logger(self):
        self.logger = get_logger(self.service_name, "INFO")


Environment().info()
