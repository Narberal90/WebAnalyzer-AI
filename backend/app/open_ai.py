import json
import re
from typing import Tuple

import httpx
from app.config import settings
from bs4 import BeautifulSoup
from openai import AsyncOpenAI
from tiktoken import encoding_for_model


client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
MAX_TOKENS = 2000

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
)


def count_tokens(text: str) -> int:
    enc = encoding_for_model("gpt-4")
    return len(enc.encode(text))


def limit_text_by_tokens(text: str, max_tokens: int) -> Tuple[str, int]:
    enc = encoding_for_model("gpt-4")
    tokens = enc.encode(text)
    if len(tokens) <= max_tokens:
        return text, len(tokens)

    limited_tokens = tokens[:max_tokens]
    return enc.decode(limited_tokens), len(limited_tokens)


def is_valid_url(url: str) -> bool:
    url_pattern = re.compile(r"https?://\S+")
    return bool(url_pattern.match(url))


async def process_message_with_openai(content: str):
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. Always respond in the "
                    "same language as the user's message. If the user writes "
                    "in Ukrainian, respond in Ukrainian. If the user writes "
                    "in English, respond in English, and so on."
                ),
            },
            {"role": "user", "content": content},
        ],
        functions=[
            {
                "name": "parse_website",
                "description": "Extracts text content from a URL.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": (
                                "The URL to extract text content from."
                            ),
                        }
                    },
                    "required": ["url"],
                },
            }
        ],
        function_call="auto",
    )

    message = response.choices[0].message

    if hasattr(message, "function_call") and message.function_call:
        function_call = message.function_call
        if function_call.name == "parse_website":
            url = json.loads(function_call.arguments)["url"]

            if is_valid_url(url):
                website_content = await parse_website(url)

                analysis_response = await client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an analyst. Analyze the content of a "
                                "website and provide a summary. Use the same "
                                "language as the user's message."
                            ),
                        },
                        {
                            "role": "user",
                            "content": (
                                f"User request: {content}\n\n"
                                "Website content to analyze:"
                            ),
                        },
                        {"role": "assistant", "content": website_content},
                    ],
                )

                return analysis_response.choices[0].message.content

            else:
                return "Invalid URL. Please check the link."

    return message.content or ""


async def parse_website(url: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"User-Agent": USER_AGENT},
            )
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        text = soup.get_text(separator=" ", strip=True)
        limited_text, token_count = limit_text_by_tokens(text, MAX_TOKENS)
        print(f"Website content tokens: {token_count}")
        return limited_text
    except Exception as e:
        return f"Error while parsing the site: {str(e)}"
