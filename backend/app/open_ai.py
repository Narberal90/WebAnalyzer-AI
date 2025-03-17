import json
import re

import httpx
from app.config import settings
from bs4 import BeautifulSoup
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


def is_valid_url(url: str) -> bool:
    url_pattern = re.compile(r"https?://\S+")
    return bool(url_pattern.match(url))


async def process_message_with_openai(content: str):
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": content}],
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
                                "You are an analyst. "
                                "Analyzes the content of a website "
                                "and provides a summary."
                            ),
                        },
                        {"role": "user", "content": website_content},
                    ],
                )

                return analysis_response.choices[0].message.content

            else:
                return "Invalid URL. Please check the link."

    return message.content or ""


async def parse_website(url: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        return soup.get_text(separator=" ", strip=True)[:1000]
    except Exception as e:
        return f"Error while parsing the site: {str(e)}"
