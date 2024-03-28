import json
import os
from typing import Any, Union, List

class ConfigManager:
    def __init__(self, file_path: str = 'config.json') -> None:
        """Initialize the ConfigManager.

        Args:
            file_path (str, optional): The path to the configuration file. Default is 'config.json'.
        """
        self.file_path = file_path
        self.config = {}
        self.cache = {}

    def read_config(self) -> None:
        """Read the configuration file."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    self.config = json.load(f)
        except Exception as e:
            print(f"Error reading configuration file: {e}")

    def read_key(self, section: str, key: str, data_type: type = str) -> Any:
        """Read a key from the configuration file.

        Args:
            section (str): The section in the configuration file.
            key (str): The key to be read.
            data_type (type, optional): The expected data type of the key's value. Default is str.

        Returns:
            The value of the key converted to the specified data type.
        """
        cache_key = f"{section}.{key}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        if section in self.config and key in self.config[section]:
            value = self.config[section][key]
        else:
            raise ValueError(f"Key '{key}' not found in section '{section}'")
        value = self._convert_to_data_type(value, data_type)
        self.cache[cache_key] = value
        return value

    def _convert_to_data_type(self, value: str, data_type: type) -> Any:
        """Convert the value to the specified data type.

        Args:
            value (str): The value to be converted.
            data_type (type): The expected data type.

        Returns:
            The value converted to the specified data type.
        """
        if data_type == int:
            return int(value)
        elif data_type == bool:
            return bool(value)
        elif data_type == list:
            return value if isinstance(value, list) else [item.strip() for item in value.split(',')]
        elif data_type == type(None):
            return None
        else:
            return value
        
    def get(self, section: str, key: str) -> Any:
        """Read a value from the configuration file.

        Args:
            section (str): The section in the configuration file.
            key (str): The key to be read.

        Returns:
            The value associated with the key.
        """
        return self.read_key(section, key)

    def get_int(self, section: str, key: str) -> int:
        """Read an integer value from the configuration file.

        Args:
            section (str): The section in the configuration file.
            key (str): The key to be read.

        Returns:
            int: The integer value.
        """
        return self.read_key(section, key, int)
    
    def get_float(self, section: str, key: str) -> int:
        """Read an float value from the configuration file.

        Args:
            section (str): The section in the configuration file.
            key (str): The key to be read.

        Returns:
            float: The float value.
        """
        return self.read_key(section, key, float)

    def get_bool(self, section: str, key: str) -> bool:
        """Read a boolean value from the configuration file.

        Args:
            section (str): The section in the configuration file.
            key (str): The key to be read.

        Returns:
            bool: The boolean value.
        """
        return self.read_key(section, key, bool)

    def get_list(self, section: str, key: str) -> List[str]:
        """Read a list value from the configuration file.

        Args:
            section (str): The section in the configuration file.
            key (str): The key to be read.

        Returns:
            list: The list value.
        """
        return self.read_key(section, key, list)
    
    def get_dict(self, section: str, key: str) -> dict:
        """Read a dictionary value from the configuration file.

        Args:
            section (str): The section in the configuration file.
            key (str): The key to be read.

        Returns:
            dict: The dictionary value.
        """
        return self.read_key(section, key, dict)

    def set_key(self, section: str, key: str, value: Any) -> None:
        """Set a key in the configuration file.

        Args:
            section (str): The section in the configuration file.
            key (str): The key to be set.
            value (Any): The value to be associated with the key.
        """
        try:
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
            cache_key = f"{section}.{key}"
            self.cache[cache_key] = value
            self.write_config()
        except Exception as e:
            print(f"Error setting key '{key}' in section '{section}': {e}")

    def write_config(self) -> None:
        """Write the configuration to the file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error writing configuration file: {e}")
            

# Initialize
config_manager = ConfigManager()
config_manager.read_config()
