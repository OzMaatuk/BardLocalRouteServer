import requests

url = "http://127.0.0.1:8000/gemini/"  # Replace with your server's URL

payload = {
    "model": "gemini-1.5-flash",
    "messages": [
        { "role": "user", "content": "Hello, can you explain about fastapi?" }
    ]
}

headers = {
    "Content-Type": "application/json"  # No need for Authorization header now
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print("Response received:")
    print(response.json())
else:
    print("Request failed with status code:", response.status_code)
    print("Error message:", response.text)