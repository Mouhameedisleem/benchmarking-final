"""
Production-ready multi-provider LLM client.
100% open-source models: phi4-mini (Ollama local), Llama 3.3 70B (Groq).

Role → Model → Provider Chain:
  QUESTIONNAIRE     → phi4-mini (Ollama local) → Groq(llama-3.3-70b) → Groq(llama-3.1-8b)
  SCORING           → phi4-mini (Ollama local) → Groq(llama-3.3-70b)
  RECOMMENDATIONS   → phi4-mini (Ollama local) → Groq(llama-3.3-70b)
  BENCHMARKING      → phi4-mini (Ollama local) → Groq(llama-3.3-70b)
  CONSULTANT_REVIEW → phi4-mini (Ollama local) → Groq(llama-3.3-70b)
"""
import asyncio
import hashlib
import json
import logging
import os
import re
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum

import httpx

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# TASK TYPES  (one per IA role)
# ═══════════════════════════════════════════════════════════════════════════════

class TaskType(str, Enum):
    QUESTIONNAIRE     = "questionnaire"      # JSON strict, qualité → phi4-mini (Ollama)
    SCORING           = "scoring"            # Raisonnement, nuance FR → DeepSeek V3
    RECOMMENDATIONS   = "recommendations"    # Raisonnement structuré + factualité → DeepSeek V3 / Llama 70B
    BENCHMARKING      = "benchmarking"       # Gros contexte, longue génération → Qwen 72B / Llama 70B
    CONSULTANT_REVIEW = "consultant_review"  # Suivi d'instruction, qualité → DeepSeek V3

    # Legacy aliases — kept for any callers that still pass task=FAST/STANDARD/HEAVY
    FAST     = "fast"
    STANDARD = "standard"
    HEAVY    = "heavy"


# ═══════════════════════════════════════════════════════════════════════════════
# PROVIDER CATALOG
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ProviderEndpoint:
    name: str
    url: str
    key_env: str
    model: str
    max_tokens: int
    timeout: float
    json_mode: bool = True          # supports response_format={"type":"json_object"}
    extra_headers: dict = field(default_factory=dict)

    @property
    def key(self) -> str:
        return os.getenv(self.key_env, "")

    @property
    def active(self) -> bool:
        """Provider is active if its API key is configured.
        Ollama is active only when OLLAMA_BASE_URL is explicitly set to a non-default value,
        OR when the user has set OLLAMA_ENABLED=true. This avoids wasting retry cycles
        when Ollama is not running locally."""
        if self.key_env == "OLLAMA_API_KEY":
            return os.getenv("OLLAMA_ENABLED", "false").lower() == "true"
        return bool(self.key)


# ── URL shortcuts ──────────────────────────────────────────────────────────────
_GROQ       = "https://api.groq.com/openai/v1/chat/completions"
_CEREBRAS   = "https://api.cerebras.ai/v1/chat/completions"
_OPENROUTER = "https://openrouter.ai/api/v1/chat/completions"
_NVIDIA     = "https://integrate.api.nvidia.com/v1/chat/completions"
_TOGETHER   = "https://api.together.xyz/v1/chat/completions"
_OLLAMA     = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/v1/chat/completions"

_OR_HDR = {
    "HTTP-Referer": "https://ia-benchmark.local",
    "X-Title": "IA Benchmark",
}


# ── Provider chains ────────────────────────────────────────────────────────────

