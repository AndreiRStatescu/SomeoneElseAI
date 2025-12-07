import os
from openai import OpenAI
from dotenv import load_dotenv
from ..llm_models_enum import LLMModels

load_dotenv(".env.local")


class OpenAIService:
    def __init__(self, api_key: str = None):
        self._client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self._default_model = LLMModels.GPT_5_NANO

    def _call_gpt5_model(self, message: str, model: str) -> str:
        completion = self._client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions concisely and accurately.",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            max_completion_tokens=1000,
        )
        return completion.choices[0].message.content or "No response generated"

    def _call_gpt4_model(self, message: str, model: str) -> str:
        completion = self._client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions concisely and accurately.",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        return completion.choices[0].message.content or "No response generated"

    def generate_response(
        self, message: str, model: str = None, messages: list = None
    ) -> dict:
        if messages is None and (not message or not isinstance(message, str)):
            return {"error": "Message is required", "status": 400}

        selected_model = model or self._default_model.value
        supported_models = [m.value for m in LLMModels]
        if selected_model not in supported_models:
            return {
                "error": f"Invalid model. Supported models: {', '.join(supported_models)}",
                "status": 400,
            }

        try:
            if messages is not None:
                if LLMModels.is_gpt5_model(selected_model):
                    completion = self._client.chat.completions.create(
                        model=selected_model,
                        messages=messages,
                        max_completion_tokens=2000,
                    )
                else:
                    completion = self._client.chat.completions.create(
                        model=selected_model,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=1000,
                    )

                if not completion.choices:
                    return {"error": "No completion choices returned", "status": 500}

                choice = completion.choices[0]

                if choice.message.refusal:
                    return {
                        "error": f"Request refused: {choice.message.refusal}",
                        "status": 400,
                    }

                response_text = choice.message.content

                if not response_text:
                    return {
                        "error": f"Empty response from API (finish_reason: {choice.finish_reason})",
                        "status": 500,
                    }
            else:
                if LLMModels.is_gpt5_model(selected_model):
                    response_text = self._call_gpt5_model(message, selected_model)
                else:
                    response_text = self._call_gpt4_model(message, selected_model)

            return {"response": response_text, "status": 200}
        except Exception as error:
            print(f"OpenAI API Error: {error}")
            return {
                "error": "Failed to generate response",
                "details": str(error),
                "status": 500,
            }
