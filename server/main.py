from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess
from lib import fast_network_scan, run_vuln_scan, get_hosts

scanning = False
fast_scanned = False

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/start")
def start_scan():
    if scanning:
        return get_hosts()

    scanning = True

    # Start the scan
    fast_network_scan('192.168.1.0/24')

    # Get the list of hosts
    discovered_hosts = get_hosts()

    # Run vulnerability scan on each host
    for host in discovered_hosts:
        run_vuln_scan(host['ip'])

    return {"message": "End"}

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
