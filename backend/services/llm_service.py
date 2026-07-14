import logging
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

load_dotenv()

logger = logging.getLogger(__name__)

CLAUDE_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")


def get_gemini():
    logger.info("Creating Gemini client (model=gemini-2.5-pro)")
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )


def get_claude(temperature: float = 0.7):
    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY is not set — Claude calls will fail")

    logger.info(
        "Creating Claude client (model=%s, requested_temperature=%s — "
        "ignored, this model does not accept a temperature parameter)",
        CLAUDE_MODEL,
        temperature,
    )
    return ChatAnthropic(
        model=CLAUDE_MODEL,
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    )