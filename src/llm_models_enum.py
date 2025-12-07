from enum import Enum


class LLMModels(Enum):
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1_NANO = "gpt-4.1-nano"
    GPT_5_NANO = "gpt-5-nano"
    GPT_5 = "gpt-5"
    GPT_5_MINI = "gpt-5-mini"
    GPT_5_1 = "gpt-5.1"

    @classmethod
    def is_gpt5_model(cls, model_str: str) -> bool:
        return model_str.startswith("gpt-5")
