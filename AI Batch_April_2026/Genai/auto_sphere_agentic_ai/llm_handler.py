import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def get_groq_client():
    """
    Creates Groq client.
    Make sure GROQ_API_KEY is available in .env file.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Please add it in .env file.")
    return Groq(api_key=GROQ_API_KEY)


def ask_groq(system_prompt: str, user_prompt: str) -> str:
    """
    Common Groq LLM handler used by all agents.
    """

    client = get_groq_client()

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content