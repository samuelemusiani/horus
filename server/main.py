from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess
from langchain_ollama import ChatOllama
from typing import List, Tuple


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
    # start the scan
    return {"message": "Scan started"}
  

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)