from fastapi import FastAPI, Response
from fastapi_mcp import FastApiMCP
from pathlib import Path
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.db import setup_db

from app.routes.members import router as members_router
from app.routes.interests_total_value import router as interests_total_value_router

import logging

logging.basicConfig(
    level=settings.LOG_LEVEL.value,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


# Startup hook for DB setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    db_path = Path(settings.SQLITE_DB_PATH)
    if not db_path.exists():
        logging.info(f"Database not found at {db_path}, initializing...")
        setup_db()
    else:
        logging.info(f"Database already exists at {db_path}, skipping setup.")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(members_router)
app.include_router(interests_total_value_router)


@app.get("/")
async def root():
    return Response(
        content="Welcome to the Members interest API.",
        media_type="text/plain",
    )

mcp = FastApiMCP(
    fastapi=app,
    include_operations=[
        "search_members_with_grouped_interest_values",
        "search_members",
        "search_member_interests",
    ],
)
mcp.mount_http()
