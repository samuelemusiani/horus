import json
import subprocess

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_ollama import ChatOllama
from typing import List, Tuple

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

global scan, is_scanning
is_scanning = False
with open("out.json", 'r') as file:
    data = json.load(file)
scan = data['scan']
# scan = []


@app.post("/start")
def start_scan():
    # start the scan
    global is_scanning, scan
    if is_scanning:
        return {"status": "error", "message": "Already scanning"}
    is_scanning = True
    # Start the scan
    fast_network_scan('172.23.0.0/25')

    # Get the list of hosts
    tmp = get_hosts()
    scan = tmp

    # Run vulnerability scan on each host
    for host in tmp:
        run_vuln_scan(host['ip'])
        scan = get_hosts()

    is_scanning = False
    return {"message": "End"}


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
            return "Ethernet"
    except Exception:
        return "Ethernet"

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
    
@app.post("/chat")
def chat(messages: List[Tuple[str, str]]):
    llm = ChatOllama(model="llama3.2", temperature=0)

    messages = [(
        "system",
        "You are a helpful assistant that provides explanations of network vulnerabilities to a non-technical user. Only answer questions.",
    )] + messages

    if messages[len(messages) - 1][0] == "user" and not messages[len(messages) - 1][1].endswith(" Short answer."):
        messages[len(messages) - 1] = ("user", messages[len(messages) - 1][1] + ". Short answer.")

    print(messages)

    ai_msg = llm.invoke(messages)
    return ai_msg.content

@app.get("/summary")
def report_summary():

    # Generation takes too lonh for demo, we will return a pre-generated summary

    return '''

**Overview**

The data includes information about 6 devices (172.23.0.1 to 172.23.0.6) with unknown names and MAC addresses. The scan was conducted on November 9, 2024.

**Vulnerable Devices**

* 2 devices (172.23.0.2 and 172.23.0.6) have open SSH ports (port 22), but only one of them is vulnerable to a known exploit.
* 1 device (172.23.0.5) has an open HTTP port (port 80) with multiple potential vulnerabilities, including stored XSS, SQL injection, and more.

**Non-Vulnerable Devices**

* 3 devices (172.23.0.1, 172.23.0.3, and 172.23.0.4) have no open ports or services that are vulnerable to known exploits.
* 1 device (172.23.0.6) has an open HTTP port (port 80), but none of the potential vulnerabilities are currently exploitable.

**Key Takeaways**

* SSH is a common and potentially vulnerable service, especially if not properly configured.
* Multiple HTTP vulnerabilities were detected on one device, highlighting the importance of keeping web servers up-to-date with the latest security patches.
* Regular network scans can help identify potential vulnerabilities before they become major issues.

'''

    llm = ChatOllama(model="llama3.2", temperature=0)

    #print(scan)

    scan_copy = []
    for device in scan:
        device_copy = device.copy()
        for service in device_copy.get('services', []):
            if 'output' in service:
                print(device['name'], service['name'])
                service['output'] = ""
        scan_copy.append(device_copy)

    messages = [
        (
            "system",
            "You are a helpful summarizer of network vulnerability data for non technical people.",
        ),
        (
            "user", 
            "Make a short summary of this device vulnerability data: " + str(scan_copy)
        ),
    ]

    print(messages)

    ai_msg = llm.invoke(messages)

    print(ai_msg.content)

    return ai_msg.content

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
