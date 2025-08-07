from backend.core import settings
from backend.core.db import setup_db

import logging

logging.basicConfig(
    level=settings.LOG_LEVEL.value,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # setup_db()
    import uvicorn

    uvicorn.run(
        "backend.api_server:app",
        host=settings.FASTAPI_HOST,
        port=settings.FASTAPI_PORT,
        reload=True,
    )
