#!/usr/bin/env python3
"""kernels/generation.py — the Hermes generation engine (GENERATION side).

Hermes GENERATES the layer content (deepseek-v4-flash via opencode-go); the deterministic gates REDUCE.
This kernel is the model engine — it reads real committed inputs and derives the layer's content.
It is REPLACEABLE (Hermes is the execution kernel; the state is the registries).
"""
from __future__ import annotations
import json, os, time
import urllib.request

# red-team LOW-12: pin the endpoint. The env override is removed so a compromised env can't redirect
# the bearer key to an attacker's host.
BASE = "https://opencode.ai/zen/go/v1"
MODEL = os.environ.get("PATALA_MODEL", "deepseek-v4-flash")
ALLOWED_BASE = "https://opencode.ai/zen/go/v1"


def _key() -> str:
    k = os.environ.get("OPENCODE_API_KEY")
    if k:
        return k
    auth = os.path.expanduser("~/.local/share/opencode/auth.json")
    try:
        data = json.load(open(auth))
        for prov in ("opencode-go", "opencode"):
            info = data.get(prov)
            if info and info.get("type") == "api":
                return info["key"]
    except Exception:
        pass
    raise RuntimeError("OpenCode Go API key not found")


def generate(system: str, user: str, *, max_tokens: int = 1200, timeout: int = 120,
             retries: int = 4, temperature: float = 0.4) -> str:
    payload = {"model": MODEL,
               "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
               "max_tokens": max_tokens, "temperature": temperature}
    req = urllib.request.Request(f"{BASE}/chat/completions", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + _key(),
                                          "User-Agent": "opencode/1.0"}, method="POST")
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode())
            content = data["choices"][0]["message"]["content"] or ""
            if content.strip():
                return content
            last = "empty content"
        except Exception as e:
            last = e
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"generation failed after {retries} retries: {last}")


def generate_json(system: str, user: str, **kw) -> dict:
    out = generate(system, user, **kw)
    stripped = out.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        nxt = stripped.find("\n")
        if nxt != -1:
            stripped = stripped[nxt + 1:].strip()
    end = stripped.rfind("}")
    if end == -1:
        return {"_raw": out}
    depth, start = 0, stripped.rfind("{")
    for i in range(end, -1, -1):
        ch = stripped[i]
        if ch == "}":
            depth += 1
        elif ch == "{":
            depth -= 1
        if depth == 0:
            start = i
            break
    try:
        parsed = json.loads(stripped[start:end + 1], strict=False)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    return {"_raw": out}


def available() -> bool:
    try:
        return "GATEWAY OK" in generate(
            "You are terse. Reply with exactly the two words: GATEWAY OK", "Confirm.",
            max_tokens=200, timeout=90, retries=1)
    except Exception:
        return False


if __name__ == "__main__":
    print("available:", available())