PROVIDER_CHAINS: dict[TaskType, list[ProviderEndpoint]] = {

    # ─── 1. QUESTIONNAIRE — phi4-mini local (primary) → Groq 70B → Groq 8B fallback
    TaskType.QUESTIONNAIRE: [
        ProviderEndpoint("ollama:phi4-mini",           _OLLAMA,     "OLLAMA_API_KEY",     "phi4-mini",                                  4096, 180.0),
        ProviderEndpoint("groq:llama3.3-70b",          _GROQ,       "GROQ_API_KEY",       "llama-3.3-70b-versatile",                    4096, 90.0),
        ProviderEndpoint("groq:llama3.1-8b",           _GROQ,       "GROQ_API_KEY",       "llama-3.1-8b-instant",                       3072, 60.0),
    ],

    # ─── 2. SCORING — Ollama phi4-mini (local) → Groq 70B fallback ──────────
    # Goal: Raisonnement, nuance FR (analyse réponses + synthèse)
    TaskType.SCORING: [
        ProviderEndpoint("ollama:phi4-mini",           _OLLAMA,     "OLLAMA_API_KEY",     "phi4-mini",                                  3072, 180.0),
        ProviderEndpoint("groq:llama3.3-70b",          _GROQ,       "GROQ_API_KEY",       "llama-3.3-70b-versatile",                    4096, 90.0),
    ],

    # ─── 3. RECOMMENDATIONS — Ollama phi4-mini (local) → Groq 70B fallback ──
    # Goal: Raisonnement structuré + recommandations stratégiques
    TaskType.RECOMMENDATIONS: [
        ProviderEndpoint("ollama:phi4-mini",           _OLLAMA,     "OLLAMA_API_KEY",     "phi4-mini",                                  3072, 180.0),
        ProviderEndpoint("groq:llama3.3-70b",          _GROQ,       "GROQ_API_KEY",       "llama-3.3-70b-versatile",                    4096, 90.0),
    ],

    # ─── 4. BENCHMARKING — Ollama phi4-mini (local) → Groq 70B fallback ─────
    # Goal: Analyse sectorielle, longue génération
    TaskType.BENCHMARKING: [
        ProviderEndpoint("ollama:phi4-mini",           _OLLAMA,     "OLLAMA_API_KEY",     "phi4-mini",                                  4096, 240.0),
        ProviderEndpoint("groq:llama3.3-70b",          _GROQ,       "GROQ_API_KEY",       "llama-3.3-70b-versatile",                    4096, 90.0),
    ],

    # ─── 5. CONSULTANT_REVIEW — Ollama phi4-mini (local) → Groq 70B fallback
    # Goal: Suivi d'instruction, qualité (custom prompt du consultant)
    TaskType.CONSULTANT_REVIEW: [
        ProviderEndpoint("ollama:phi4-mini",           _OLLAMA,     "OLLAMA_API_KEY",     "phi4-mini",                                  3072, 180.0),
        ProviderEndpoint("groq:llama3.3-70b",          _GROQ,       "GROQ_API_KEY",       "llama-3.3-70b-versatile",                    4096, 90.0),
    ],
}

# Legacy task type aliases → map to the new role-based types
PROVIDER_CHAINS[TaskType.FAST]     = PROVIDER_CHAINS[TaskType.SCORING]
PROVIDER_CHAINS[TaskType.STANDARD] = PROVIDER_CHAINS[TaskType.RECOMMENDATIONS]
PROVIDER_CHAINS[TaskType.HEAVY]    = PROVIDER_CHAINS[TaskType.BENCHMARKING]


# ═══════════════════════════════════════════════════════════════════════════════
# CIRCUIT BREAKER
# Open after 3 failures in 5 min → skip provider 60 s → half-open probe
# ═══════════════════════════════════════════════════════════════════════════════

class _CircuitBreaker:
    _FAILURE_THRESHOLD = 3
    _WINDOW_S          = 300   # 5 min rolling window
    _OPEN_DURATION_S   = 60    # stay open 60 s before half-open

    def __init__(self):
        self._state: dict[str, dict] = {}
        self._lock = asyncio.Lock()

    async def is_open(self, name: str) -> bool:
        async with self._lock:
            s = self._state.get(name)
            if not s:
                return False
            if s.get("open_until", 0) > time.time():
                return True
            if s.get("open_until", 0) > 0:
                s["open_until"] = 0
            return False

    async def record_success(self, name: str) -> None:
        async with self._lock:
            self._state[name] = {"failures": 0, "window_start": time.time(), "open_until": 0}

    async def record_failure(self, name: str) -> None:
        async with self._lock:
            now = time.time()
            s = self._state.get(name, {"failures": 0, "window_start": now, "open_until": 0})
            if now - s["window_start"] > self._WINDOW_S:
                s = {"failures": 0, "window_start": now, "open_until": 0}
            s["failures"] += 1
            if s["failures"] >= self._FAILURE_THRESHOLD:
                s["open_until"] = now + self._OPEN_DURATION_S
                logger.warning(
                    "CircuitBreaker OPEN for '%s' — %d failures, retry after %ds",
                    name, s["failures"], self._OPEN_DURATION_S,
                )
            self._state[name] = s


