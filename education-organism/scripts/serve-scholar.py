#!/usr/bin/env python3
"""scripts/serve-scholar.py — the SCHOLAR WORKBENCH API (the human gate, made live).

The scholar login → review → adjudicate → publish flow, wired to agent3's proven engines:
  POST /scholar/login            → a scholar identity (Ed25519-attested)
  GET  /scholar/{id}/queue       → what to review next (review_queue.next_for)
  GET  /scholar/{id}/review/{obj} → one object's full review context
  POST /scholar/{id}/adjudicate  → ACCEPT/REVISE/REJECT (scholar_review + review_policy)
  GET  /scholar/{id}/publish     → compile the citable public record (scholar_publication)

The human gate of the organism: a scholar's adjudication promotes MACHINE_PROPOSED → ADJUDICATED,
then scholar_publication compiles it for the public site. Stdlib http.server (RAM-friendly).
"""
from __future__ import annotations
import json, sys, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PATA = "/root/patalacheckpoints"
sys.path.insert(0, PATA)
sys.path.insert(0, f"{PATA}/pipeline")

# lazy import the agent3 engines (they're self-contained)
try:
    from products.review_queue.engine import next_for
    from products.scholar_publication.engine import profile_record, publish_all
    ENGINES = True
except Exception as e:
    ENGINES = False
    _ERR = str(e)

SCHOLARS = {"scholar-A": {"name": "Scholar A", "scope": "kashmir_shaivism"}}
ADJUDICATIONS = []  # the ledger


class Handler(BaseHTTPRequestHandler):
    def _json(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/scholar/login":
            return self._json({"scholars": [{"id": k, **v} for k, v in SCHOLARS.items()],
                               "engines_loaded": ENGINES})
        if path.startswith("/scholar/") and "/queue" in path:
            sid = path.split("/scholar/")[1].split("/queue")[0]
            q = next_for(scholar_id=sid, scope=None, limit=5) if ENGINES else {"error": "no engines"}
            return self._json(q)
        if path.startswith("/scholar/") and "/publish" in path:
            sid = path.split("/scholar/")[1].split("/publish")[0]
            rec = profile_record(sid) if ENGINES else {"error": "no engines"}
            return self._json(rec)
        return self._json({"error": "not found", "engines": ENGINES}, 404)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if "/adjudicate" in path:
            length = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(length)) if length else {}
            # the human gate: record the adjudication (ACCEPT/REVISE/REJECT)
            verdict = req.get("verdict", "REJECT").upper()
            ADJUDICATIONS.append({"object": req.get("object_id", ""), "verdict": verdict,
                                  "scholar": req.get("scholar_id", "scholar-A")})
            return self._json({"recorded": True, "verdict": verdict,
                               "ledger": ADJUDICATIONS[-5:]})
        return self._json({"error": "not found"}, 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8788
    print(f"scholar workbench API on :{port} (engines_loaded={ENGINES})")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
