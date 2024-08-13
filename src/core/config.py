import json
import os
from typing import Dict, Any


class Config:
    """
    A class to load and store the config and import file paths for the mod manager
    """

    def __init__(self, config_path: str = 'config/production_config.json'):
        """
        Initialise Config with a specified configuration file

        :param config_path: Absolute or Relative path to the configuration file
        """
        is_path_absolute = os.path.isabs(config_path)
        if is_path_absolute:
            self.config_path = config_path
        else:
            content_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
            self.config_path = os.path.join(content_root, config_path)

        self.config_data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the configuration from the initialised config json file

        :return: A dictionary containing the config data
        """
        try:
            with open(self.config_path, 'r') as file:
                config_data = json.load(file)
                print(f"Config loaded from {self.config_path}")
                return config_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {self.config_path}: {e}")
            return {}
        except FileNotFoundError:
            print(f"No configuration file found at {self.config_path}")
            return {}

