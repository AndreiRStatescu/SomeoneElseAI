from typing import List, Dict


class Character:
    def __init__(self):
        self.name: str = ""
        self.system_prompt: str = ""
        self.example_dialogues: List[Dict[str, str]] = []
        self.conversation_starters: List[str] = []

    def get_system_prompt(self) -> str:
        return self.system_prompt

    def get_example_dialogues(self) -> List[Dict[str, str]]:
        return self.example_dialogues

    def get_conversation_starters(self) -> List[str]:
        return self.conversation_starters.copy()
