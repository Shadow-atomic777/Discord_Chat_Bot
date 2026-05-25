import discord
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True



client = discord.Client(intents=intents)

# load character personality
with open("charactor.txt", "r", encoding="utf-8") as f:
    CHARACTER_PROMPT = f.read()

MEMORY_FILE = "memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

memory = load_memory()


def get_ai_response(user_id, message):

    history = memory.get(user_id, [])

    history.append({
        "role": "user",
        "content": message
    })

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": CHARACTER_PROMPT
            },
            *history[-10:]
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    reply = response.json()["choices"][0]["message"]["content"]

    history.append({
        "role": "assistant",
        "content": reply
    })

    memory[user_id] = history
    save_memory(memory)

    return reply


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    user_id = str(message.author.id)

    reply = get_ai_response(user_id, message.content)

    await message.channel.send(reply)


client.run(DISCORD_TOKEN)
