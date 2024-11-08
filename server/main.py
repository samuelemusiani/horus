from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/start")
def start_scan():
    # start the scan
    return {"message": "Scan started"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)