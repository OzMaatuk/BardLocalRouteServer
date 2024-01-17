import datetime
import random
import os
from dotenv import load_dotenv

from fastapi import FastAPI, APIRouter, Header, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Create an APIRouter instance
app = FastAPI()  # Create the application instance
chat = APIRouter()

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class Usage(BaseModel):
    # Add model properties as needed
    pass

class ResponseData(BaseModel):
    id: int
    model: str
    created: float
    choices: List[Choice]
    usage: Usage

class RequestData(BaseModel):
    model: str
    messages: List[Message]

# Bard API client initialization
def get_bard_client():
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel('gemini-pro')

# API endpoint using Bard API
@chat.post("/bard/chat/completions/", response_model=ResponseData, summary="Send a chat message to Bard and get an OpenAI-compatible API response.")
async def chat_completions_endpoint(request: RequestData):
    try:
        model = request.model
        messages = request.messages
        system_message = "system_message: "

        # Prepare prompt for Bard request
        prompt = f"{system_message}\n" + ''.join([f"{m.role}: {m.content}\n" for m in messages])

        # Send request to Bard API using Python client
        bard_client = get_bard_client()
        response = bard_client.generate_content(prompt)
        response_text = response.text


        # Create response using the model
        response_dict = ResponseData(
            id=random.randint(1, 999999999999999999999),
            model=model,
            created=datetime.datetime.now().timestamp(),
            choices=[
                Choice(
                    index=0,
                    message=Message(role="bot", content=response_text),
                    finish_reason="stop"
                )
            ],
            usage=Usage()
        )
        return response_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error: " + str(e))
    
app.include_router(chat)  # Mount the chat APIRouter to the main app