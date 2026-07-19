from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from app.api.v1 import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Wellcome to Study2Work"}
