# Bard Local Route Server

This project demonstrates interacting with the Bard API to create a simple chat completions server using FastAPI.

## Project Structure

- `app.py`: Contains the FastAPI server code.
- `test.py`: Provides a script for testing the server's functionality.
- `README.md` (this file): Provides project documentation.
- `requirements.txt`: Lists required Python dependencies (e.g., `fastapi`, `google-generativeai`, `pydantic`, `python-dotenv`).
- `.env`: Stores sensitive information like your Bard API key (not included in version control).

## Running the Server

1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file in the project directory and set the `API_KEY` variable to your Bard API key.
3. Run the server: `uvicorn app:app --reload`

## Testing the Server

1. Execute the test script: `python test.py`
2. Observe the output for successful interaction with the server.

## API Endpoint

The server exposes a single endpoint:

- **POST /bard/chat/completions/**
   - Accepts a JSON payload with the following structure:
     ```json
     {
         "model": "gemini-pro",
         "messages": [
             { "role": "user", "content": "initial message" }
         ]
     }
     ```
   - Returns a response in the following format:
     ```json
     {
         "id": 123456789,
         "model": "gemini-pro",
         "created": 1668555200.0,
         "choices": [
             {
                 "index": 0,
                 "message": { "role": "bot", "content": "response from Bard" },
                 "finish_reason": "stop"
             }
         ],
         "usage": {}
     }
     ```

## Additional Notes

- Ensure you have a valid Bard API key to use the server.
- Refer to the FastAPI and Bard API documentation for more advanced usage and customization.
