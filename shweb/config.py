# ==============================================================================
# Copyright 2020 Sreda Software Solutions. All rights reserved.
# The copyright notice above does not evidence any actual or
# intended publication of such source code. The code contains
# Sreda Software Solutions Confidential Proprietary Information.
# ==============================================================================

import os
import json
import importlib.util


class Config():
    def __init__(self) -> None:
        # default vars from env
        self.port: int = "9090"

        # env_vars here
        self.mapping = {
            "port": int,
        }

        for par_name in self.mapping:
            self._map(par_name, getattr(self, par_name))

    def _map(self, par_name, value):
        if par_name != "mapping":
            setattr(self, par_name, self.mapping[par_name](value))

    def _check_env(self, par_name: str):
        env_style_par_name = par_name.upper()
        if env_style_par_name in os.environ:
            self._map(par_name, os.environ[env_style_par_name])

    def load(self, config_path: str, root_key: str = None):
        if config_path:
            if config_path.endswith(".py"):
                self.from_object(config_path)
            elif config_path.endswith(".json"):
                self.from_json(config_path, root_key)
            elif config_path.endswith(".yml") or config_path.endswith(".yaml"):
                self.from_yaml(config_path, root_key)
            else:
                raise TypeError("Config file must be .py or .json")
        else:
            self.from_env()

    def from_dict(self, dict_config: dict, root_key: str = None):
        if root_key is not None:
            dict_config = dict_config[root_key]

        for par_name in self.mapping:
            env_style_par_name = par_name.upper()
            if env_style_par_name in dict_config:
                self._map(par_name, dict_config[env_style_par_name])
            else:
                self._check_env(par_name)

    def from_object(self, path_to_config: str) -> None:
        # Import external config if exists
        if path_to_config.startswith("./"):
            path_to_config = f"{os.getcwd()}/{path_to_config[2:]}"
        elif path_to_config.startswith("/"):
            pass
        else:
            path_to_config = f"{os.getcwd()}/{path_to_config}"

        spec = importlib.util.spec_from_file_location("config", path_to_config)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)

        for par_name in self.mapping:
            env_style_par_name = par_name.upper()
            if hasattr(config, env_style_par_name):
                self._map(par_name, getattr(config, env_style_par_name))
            else:
                self._check_env(par_name)

    def from_json(self, path_to_config: str, root_key: str = None):
        with open(path_to_config, 'r') as jc:
            dict_config = json.load(jc)
        self.from_dict(dict_config, root_key)

    def from_yaml(self, path_to_config: str, root_key: str = None):
        import yaml
        with open(path_to_config, 'r') as yc:
            documents = yaml.safe_load_all(yc)
            for dict_config in documents:
                if root_key in dict_config:
                    self.from_dict(dict_config, root_key)
                    break

    def from_env(self):
        for par_name in self.mapping:
            self._check_env(par_name)
