import datetime
import random
import os
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    logger.error("API_KEY environment variable not set.")
    raise RuntimeError("API_KEY environment variable not set.")

# Create an APIRouter instance
app = FastAPI()
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
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

class ResponseData(BaseModel):
    id: int
    model: str
    created: int
    choices: List[Choice]
    usage: Optional[Usage] = None

class RequestData(BaseModel):
    model: str
    messages: List[Message]

# Gemini API client initialization
def get_gemini_client():
    try:
        genai.configure(api_key=API_KEY)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logger.error(f"Error configuring Gemini client: {e}")
        raise

# API endpoint using Gemini API
@chat.post("/gemini/chat/completions", response_model=ResponseData, summary="Send a chat message to Gemini.")
async def chat_completions_endpoint(request: RequestData):
    try:
        model = request.model
        messages = request.messages

        prompt = ''.join([f"{m.role}: {m.content}\n" for m in messages])
        logger.info(f"Sending prompt to Gemini: {prompt}")

        gemini_client = get_gemini_client()
        response = gemini_client.generate_content(prompt)

        response_text = response.text

        response_dict = ResponseData(
            id=random.randint(1, 999999999999999999999),
            model=model,
            created=int(datetime.datetime.now().timestamp()),
            choices=[
                Choice(
                    index=0,
                    message=Message(role="bot", content=response_text),
                    finish_reason="stop"
                )
            ],
            usage=Usage()
        )

        logger.info(f"Gemini response: {response_dict}")
        return response_dict

    except Exception as e:
        logger.error(f"Error during Gemini request: {e}")
        raise HTTPException(status_code=500, detail=f"Server Error: {e}")

app.include_router(chat)