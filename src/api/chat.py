from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import asyncio
from src.services.character_service import CharacterService
from src.models.test_case_config import TestCaseConfig
from src.models.llm_models_enum import LLMModels

router = APIRouter()


class ChatRequest(BaseModel):
    character_file: str
    enable_user_memory: bool = False
    user_name: str = ""
    user_interests: str = ""
    message: str
    prior_history: Optional[List[Dict[str, str]]] = None
    model: str = LLMModels.GPT_5_NANO.value


class ChatResponse(BaseModel):
    response: Optional[str] = None
    error: Optional[str] = None
    status: int


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        config = TestCaseConfig()
        config.character_file = request.character_file
        config.enable_user_memory = request.enable_user_memory
        config.user_name = request.user_name
        config.user_interests = request.user_interests
        config.messages = []

        service = CharacterService(config)

        if request.prior_history:
            service.conversation_history = request.prior_history

        result = service.generate_response(
            message=request.message,
            model=request.model,
            include_history=True,
            save_to_history=False,
            stream=False,
        )

        return ChatResponse(
            response=result.get("response"),
            error=result.get("error"),
            status=result.get("status", 500),
        )

    except Exception as e:
        return ChatResponse(
            response=None, error=f"Failed to process chat request: {str(e)}", status=500
        )


async def stream_chat_response(request: ChatRequest):
    try:
        config = TestCaseConfig()
        config.character_file = request.character_file
        config.enable_user_memory = request.enable_user_memory
        config.user_name = request.user_name
        config.user_interests = request.user_interests
        config.messages = []

        service = CharacterService(config)

        if request.prior_history:
            service.conversation_history = request.prior_history

        chunks = []

        def stream_handler(chunk: str):
            chunks.append(chunk)

        result = service.generate_response(
            message=request.message,
            model=request.model,
            include_history=True,
            save_to_history=False,
            stream=True,
            stream_handler=stream_handler,
        )

        if result.get("status") != 200:
            error_msg = result.get("error", "Unknown error")
            yield f"Error: {error_msg}"
            return

        for chunk in chunks:
            yield chunk
            await asyncio.sleep(0.01)

    except Exception as e:
        yield f"Error: Failed to process chat request: {str(e)}"


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(stream_chat_response(request), media_type="text/plain")