_circuit = _CircuitBreaker()


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE CACHE  (LRU + TTL 15 min)
# Avoids duplicate LLM calls for identical prompts within the same session
# ═══════════════════════════════════════════════════════════════════════════════

class _LRUCache:
    def __init__(self, max_size: int = 256, ttl: float = 900.0):
        self._data: OrderedDict[str, tuple[str, float]] = OrderedDict()
        self._max  = max_size
        self._ttl  = ttl
        self._lock = asyncio.Lock()

    @staticmethod
    def _make_key(messages: list, temperature: float) -> str:
        raw = json.dumps(messages, sort_keys=True, ensure_ascii=False) + f"|{temperature:.2f}"
        return hashlib.sha256(raw.encode()).hexdigest()[:20]

    async def get(self, messages: list, temperature: float) -> str | None:
        k = self._make_key(messages, temperature)
        async with self._lock:
            entry = self._data.get(k)
            if entry is None:
                return None
            value, ts = entry
            if time.time() - ts > self._ttl:
                del self._data[k]
                return None
            self._data.move_to_end(k)
            return value

    async def put(self, messages: list, temperature: float, value: str) -> None:
        k = self._make_key(messages, temperature)
        async with self._lock:
            self._data[k] = (value, time.time())
            self._data.move_to_end(k)
            while len(self._data) > self._max:
                self._data.popitem(last=False)


_response_cache = _LRUCache(max_size=256, ttl=900.0)


# ═══════════════════════════════════════════════════════════════════════════════
# LOW-LEVEL SINGLE-PROVIDER CALL  (retry + 429 handling)
# ═══════════════════════════════════════════════════════════════════════════════

_MAX_RETRIES = 3


