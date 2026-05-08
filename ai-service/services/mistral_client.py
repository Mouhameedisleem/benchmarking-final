"""
Shared async Mistral API client.
Uses httpx.AsyncClient with a 120-second timeout to avoid blocking FastAPI's event loop.
"""
import json
import os
import httpx

MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"


async def call_mistral(messages: list, temperature: float = 0.5, model: str | None = None) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY not set")
    model = model or os.getenv("MISTRAL_MODEL", "mistral-large-latest")

    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            MISTRAL_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"model": model, "messages": messages, "temperature": temperature},
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


def extract_json(raw: str) -> dict:
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:]).strip()
        if raw.endswith("```"):
            raw = raw[:-3].strip()
        elif "```" in raw:
            raw = raw[: raw.rfind("```")].strip()
    return json.loads(raw)
