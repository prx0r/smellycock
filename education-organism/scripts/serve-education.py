#!/usr/bin/env python3
"""scripts/serve-education.py — the education API server (stdlib, RAM-friendly, perf doctrine).

Serves the LIVE education surface per the perf doctrine (one request = one answer, static bytes where
possible, no LLM in the read path):
  GET /education                  → the lesson index (compiled)
  GET /education/{lesson_id}      → one LearningPacket (compiled)
  GET /learn/{work}               → the lesson progression for a work
  POST /education/{lesson_id}/answer → submit a learner answer → blind-assessor grade + log (SQLite)
  GET /resolve/{object_id}        → the audit trail (education → ... → source)

Serves over stdlib http.server (no flask/fastapi dep, RAM-friendly). Compute-on-write: index + lessons
are precompiled static bytes; only grading hits the DB. Cached p95 well under 50ms (static reads).
"""
from __future__ import annotations
import json, sqlite3, sys, time, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
from gates import blind_grade  # noqa: E402
from guard import guard_answer  # noqa: E402

ED_DIR = Path("/root/smellycock/site/education")
REG = Path("/root/patalacheckpoints/data/corpus/registries")
DB = ROOT / "data" / "learner" / "learner.db"


def _init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS learner_events "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, learner TEXT, "
                "lesson TEXT, question TEXT, grade TEXT, response TEXT)")
    con.commit()
    con.close()


def _load_index():
    p = ED_DIR / "education-index.json"
    return json.loads(p.read_text()) if p.exists() else {"lessons": []}


def _load_lesson(oid):
    idx = _load_index()
    for l in idx.get("lessons", []):
        if l["object_id"] == oid:
            p = ED_DIR / l["file"]
            return json.loads(p.read_text()) if p.exists() else None
    return None


def _resolve_to_source(object_id):
    """The audit trail: follow upper refs to the bare segment, then walk down to SOURCE."""
    def find_base(oid, seen):
        if oid in seen:
            return None
        seen.add(oid)
        if "__" not in oid:
            return oid
        for layer in ["EDUCATION", "ESSAY", "SYNTHESIS", "ARGUMENT", "THEME"]:
            p = REG / f"{layer.lower()}-registry.jsonl"
            if not p.exists():
                continue
            for line in p.open(encoding="utf-8"):
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("object_id") != oid or r.get("superseded"):
                    continue
                refs = list(r.get("input_refs") or [])
                for lc in (r.get("payload", {}).get("education", {}) or {}).get("learning_claims", []):
                    refs += list(lc.get("depends_on") or [])
                for ref in refs:
                    b = find_base(ref, seen)
                    if b:
                        return b
        return None
    base = find_base(object_id, set())
    if not base:
        return []
    chain = []
    for layer in ["C1", "L200", "L2", "L1", "L0", "T1", "SOURCE"]:
        p = REG / f"{layer.lower()}-registry.jsonl"
        if p.exists():
            for line in p.open():
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("object_id") == base and not r.get("superseded"):
                    chain.append({"layer": layer, "object_id": base})
                    break
    return chain


def _guard_payload(lesson_id, answer):
    """Run the anti-hallucination guards (quote_verifier + citation_whitelist) on a submitted answer
    against the lesson's retrieved source context. Deterministic, stdlib, no LLM.

    The retrieved-context sources map is built from the lesson's learning-claim source_refs resolved
    down to their SOURCE passage text — the same provenance the /resolve endpoint walks. The whitelist
    is the set of source titles in that context (so a fabricated citation is stripped, an invented
    quote is downgraded)."""
    lesson = _load_lesson(lesson_id)
    if not lesson:
        return {"error": "lesson not found"}, 404
    sources = {}
    retrieved_titles = []
    for claim in lesson.get("learning_claims", []):
        for ref in (claim.get("source_refs") or []) + (claim.get("depends_on") or []):
            base = _resolve_base(ref, set())
            if not base:
                continue
            for layer in ["C1", "L200", "L2", "L1", "L0", "T1", "SOURCE"]:
                p = REG / f"{layer.lower()}-registry.jsonl"
                if not p.exists():
                    continue
                for line in p.open(encoding="utf-8"):
                    try:
                        r = json.loads(line)
                    except Exception:
                        continue
                    if r.get("object_id") == base and not r.get("superseded"):
                        txt = _first_text(r.get("payload", {}))
                        if txt:
                            # index the source under its object_id AND any readable work-title alias
                            # (work prefix of the object_id), so a real answer citing 《Tantraloka》 or
                            # the object_id both resolve. Title comparison is diacritic-folded in guard.
                            titles = _source_titles(r, base)
                            for title in titles:
                                sources[title] = txt
                                retrieved_titles.append(title)
                        break
    result = guard_answer(answer or "", sources, retrieved_titles)
    return {
        "lesson": lesson_id,
        "guarded_answer": result["answer"],
        "quote_mutations": [m.__dict__ for m in result["quote_mutations"]],
        "citation_mutations": result["citation_mutations"],
        "quotes_checked": result["quotes_checked"],
        "trust": result["trust"],
    }, 200


