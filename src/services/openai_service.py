import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env.local")


class OpenAIService:
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model_gpt_5_nano = "gpt-5-nano"

    def call_gpt5_model(self, message: str, mode: str, model: str) -> str:
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that answers questions concisely and accurately."
                        if mode == "ask"
                        else "You are a helpful writing assistant that helps users create content. Provide clear, well-written responses."
                    ),
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            max_completion_tokens=1000,
        )
        return completion.choices[0].message.content or "No response generated"

    def call_gpt4_model(self, message: str, mode: str, model: str) -> str:
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that answers questions concisely and accurately."
                        if mode == "ask"
                        else "You are a helpful writing assistant that helps users create content. Provide clear, well-written responses."
                    ),
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

    def generate_response(self, message: str, mode: str, model: str = None) -> dict:
        if not message or not isinstance(message, str):
            return {"error": "Message is required", "status": 400}

        if not mode or mode not in ["ask", "write"]:
            return {"error": "Invalid mode", "status": 400}

        selected_model = model or self.model_gpt_5_nano
        if not selected_model.startswith("gpt-4") and not selected_model.startswith(
            "gpt-5"
        ):
            return {
                "error": "Invalid model. Supported models: any gpt-4 variant (e.g., gpt-4, gpt-4-turbo, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano) and any gpt-5 variant (e.g., gpt-5-nano, gpt-5, gpt-5-mini, gpt-5.1)",
                "status": 400,
            }

        try:
            if selected_model.startswith("gpt-5"):
                response_text = self.call_gpt5_model(message, mode, selected_model)
            else:
                response_text = self.call_gpt4_model(message, mode, selected_model)

            return {"response": response_text, "status": 200}
        except Exception as error:
            print(f"OpenAI API Error: {error}")
            return {
                "error": "Failed to generate response",
                "details": str(error),
                "status": 500,
            }
