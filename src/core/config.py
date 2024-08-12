import json
import os
from typing import Dict, Any


class Config:
    """
    A class to load and store the config and import file paths for the mod manager
    """

    def __init__(self, config_file: str = 'config/mod_config.json'):
        """
        Initialise Config with a specified configuration file

        :param config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config_data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the configuration from the initialised config json file

        :return: A dictionary containing the config data
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as file:
                    config_data = json.load(file)
                    print(f"Config loaded from {self.config_file}")
                    return config_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {self.config_file}: {e}")
                return {}
        else:
            print(f"No configuration file found at {self.config_file}")
            return {}

