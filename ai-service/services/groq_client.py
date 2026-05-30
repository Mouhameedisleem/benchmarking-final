"""
LLM client — Groq API (Llama 3.3 70B)
Groq's LPU inference is ~10x faster than standard inference APIs.
Exposes call_groq() and extract_json() used across all AI services.
"""
import asyncio
import json
import os
import httpx

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

_MAX_RETRIES = 3
_RETRY_DELAYS = [2, 5, 10]          # for transient errors (5xx, timeout)
_RETRYABLE_STATUS = {500, 502, 503, 504}

# Fallback model: much higher rate limits on Groq free tier (~6× more tokens/min)
_FALLBACK_MODEL = "llama-3.1-8b-instant"


async def call_groq(messages: list, temperature: float = 0.4, model: str | None = None) -> str:
    """Call Groq API with the same signature used across all services."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set — créez un compte sur https://console.groq.com et ajoutez la clé dans .env")

    model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    payload: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 3000,
    }

    # Activate native JSON mode when the prompt asks for JSON (faster + more reliable)
    asks_json = any(
        "json" in (m.get("content") or "").lower()
        for m in messages
        if isinstance(m, dict)
    )
    if asks_json:
        payload["response_format"] = {"type": "json_object"}

    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    GROQ_URL,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )

                # 413 — Payload too large: try fallback model with reduced max_tokens
                if response.status_code == 413:
                    if model != _FALLBACK_MODEL:
                        return await call_groq(messages, temperature, _FALLBACK_MODEL)
                    # Already on fallback — reduce max_tokens and retry once
                    if payload.get("max_tokens", 3000) > 1500:
                        payload["max_tokens"] = 1500
                        continue
                    err_body = response.text[:300]
                    raise RuntimeError(f"PAYLOAD_TOO_LARGE: Requête rejetée par Groq (413). Détail: {err_body}")

                # 429 — Rate limit: auto-switch to smaller fallback model first
                if response.status_code == 429:
                    if model != _FALLBACK_MODEL:
                        # Transparent fallback: retry immediately with lighter model
                        return await call_groq(messages, temperature, _FALLBACK_MODEL)
                    # Already on fallback model — wait retry-after then try once more
                    retry_after_raw = response.headers.get("retry-after", "")
                    wait = int(retry_after_raw) if retry_after_raw.isdigit() else 20
                    wait = min(wait, 60)
                    if attempt < _MAX_RETRIES - 1:
                        await asyncio.sleep(wait)
                        continue
                    raise RuntimeError(
                        f"RATE_LIMIT: Quota Groq dépassé sur les deux modèles. "
                        f"Attendez {wait} secondes et réessayez."
                    )

                if response.status_code in _RETRYABLE_STATUS:
                    last_exc = httpx.HTTPStatusError(
                        f"HTTP {response.status_code}",
                        request=response.request,
                        response=response,
                    )
                    if attempt < _MAX_RETRIES - 1:
                        await asyncio.sleep(_RETRY_DELAYS[attempt])
                    continue

                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]

        except RuntimeError:
            raise  # propagate rate-limit errors directly
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            last_exc = exc
            if attempt < _MAX_RETRIES - 1:
                await asyncio.sleep(_RETRY_DELAYS[attempt])

    raise RuntimeError(f"Groq API inaccessible après {_MAX_RETRIES} tentatives: {last_exc}")


def extract_json(raw: str) -> dict:
    """Parse LLM response to dict — handles markdown code fences and extra text."""
    raw = raw.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:]).strip()
        if raw.endswith("```"):
            raw = raw[:-3].strip()
        elif "```" in raw:
            raw = raw[: raw.rfind("```")].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(raw[start: end + 1])
        raise
