from src.services.small_language_model_train_service import SmallLanguageModelTrainService
from src.services.fine_tune_service import FineTuneService
from src.services.character_service import CharacterService
from src.services.test_case_reader import TestCaseReader
from src.models.llm_models_enum import LLMModels


def run_case():
    config = TestCaseReader.load_from_yaml("data/test_scenarios/test_case_astra.yaml")

    service = CharacterService(config)
    model = LLMModels.GPT_5_NANO.value
    should_stream = LLMModels.is_gpt5_model(model)

    def print_stream_chunk(chunk: str) -> None:
        print(chunk, end="", flush=True)

    for message in config.messages:
        print(f"You: {message}")
        if should_stream:
            print("Astra: ", end="", flush=True)

        result = service.generate_response(
            message=message,
            model=model,
            save_to_history=True,
            stream=should_stream,
            stream_handler=print_stream_chunk if should_stream else None,
        )

        if should_stream:
            print()

        print(f"Status: {result.get('status')}")
        if result.get("response") and not should_stream:
            print(f"Astra: {result.get('response')}\n")
        elif not result.get("response"):
            print(f"Error: {result.get('error')}")
            if result.get("details"):
                print(f"Details: {result.get('details')}")
        print("-" * 50 + "\n")


def run_fine_tune():
    fine_tune_service = FineTuneService()
    fine_tune_service.run()


def main():
    SmallLanguageModelTrainService().prepare_dataset()


if __name__ == "__main__":
    main()
