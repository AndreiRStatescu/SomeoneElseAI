import yaml
from typing import Dict, Any
from pathlib import Path
from ..models.character import Character


class CharacterReader:
    @staticmethod
    def load_from_yaml(character_file: str) -> Character:
        character_path = Path(character_file)

        if not character_path.exists():
            raise FileNotFoundError(f"Character file not found: {character_file}")

        with open(character_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return CharacterReader._create_character_from_data(data)

    @staticmethod
    def _create_character_from_data(data: Dict[str, Any]) -> Character:
        character = Character()
        character.name = data.get("name", "Unknown")
        character.system_prompt = data.get("system_prompt", "")
        character.example_dialogues = data.get("example_dialogues", [])
        character.conversation_starters = data.get("conversation_starters", [])
        return character
