from fastapi import FastAPI, Response
from fastapi_mcp import FastApiMCP


from backend.routes.members import router as members_router
from backend.routes.interests_total_value import router as interests_total_value_router

app = FastAPI()

app.include_router(members_router)
app.include_router(interests_total_value_router)

@app.get("/")
async def root():
    return Response(
        content="Welcome to the Members interest API.",
        media_type="text/plain",
    )

mcp = FastApiMCP(fastapi=app, include_operations=["search_members_with_grouped_interest_values", "search_members"])
mcp.mount()