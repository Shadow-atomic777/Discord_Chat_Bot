import requests
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {
            "role": "user",
            "content": "Explain what is AI in simple words"
        }
    ]
}

response = requests.post(url, headers=headers, json=payload)

print(response.json())