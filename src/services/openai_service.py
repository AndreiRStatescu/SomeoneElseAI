import os
from openai import OpenAI
from dotenv import load_dotenv
from ..llm_models_enum import LLMModels

load_dotenv(".env.local")


class OpenAIService:
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.default_model = LLMModels.GPT_5_NANO

    def call_gpt5_model(self, message: str, model: str) -> str:
        completion = self.client.chat.completions.create(
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

    def call_gpt4_model(self, message: str, model: str) -> str:
        completion = self.client.chat.completions.create(
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

    def generate_response(self, message: str, model: str = None) -> dict:
        if not message or not isinstance(message, str):
            return {"error": "Message is required", "status": 400}

        selected_model = model or self.default_model.value
        supported_models = [m.value for m in LLMModels]
        if selected_model not in supported_models:
            return {
                "error": f"Invalid model. Supported models: {', '.join(supported_models)}",
                "status": 400,
            }

        try:
            if LLMModels.is_gpt5_model(selected_model):
                response_text = self.call_gpt5_model(message, selected_model)
            else:
                response_text = self.call_gpt4_model(message, selected_model)

            return {"response": response_text, "status": 200}
        except Exception as error:
            print(f"OpenAI API Error: {error}")
            return {
                "error": "Failed to generate response",
                "details": str(error),
                "status": 500,
            }
