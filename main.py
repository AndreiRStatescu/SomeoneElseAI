from pathlib import Path
from src.services.small_language_model_train_service import (
    SmallLanguageModelTrainService,
)
from src.services.fine_tune_service import FineTuneService
from src.services.character_service import CharacterService
from src.services.openai_service import OpenAIService
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


def run_case_2():
    orra_context_path = Path("data/orra_enterprise_concatenated.md")
    orra_context = orra_context_path.read_text(encoding="utf-8")

    service = OpenAIService()
    model = LLMModels.GPT_5_1.value #GPT_5_NANO.value
    should_stream = LLMModels.is_gpt5_model(model)

    system_prompt = f"""You are ORRA, a numerology guidance assistant. Use the following knowledge base to answer questions:

{orra_context}

Provide guidance based on the ORRA system described above."""

    conversation_history = [{"role": "system", "content": system_prompt}]

    def print_stream_chunk(chunk: str) -> None:
        print(chunk, end="", flush=True)

    # test_messages = [
    #     "Calculate my daily guidance for birth date 13.06.1994 and date 22.12.2025",
    #     "What does Soul number 8 mean?",
    #     "Explain the ORRA Daily v1 format",
    # ]
    test_messages = [
        "Calculate my daily guidance for birth date and 28.09.1986 date 31.12.2025"
    ]

    for message in test_messages:
        print(f"You: {message}")
        conversation_history.append({"role": "user", "content": message})

        if should_stream:
            print("ORRA: ", end="", flush=True)

        result = service.generate_response(
            message=None,
            model=model,
            messages=conversation_history,
            stream=should_stream,
            stream_handler=print_stream_chunk if should_stream else None,
        )

        if should_stream:
            print()

        print(f"Status: {result.get('status')}")
        if result.get("response"):
            if not should_stream:
                print(f"ORRA: {result.get('response')}\n")
            conversation_history.append(
                {"role": "assistant", "content": result.get("response")}
            )
        else:
            print(f"Error: {result.get('error')}")
            if result.get("details"):
                print(f"Details: {result.get('details')}")
        print("-" * 50 + "\n")


def concatenate_orra_md_files(
    output_path: str = "data/orra_enterprise_concatenated.md",
) -> None:
    source_dir = Path("data/orra_enterprise_additional_exports")
    all_md_files = list(source_dir.glob("*.md"))

    master_file = source_dir / "ORRA_MASTER.md"
    other_files = sorted([f for f in all_md_files if f.name != "ORRA_MASTER.md"])

    md_files = [master_file] + other_files if master_file.exists() else other_files

    with open(output_path, "w", encoding="utf-8") as output_file:
        for md_file in md_files:
            separator = (
                f"\n{'=' * 80}\n{'=' * 80}\n{md_file.name}\n{'=' * 80}\n{'=' * 80}\n\n"
            )
            output_file.write(separator)
            content = md_file.read_text(encoding="utf-8")
            output_file.write(content)
            output_file.write("\n\n")

    print(f"Concatenated {len(md_files)} markdown files to {output_path}")


def main():
    # SmallLanguageModelTrainService().prepare_dataset()
    run_case_2()
    # concatenate_orra_md_files()


if __name__ == "__main__":
    main()
