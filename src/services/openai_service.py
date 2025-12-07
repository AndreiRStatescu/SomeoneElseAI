import logging
import os
from typing import Callable, List, Dict
from openai import OpenAI
from dotenv import load_dotenv
from ..llm_models_enum import LLMModels

load_dotenv(".env.local")
logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self, api_key: str = None):
        self._client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self._default_model = LLMModels.GPT_5_1

    def _format_messages_for_gpt5(self, messages: List[Dict[str, str]]) -> str:
        input_text = ""
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "system":
                input_text += f"{content}\n\n"
            elif role == "user":
                input_text += f"User: {content}\n"
            elif role == "assistant":
                input_text += f"Assistant: {content}\n"
        return input_text.strip()

    def _stream_gpt5_response(
        self,
        input_text: str,
        model: str,
        stream_handler: Callable[[str], None] = None,
        max_output_tokens: int = 2000,
    ) -> dict:
        reasoning_effort = "none" if model == "gpt-5.1" else "minimal"
        try:
            with self._client.responses.stream(
                model=model,
                input=input_text,
                reasoning={"effort": reasoning_effort},
                text={"verbosity": "medium"},
                max_output_tokens=max_output_tokens,
            ) as stream:
                collected_chunks: List[str] = []

                for event in stream:
                    if event.type == "response.output_text.delta":
                        delta = getattr(event, "delta", None)
                        if not delta:
                            continue
                        collected_chunks.append(delta)
                        if stream_handler:
                            stream_handler(delta)

                final_response = stream.get_final_response()
                response_text = final_response.output_text or "".join(collected_chunks)

                if not response_text:
                    return {"error": "Empty response from API", "status": 500}

                return {"response": response_text, "status": 200}
        except Exception as error:
            logger.error(f"OpenAI Streaming Error: {error}")
            return {
                "error": "Failed to stream response",
                "details": str(error),
                "status": 500,
            }

    def _call_gpt5_model(self, message: str, model: str) -> str:
        reasoning_effort = "none" if model == "gpt-5.1" else "minimal"
        response = self._client.responses.create(
            model=model,
            input=f"You are a helpful assistant that answers questions concisely and accurately.\n\nUser: {message}",
            reasoning={"effort": reasoning_effort},
            text={"verbosity": "medium"},
            max_output_tokens=1000,
        )
        return response.output_text or "No response generated"

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
        self,
        message: str,
        model: str = None,
        messages: list = None,
        stream: bool = False,
        stream_handler: Callable[[str], None] = None,
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
                    input_text = self._format_messages_for_gpt5(messages)
                    if stream:
                        return self._stream_gpt5_response(
                            input_text=input_text,
                            model=selected_model,
                            stream_handler=stream_handler,
                            max_output_tokens=2000,
                        )

                    reasoning_effort = (
                        "none"
                        if selected_model == LLMModels.GPT_5_1.value
                        else "minimal"
                    )
                    response = self._client.responses.create(
                        model=selected_model,
                        input=input_text,
                        reasoning={"effort": reasoning_effort},
                        text={"verbosity": "medium"},
                        max_output_tokens=2000,
                    )

                    response_text = response.output_text
                    if not response_text:
                        return {"error": "Empty response from API", "status": 500}

                    return {"response": response_text, "status": 200}
                else:
                    if stream:
                        return {
                            "error": "Streaming is only supported for gpt-5 models",
                            "status": 400,
                        }

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

                return {"response": response_text, "status": 200}
            else:
                if LLMModels.is_gpt5_model(selected_model):
                    if stream:
                        input_text = f"You are a helpful assistant that answers questions concisely and accurately.\n\nUser: {message}"
                        return self._stream_gpt5_response(
                            input_text=input_text,
                            model=selected_model,
                            stream_handler=stream_handler,
                            max_output_tokens=1000,
                        )

                    response_text = self._call_gpt5_model(message, selected_model)
                else:
                    response_text = self._call_gpt4_model(message, selected_model)

                return {"response": response_text, "status": 200}
        except Exception as error:
            logger.error(f"OpenAI API Error: {error}")
            return {
                "error": "Failed to generate response",
                "details": str(error),
                "status": 500,
            }
