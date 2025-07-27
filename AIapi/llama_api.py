from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

OLLAMA_API_URL = "http://localhost:11434/api/generate"

class EmailRequest(BaseModel):
    content: str
    model: str = "llama3.2"

@app.post("/summarize")
async def summarize_email(req: EmailRequest):
    prompt = f"your name is wonder a personal assistant, your job is to read my mail and give a concise summary so that your owner refered to in these emails  by names daliso or techdc or tech,doesnt have to read everything or miss anything get. just Summarize the following email content dont say anything else:\n\n{req.content}\n\nSummary:"
    payload = {
        "model": req.model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    return response.json()
