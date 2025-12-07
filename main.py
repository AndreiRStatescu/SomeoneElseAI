from src.services.character_service import CharacterService
from src.llm_models_enum import LLMModels


def main():
    service = CharacterService(
        character_file="data/characters/cipher.yaml", enable_user_memory=True
    )

    service.set_user_info(name="Alex", interests="cybersecurity and privacy")

    print("=== Conversation Starters ===")
    for i, starter in enumerate(service.get_conversation_starters(), 1):
        print(f"{i}. {starter}")
    print("\n=== Chat with Cipher ===\n")

    messages = [
        "What do you do?",
        "Tell me about Neo-Tokyo",
        "What's the biggest threat to privacy?",
    ]

    for message in messages:
        print(f"You: {message}")
        result = service.generate_response(
            message=message,
            model=LLMModels.GPT_5_NANO.value,
            save_to_history=True,
        )

        print(f"Status: {result.get('status')}")
        if result.get("response"):
            print(f"Cipher: {result.get('response')}\n")
        else:
            print(f"Error: {result.get('error')}")
            if result.get("details"):
                print(f"Details: {result.get('details')}")
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()
