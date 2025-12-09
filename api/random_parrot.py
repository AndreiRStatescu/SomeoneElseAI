from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import random
import asyncio

router = APIRouter()

WORD_LIST = [
    "apple",
    "banana",
    "cherry",
    "dragon",
    "elephant",
    "falcon",
    "guitar",
    "harmony",
    "island",
    "jungle",
    "kitten",
    "laptop",
    "mountain",
    "notebook",
    "ocean",
    "penguin",
    "quantum",
    "rainbow",
    "sunset",
    "thunder",
    "umbrella",
    "volcano",
    "whisper",
    "xylophone",
    "yellow",
    "zebra",
    "acoustic",
    "butterfly",
    "crystal",
    "dolphin",
    "emerald",
    "firefly",
    "galaxy",
    "horizon",
    "infinite",
    "jasmine",
    "kaleidoscope",
    "lighthouse",
    "melody",
    "nebula",
    "orchestra",
    "paradise",
    "quasar",
    "radiance",
    "symphony",
    "tranquil",
    "universe",
    "velvet",
    "wonder",
    "xenon",
    "yearning",
    "zephyr",
]


async def generate_random_words(num_words: int):
    words = random.choices(WORD_LIST, k=num_words)
    text = " ".join(words)

    for char in text:
        yield char
        await asyncio.sleep(0.05)


@router.get("/random_parrot")
async def random_parrot(num_words: int):
    return StreamingResponse(generate_random_words(num_words), media_type="text/plain")
