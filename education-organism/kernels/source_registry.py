"""lib/source_registry.py — the source-registry pattern, adopted from fojin (GEM 1.1, translation).

GEM 1.1 (patala migration/v2/GEMS.md): fojin (xr843, 10,500+ texts / 613 sources) proves the harvest is
tractable at scale. The gem is the **source-registry pattern** — a DataSource model that captures, per
source: identity (code/name), categorization (languages/research_fields), access (type/API/IIIF), LIVE
HEALTH (health_status/confidence/unreachable_since — a prober signal), and RIGHTS (license_spdx — the
PANDiT rule / rights doctrine).

We had `source_refs` on claims but NO first-class source registry. This kernel closes that gap: every
claim's evidence resolves to a REGISTERED source (no dangling references), and the registry tracks
rights + health so the provenance graph is complete. This is what our context bundles / provenance /
essay-ingest reference as `source_refs` — now they resolve to a real registry entry.
"""
from __future__ import annotations
import hashlib, json


class Source:
    """A registered source (fojin DataSource pattern). Identity + access + rights + health."""

    def __init__(self, code, name, languages, access_type="external",
                 license_spdx=None, license_url=None, region=None,
                 research_fields="", supports_api=False, supports_iiif=False):
        self.code = code
        self.name = name
        self.languages = languages
        self.access_type = access_type          # local / external / api
        self.license_spdx = license_spdx        # SPDX or public-domain/unknown (rights doctrine)
        self.license_url = license_url
        self.region = region
        self.research_fields = research_fields  # the PANDiT / cross-canon categorization
        self.supports_api = supports_api
        self.supports_iiif = supports_iiif
        self.health_status = "ok"               # ok | degraded | unreachable (prober signal)
        self.health_confidence = "high"         # high | low
        self.unreachable_since = None
        self._hash = hashlib.sha256(f"{code}:{name}".encode()).hexdigest()[:16]

    def to_dict(self):
        return {"code": self.code, "name": self.name, "languages": self.languages,
                "access_type": self.access_type, "license_spdx": self.license_spdx,
                "research_fields": self.research_fields, "supports_api": self.supports_api,
                "supports_iiif": self.supports_iiif, "health_status": self.health_status,
                "health_confidence": self.health_confidence, "unreachable_since": self.unreachable_since,
                "id": self._hash}


class SourceRegistry:
    """The source registry: every evidence `source_ref` resolves to a registered source (no dangling)."""

    def __init__(self):
        self.sources = {}

    def register(self, src):
        self.sources[src.code] = src
        return src

    def resolve(self, code):
        """Resolve a claim's source_ref to a registered source (or None if unknown = dangling)."""
        return self.sources.get(code)

    def probe(self, code, reachable=True):
        """The prober signal (fojin health): update a source's reachability."""
        src = self.sources.get(code)
        if not src:
            return None
        if reachable:
            src.health_status = "ok"
            src.unreachable_since = None
        else:
            src.health_status = "unreachable"
            src.unreachable_since = src.unreachable_since or "now"
        return src

    def audit_evidence(self, claim_sources):
        """Check every claim's source_refs resolve to a registered, rights-audited source."""
        missing, no_rights, unreachable = [], [], []
        for code in claim_sources:
            src = self.resolve(code)
            if not src:
                missing.append(code)
            else:
                if not src.license_spdx:
                    no_rights.append(code)
                if src.health_status == "unreachable":
                    unreachable.append(code)
        return {"missing": missing, "no_rights": no_rights, "unreachable": unreachable}

    def to_dict(self):
        return {"sources": [s.to_dict() for s in self.sources.values()],
                "count": len(self.sources)}
