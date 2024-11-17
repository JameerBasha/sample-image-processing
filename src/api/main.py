from fastapi import FastAPI

from src.api.routers import image_router

app = FastAPI()


@app.get("/health/")
def health():
    return {"message": "OK"}


app.include_router(image_router.router, prefix="/image", tags=["images"])