async def _call_one_provider(ep: ProviderEndpoint, messages: list, temperature: float) -> str:
    """Call one provider with retry, 429 backoff, and 413 token reduction."""
    asks_json = any(
        "json" in (m.get("content") or "").lower()
        for m in messages
        if isinstance(m, dict)
    )
    payload: dict = {
        "model":       ep.model,
        "messages":    messages,
        "temperature": temperature,
        "max_tokens":  ep.max_tokens,
    }
    if asks_json and ep.json_mode:
        payload["response_format"] = {"type": "json_object"}

    headers = {
        "Authorization": f"Bearer {ep.key}",
        "Content-Type":  "application/json",
        **ep.extra_headers,
    }

    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        backoff = 2.0 ** attempt          # 1s, 2s, 4s

        try:
            async with httpx.AsyncClient(timeout=ep.timeout) as client:
                resp = await client.post(ep.url, headers=headers, json=payload)

            # ── Rate limit — only 1 retry then fail fast (don't block the chain) ──
            if resp.status_code == 429:
                if attempt == 0:
                    raw_ra = resp.headers.get("retry-after", "")
                    wait   = int(raw_ra) if raw_ra.isdigit() else 15
                    wait   = min(wait, 30)   # never wait more than 30s per provider
                    logger.warning("[%s] 429 — waiting %ds then trying next provider",
                                   ep.name, wait)
                    await asyncio.sleep(wait)
                    continue
                raise RuntimeError(f"RATE_LIMIT@{ep.name}: still rate-limited after 1 retry")

            # ── Payload too large → halve max_tokens (floor 2048 to keep JSON quality) ──
            if resp.status_code == 413:
                current = payload.get("max_tokens", 4096)
                reduced = max(current // 2, 2048)
                if reduced < current:
                    payload["max_tokens"] = reduced
                    continue
                raise RuntimeError(f"PAYLOAD_TOO_LARGE@{ep.name}")

            # ── Transient server errors ───────────────────────────────────────
            if resp.status_code in {500, 502, 503, 504}:
                last_exc = RuntimeError(f"HTTP {resp.status_code}@{ep.name}")
                if attempt < _MAX_RETRIES - 1:
                    await asyncio.sleep(backoff)
                continue

            if not resp.is_success:
                raise RuntimeError(
                    f"HTTP {resp.status_code}@{ep.name}: {resp.text[:300]}"
                )

            content = resp.json()["choices"][0]["message"]["content"]
            logger.debug("[%s] OK — %d tokens out (attempt=%d)", ep.name, len(content.split()), attempt + 1)
            return content

        except RuntimeError:
            raise
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            last_exc = exc
            logger.warning("[%s] network error (attempt %d): %s", ep.name, attempt + 1, exc)
            if attempt < _MAX_RETRIES - 1:
                await asyncio.sleep(backoff)

    raise RuntimeError(f"{ep.name} failed after {_MAX_RETRIES} attempts: {last_exc}")


# ═══════════════════════════════════════════════════════════════════════════════
# PROVIDER CHAIN RUNNER  (circuit breaker + skip unconfigured)
# ═══════════════════════════════════════════════════════════════════════════════

async def _run_chain(chain: list[ProviderEndpoint], messages: list, temperature: float) -> str:
    errors: list[str] = []

    for ep in chain:
        if not ep.active:
            continue
        if await _circuit.is_open(ep.name):
            logger.debug("Circuit open → skipping %s", ep.name)
            continue

        try:
            result = await _call_one_provider(ep, messages, temperature)
            await _circuit.record_success(ep.name)
            logger.info("✓ LLM via %-30s model=%s", ep.name, ep.model)
            return result
        except Exception as exc:
            await _circuit.record_failure(ep.name)
            errors.append(f"{ep.name}: {exc}")
            logger.warning("✗ %s failed — trying next provider (%s)", ep.name, exc)

    raise RuntimeError(
        "All providers exhausted — check API keys and provider status.\n"
        + "\n".join(f"  • {e}" for e in errors)
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════════

async def call_llm(
    messages: list,
    temperature: float = 0.4,
    model: str | None = None,     # legacy param — ignored; routing done via task=
    task: TaskType = TaskType.RECOMMENDATIONS,
    use_cache: bool = True,
) -> str:
    """
    Call the best available open-source LLM for the given IA role.

    Routing:
        QUESTIONNAIRE     → Ollama(phi4-mini) → Groq(llama-3.3-70b) → Groq(llama-3.1-8b)
        SCORING           → Ollama(phi4-mini) → Groq(llama-3.3-70b)
        RECOMMENDATIONS   → Ollama(phi4-mini) → Groq(llama-3.3-70b)
        BENCHMARKING      → Ollama(phi4-mini) → Groq(llama-3.3-70b)
        CONSULTANT_REVIEW → Ollama(phi4-mini) → Groq(llama-3.3-70b)

    Args:
        messages:    OpenAI-format message list [{role, content}, …]
        temperature: Sampling temperature (0.0 – 1.0)
        model:       Ignored (kept for backward compat — pass task= instead)
        task:        IA role → selects provider chain and model
        use_cache:   Enable LRU response cache (default True)

    Returns:
        Raw text content from the LLM.
    """
    if use_cache:
        cached = await _response_cache.get(messages, temperature)
        if cached is not None:
            logger.debug("Cache HIT (task=%s)", task.value)
            return cached

    chain  = PROVIDER_CHAINS.get(task, PROVIDER_CHAINS[TaskType.RECOMMENDATIONS])
    result = await _run_chain(chain, messages, temperature)

    if use_cache:
        await _response_cache.put(messages, temperature, result)

    return result


# Backward-compatibility alias — all existing callers (call_groq) work unchanged
call_groq = call_llm


# ═══════════════════════════════════════════════════════════════════════════════
# JSON EXTRACTION  (handles markdown fences, trailing commas, embedded JSON)
# ═══════════════════════════════════════════════════════════════════════════════

def extract_json(raw: str) -> dict:
    """
    Parse JSON from an LLM response that may be wrapped in markdown code fences
    or surrounded by explanatory text.

    Handles:
      • Raw JSON object
      • ```json … ``` fences
      • JSON embedded mid-text
      • Trailing commas before } or ]  (common LLM output artifact)
    """
    raw = raw.strip()

    # ── Strip markdown fences ─────────────────────────────────────────────────
    if "```" in raw:
        parts = raw.split("```")
        for part in parts[1::2]:                     # content inside fences
            candidate = part.lstrip("json").lstrip("JSON").strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                pass

    # ── Direct parse ──────────────────────────────────────────────────────────
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # ── Extract first {...} block with trailing-comma fix ─────────────────────
    start = raw.find("{")
    end   = raw.rfind("}")
    if start != -1 and end > start:
        candidate = raw[start:end + 1]
        candidate = re.sub(r",\s*([\]}])", r"\1", candidate)   # remove trailing commas
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"No valid JSON found in LLM response.\n"
        f"First 300 chars: {raw[:300]}"
    )
