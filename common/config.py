"""
Configuration management for API credentials.
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()


class ConfigManager:
    """Manages configuration and credentials for API connections."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to a JSON configuration file (optional)
        """
        self.config: Dict[str, Any] = {}
        
        # Load configuration from file if provided
        if config_file:
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str) -> None:
        """
        Load configuration from a JSON file.
        
        Args:
            config_file: Path to a JSON configuration file
        """
        try:
            with open(config_file, 'r') as f:
                self.config.update(json.load(f))
            logger.info(f"Loaded configuration from {config_file}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load configuration from {config_file}: {e}")
    
    def load_from_env(self, prefix: str = "BOOMPAH_") -> None:
        """
        Load configuration from environment variables.
        
        Args:
            prefix: Prefix for environment variables to load
        """
        for key, value in os.environ.items():
            if key.startswith(prefix):
                # Convert BOOMPAH_WORDPRESS_URL to wordpress.url
                config_key = key[len(prefix):].lower().replace("_", ".")
                self._set_nested_key(self.config, config_key, value)
        
        logger.info(f"Loaded configuration from environment variables with prefix {prefix}")
    
    def _set_nested_key(self, config_dict: Dict[str, Any], key: str, value: Any) -> None:
        """
        Set a nested key in the configuration dictionary.
        
        Args:
            config_dict: Configuration dictionary
            key: Nested key (e.g., "wordpress.url")
            value: Value to set
        """
        if "." in key:
            main_key, rest = key.split(".", 1)
            if main_key not in config_dict:
                config_dict[main_key] = {}
            self._set_nested_key(config_dict[main_key], rest, value)
        else:
            config_dict[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (can be nested, e.g., "wordpress.url")
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        parts = key.split(".")
        value = self.config
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
                
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key (can be nested, e.g., "wordpress.url")
            value: Value to set
        """
        self._set_nested_key(self.config, key, value)
    
    def save_to_file(self, config_file: str) -> None:
        """
        Save configuration to a JSON file.
        
        Args:
            config_file: Path to a JSON configuration file
        """
        # Create directory if it doesn't exist
        Path(config_file).parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Saved configuration to {config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration to {config_file}: {e}")


# Default configuration manager instance
config = ConfigManager()
config.load_from_env()
