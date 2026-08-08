from fastapi import FastAPI, HTTPException

from app.api.v1 import router
from app.core.exceptions import http_exception_handler
from app.core.middleware import TraceIdMiddleware

app = FastAPI()

app.add_middleware(TraceIdMiddleware)
app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(router)


@app.get("/")
def root():
    return {"message": "Welcome to Study2Work"}
