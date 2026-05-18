import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

load_dotenv()


def get_gemini():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )


def get_claude(temperature: float = 0.7):
    return ChatAnthropic(
        model="claude-sonnet-4-20250514",
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=temperature
    )