def main() -> None:
    import sys
    from pathlib import Path

    import uvicorn

    # The FastAPI app lives beside src/ and is not installed in the script package.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    uvicorn.run("app.main:app", host="127.0.0.1", port=3000)
