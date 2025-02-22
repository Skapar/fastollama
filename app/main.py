import uvicorn

from fastapi import FastAPI, APIRouter

app = FastAPI(title="FastOllama API")

router = APIRouter()

@app.get("/")
def root():
    return {"message": "FastOllama API is running"}

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")