"""Configuration loader for search tool"""
import yaml
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Load and manage YAML configuration"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            if not self.config_path.exists():
                logger.warning(f"Config file not found: {self.config_path}")
                return {}
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
            
            logger.info(f"Configuration loaded from {self.config_path}")
            return self.config
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value with dot notation (e.g., 'app.name')"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire config section"""
        return self.config.get(section, {})
    
    def set(self, key: str, value: Any) -> None:
        """Set config value (in-memory only)"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, path: Optional[str] = None) -> bool:
        """Save configuration to YAML file"""
        try:
            target_path = Path(path or self.config_path)
            with open(target_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)
            logger.info(f"Configuration saved to {target_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
            return False
    
    def reload(self) -> None:
        """Reload configuration from file"""
        self.load()
        logger.info("Configuration reloaded")

# Global config instance
config = ConfigLoader()
