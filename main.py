from src.services.character_service import CharacterService
from src.services.test_case_reader import TestCaseReader
from src.llm_models_enum import LLMModels


def main():
    config = TestCaseReader.load_from_yaml("data/test_scenarios/test_case_1.yaml")

    service = CharacterService(config)

    print("=== Conversation Starters ===")
    for i, starter in enumerate(service.get_conversation_starters(), 1):
        print(f"{i}. {starter}")
    print("\n=== Chat Start ===\n")

    messages = config.messages

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
