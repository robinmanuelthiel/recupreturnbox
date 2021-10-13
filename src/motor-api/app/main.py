import logging

# API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from config import DefaultConfig
from router import health_router, motor_router

log = logging.getLogger(__name__)


config = DefaultConfig()

tags_metadata = [
    {
        "name": "Health",
        "description": "This API endpoint describes the status of the service.",
    }
]

app = FastAPI(
    openapi_tags=tags_metadata,
    # https://fastapi.tiangolo.com/tutorial/metadata/#openapi-url
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.RELEASE,
    root_path=config.ROOT_PATH)


@app.get("/openapi.json")
async def get_open_api_endpoint():
    response = JSONResponse(
        get_openapi(
            title="FastAPI security test",
            version=1,
            routes=app.routes)
    )
    return response

app.include_router(
    health_router.router,
    prefix="/health",
    tags=["Health"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    motor_router.router,
    prefix="/motor",
    tags=["Motor"],
    responses={404: {"description": "Not found"}},
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)