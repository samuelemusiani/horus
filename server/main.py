import json
import subprocess

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

global scan, is_scanning
is_scanning = False
scan = [{"ip": "127.0.0.1", "mac": "00:00:00:00:00:00", "services": []}, {"ip": "192.168.0.3", "mac": "00:00:00:00:00:00", "services": []}]
# scan = []


@app.post("/start")
def start_scan():
    # start the scan
    global is_scanning
    if is_scanning:
        return {"status": "error", "message": "Already scanning"}
    is_scanning = True
    # call scanning
    return


@app.get("/scan")
def read_scan():
    global scan, is_scanning
    return {"status": is_scanning, "scan": json.dumps(scan)}


# get ssid of the connected wifi
@app.get("/ssid")
def get_ssid():
    try:
        result = subprocess.run(["sudo", "iwgetid", "-r"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            ssid = result.stdout.strip()
            return ssid if ssid else "Could not find SSID"
        else:
            return None
    except Exception as e:
        return None


@app.get("/isonline/{ip}")
def is_online(ip: str):
    try:
        result = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return {"status": "online"}
        else:
            return {"status": "offline"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
