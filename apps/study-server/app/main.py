from fastapi import FastAPI

from app.api.v1 import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Wellcome to Study2Work"}
