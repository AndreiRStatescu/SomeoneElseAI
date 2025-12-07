from typing import List


class TestCaseConfig:
    def __init__(self):
        self.character_file: str = ""
        self.enable_user_memory: bool = False
        self.user_name: str = ""
        self.user_interests: str = ""
        self.messages: List[str] = []
