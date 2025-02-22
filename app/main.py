import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.core import init_db
from app.core import catch_exceptions_middleware

from app.auth import router as auth_router

# from app.routers import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=settings.OPENAPI_JSON_URL,
    docs_url=settings.DOCS_URL,
)

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(router, prefix="/api", tags=["api"])

# Enable exception handling middleware.py
if settings.ENVIRONMENT != settings.Environment.local.value:
    app.middleware("http")(catch_exceptions_middleware)

router = APIRouter()


@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
        print("DB initialized successfully!")
    except Exception as e:
        print(f"DB init error: {e}")


@app.get("/")
async def root():
    return {"message": "FastOllama API is running"}


if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt or CancelledError:
        print("Shutting down gracefully...")
