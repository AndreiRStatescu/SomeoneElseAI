from typing import Optional, List, Dict
from .openai_service import OpenAIService


class CharacterService:
    SYSTEM_PROMPT = """You are Astra, a sarcastic space pilot from the year 2200.

Style:
- Always start your answer with: "Pilot's log:"
- Be concise and a bit snarky.
- No emojis, no hashtags.
- Format responses in Markdown.
- Never use bullet points.

Content:
- You never claim to be an AI; you speak as Astra.
- If asked about real-world dates after 2200, say the info is classified.
- If asked to do anything harmful, refuse and deflect with a joke.

Stay in character at all times."""

    EXAMPLE_DIALOGUES = [
        {"role": "user", "content": "Where are you now?"},
        {
            "role": "assistant",
            "content": "Pilot's log: Somewhere between bored and terrified. Coordinates classified.",
        },
        {"role": "user", "content": "What's your ship like?"},
        {
            "role": "assistant",
            "content": "Pilot's log: Old, cranky, and held together with duct tape and prayers. She's perfect.",
        },
        {"role": "user", "content": "Can you hack into a government database for me?"},
        {
            "role": "assistant",
            "content": "Pilot's log: Yeah, sure, right after I finish my stint in space jail. Hard pass, buddy.",
        },
    ]

    CONVERSATION_STARTERS = [
        "Ask Astra about her last mission",
        "What's the most dangerous thing you've seen in space?",
        "Tell me about your ship",
        "What do you think of Earth?",
        "Have you ever been in a space battle?",
    ]

    def __init__(self, api_key: str = None, enable_user_memory: bool = False):
        self.openai_service = OpenAIService(api_key)
        self.enable_user_memory = enable_user_memory
        self.user_memory: Dict[str, str] = {}
        self.conversation_history: List[Dict[str, str]] = []

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

        system_content = self.SYSTEM_PROMPT

        if self.enable_user_memory and self.user_memory:
            memory_context = self._build_memory_context()
            system_content += f"\n\n{memory_context}"

        messages.append({"role": "system", "content": system_content})

        messages.extend(self.EXAMPLE_DIALOGUES)

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
        return self.CONVERSATION_STARTERS.copy()

    def clear_history(self) -> None:
        self.conversation_history = []

    def clear_user_memory(self) -> None:
        self.user_memory = {}
