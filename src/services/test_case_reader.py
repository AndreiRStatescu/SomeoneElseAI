import yaml
from typing import Dict, Any
from pathlib import Path
from ..models.test_case_config import TestCaseConfig


class TestCaseReader:
    @staticmethod
    def load_from_yaml(config_file: str) -> TestCaseConfig:
        config_path = Path(config_file)

        if not config_path.exists():
            raise FileNotFoundError(f"Test case config file not found: {config_file}")

        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return TestCaseReader._create_config_from_data(data)

    @staticmethod
    def _create_config_from_data(data: Dict[str, Any]) -> TestCaseConfig:
        config = TestCaseConfig()
        config.character_file = data.get("character_file", "")
        config.enable_user_memory = data.get("enable_user_memory", False)
        config.user_name = data.get("user_name", "")
        config.user_interests = data.get("user_interests", "")
        config.messages = data.get("messages", [])
        return config