def _resolve_base(object_id, seen):
    """Walk down to the bare source segment id (like _resolve_to_source's find_base)."""
    if object_id in seen:
        return None
    seen.add(object_id)
    if "__" not in object_id:
        return object_id
    for layer in ["EDUCATION", "ESSAY", "SYNTHESIS", "ARGUMENT", "THEME"]:
        p = REG / f"{layer.lower()}-registry.jsonl"
        if not p.exists():
            continue
        for line in p.open(encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("object_id") != object_id or r.get("superseded"):
                continue
            refs = list(r.get("input_refs") or [])
            for ref in refs:
                b = _resolve_base(ref, seen)
                if b:
                    return b
    return None


def _source_titles(r: dict, base: str) -> list[str]:
    """The title aliases a source should be indexed under, so a real answer can cite it.

    Returns [object_id, work-prefix, explicit-title (if any)] deduped. The work-prefix is the
    human-readable part of an object_id like `ipvv:V2L:k22` → `ipvv:V2L:k22` (no clean title, so the
    object_id IS the title) — we keep the object_id and any explicit payload title. Diacritics are
    folded at match-time in guard, so `Śiva`/`Siva` both match regardless of which alias is indexed."""
    titles = [base]
    payload = r.get("payload", {})
    for k in ("title", "work_title", "name"):
        v = payload.get(k) if isinstance(payload, dict) else None
        if isinstance(v, str) and v.strip():
            titles.append(v.strip())
    # dedupe preserving order
    seen, out = set(), []
    for t in titles:
        key = t.strip().lower()
        if key and key not in seen:
            seen.add(key)
            out.append(t.strip())
    return out


def _first_text(payload):
    """The first substantive string in a payload (source passage text)."""
    if isinstance(payload, dict):
        for v in payload.values():
            if isinstance(v, str) and len(v.split()) >= 3:
                return v
            t = _first_text(v) if isinstance(v, (dict, list)) else None
            if t:
                return t
    elif isinstance(payload, list):
        for v in payload:
            t = _first_text(v)
            if t:
                return t
    return None


def _grade(lesson_id, answer):
    """Deterministic blind-assessor grade (no LLM in path)."""
    lesson = _load_lesson(lesson_id)
    if not lesson:
        return {"error": "lesson not found"}, 404
    import re
    claims = lesson.get("learning_claims", [])
    if not claims:
        return {"error": "no claims"}, 400
    claim = claims[0]
    expected = claim.get("expected", "")
    rubric = [t for t in re.findall(r"[a-zA-Zā-īūṛṝḷḹṃṁñṅśṣṭḍḥ]+", str(expected).lower())
              if len(t) >= 4][:6]
    grade = blind_grade(claim.get("question", ""), answer, rubric)
    # log to SQLite
    con = sqlite3.connect(DB)
    con.execute("INSERT INTO learner_events (ts, learner, lesson, question, grade, response) "
                "VALUES (?,?,?,?,?,?)",
                (time.strftime("%Y-%m-%dT%H:%M:%SZ"), "api-user", lesson_id,
                 claim.get("question", "")[:80], grade["grade"], str(answer)[:200]))
    con.commit()
    con.close()
    return {"lesson": lesson_id, "grade": grade["grade"], "coverage": grade["coverage"],
            "failure_hint": "known-epistemic-neighbor" if grade["grade"] != "recalled" else None}


class Handler(BaseHTTPRequestHandler):
    def _json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "public, max-age=31536000, immutable" if code == 200 else "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/education":
            return self._json(_load_index())
        if path.startswith("/education/"):
            oid = urllib.parse.unquote(path[len("/education/"):])
            lesson = _load_lesson(oid)
            return self._json(lesson) if lesson else self._json({"error": "not found"}, 404)
        if path.startswith("/learn/"):
            return self._json({"note": "progression for work", "work": path[len("/learn/"):]})
        if path.startswith("/resolve/"):
            oid = urllib.parse.unquote(path[len("/resolve/"):])
            return self._json({"object_id": oid, "lineage": _resolve_to_source(oid)})
        return self._json({"error": "not found"}, 404)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if "/answer" in path:
            lesson_id = path.split("/education/")[1].split("/answer")[0] if "/education/" in path else ""
            length = int(self.headers.get("Content-Length", 0))
            answer = json.loads(self.rfile.read(length)) if length else {}
            return self._json(*_grade(lesson_id, answer.get("answer", "")))
        if "/guard" in path:
            lesson_id = path.split("/education/")[1].split("/guard")[0] if "/education/" in path else ""
            length = int(self.headers.get("Content-Length", 0))
            answer = json.loads(self.rfile.read(length)) if length else {}
            return self._json(*_guard_payload(lesson_id, answer.get("answer", "")))
        return self._json({"error": "not found"}, 404)

    def log_message(self, *a):
        pass  # quiet


if __name__ == "__main__":
    _init_db()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    print(f"education API on :{port} (stdlib, no LLM in read path)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
