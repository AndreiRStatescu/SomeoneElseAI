from typing import Optional, List, Dict
from pathlib import Path
from .openai_service import OpenAIService
from ..models.character import Character
from .character_reader import CharacterReader


class CharacterService:
    def __init__(
        self,
        api_key: str = None,
        enable_user_memory: bool = False,
        character_file: str = None,
    ):
        self.openai_service = OpenAIService(api_key)
        self.enable_user_memory = enable_user_memory
        self.user_memory: Dict[str, str] = {}
        self.conversation_history: List[Dict[str, str]] = []

        if character_file is None:
            base_path = Path(__file__).parent.parent.parent
            character_file = str(base_path / "data" / "characters" / "astra.yaml")

        self.character = CharacterReader.load_from_yaml(character_file)

    def set_user_info(self, name: str = None, **kwargs) -> None:
        if name:
            self.user_memory["name"] = name

        for key, value in kwargs.items():
            self.user_memory[key] = value

    def _build_memory_context(self) -> str:
        if not self.user_memory:
            return ""

        memory_parts = []
        if "name" in self.user_memory:
            memory_parts.append(
                f"The user's name is {self.user_memory['name']}. You remember and use this in conversation."
            )

        for key, value in self.user_memory.items():
            if key != "name":
                memory_parts.append(f"The user {key}: {value}")

        return " ".join(memory_parts) if memory_parts else ""

    def _build_messages(
        self, user_message: str, include_history: bool = False
    ) -> List[Dict[str, str]]:
        messages = []

        system_content = self.character.get_system_prompt()

        if self.enable_user_memory and self.user_memory:
            memory_context = self._build_memory_context()
            system_content += f"\n\n{memory_context}"

        messages.append({"role": "system", "content": system_content})

        messages.extend(self.character.get_example_dialogues())

        if include_history and self.conversation_history:
            messages.extend(self.conversation_history)

        messages.append({"role": "user", "content": user_message})

        return messages

    def generate_response(
        self,
        message: str,
        model: str = None,
        include_history: bool = False,
        save_to_history: bool = False,
    ) -> dict:
        if not message or not isinstance(message, str):
            return {"error": "Message is required", "status": 400}

        try:
            messages = self._build_messages(message, include_history)

            response = self.openai_service.generate_response(
                message=None, model=model, messages=messages
            )

            if response.get("status") != 200:
                return response

            response_text = response["response"]

            if save_to_history:
                self.conversation_history.append({"role": "user", "content": message})
                self.conversation_history.append(
                    {"role": "assistant", "content": response_text}
                )

            return {"response": response_text, "status": 200}

        except Exception as error:
            print(f"Character Service Error: {error}")
            return {
                "error": "Failed to generate response",
                "details": str(error),
                "status": 500,
            }

    def get_conversation_starters(self) -> List[str]:
        return self.character.get_conversation_starters()

    def clear_history(self) -> None:
        self.conversation_history = []

    def clear_user_memory(self) -> None:
        self.user_memory = {}
