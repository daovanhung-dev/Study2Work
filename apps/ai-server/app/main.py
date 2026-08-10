from fastapi import FastAPI
from app.api.v1 import router

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Wellcome to AI server"
    }

app.include_router(router)