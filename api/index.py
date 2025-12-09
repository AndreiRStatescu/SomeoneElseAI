import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from api.api import app
    from mangum import Mangum

    handler = Mangum(app, lifespan="off")
except Exception as e:
    print(f"Import error: {e}")
    import traceback

    traceback.print_exc()

    from fastapi import FastAPI
    from mangum import Mangum

    fallback_app = FastAPI()

    @fallback_app.get("/healthz")
    async def healthz():
        return {"status": "ok", "error": str(e)}

    handler = Mangum(fallback_app, lifespan="off")
