from fastapi import FastAPI, Response

from backend.routes.members import router as members_router

app = FastAPI()

app.include_router(members_router)

@app.get("/")
async def root():
    return Response(
        content="Welcome to the Members interest API.",
        media_type="text/plain",
    )

