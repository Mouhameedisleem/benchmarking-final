"""
Sector-aware JSON knowledge loader.

Priority chain per sub-axis lookup:
  1. sectors/{sector}/{file}.json   (sector-specific override)
  2. sectors/_generic/{file}.json   (cross-sector fallback)
  3. {}                             (empty dict — never raises)

Alias support: sectors/{sector}/_alias.json → { "alias": "banque" }
Caching: lru_cache on individual file reads (reset on process restart).
"""

from __future__ import annotations

import json
import logging
from functools import lru_cache
from pathlib import Path

log = logging.getLogger(__name__)

# ── Paths ──────────────────────────────────────────────────────────────────────

_SECTORS_DIR = Path(__file__).parent / "sectors"

# ── Sub-axis → filename mapping ────────────────────────────────────────────────
# Key   : "AXIS::Sub-axis label" (must match sub_axis_data.py keys exactly)
# Value : filename stem (no .json extension)

_SUB_AXIS_FILE_MAP: dict[str, str] = {
    # AXE 1 — BUSINESS
    "BUSINESS::Stratégie digitale":             "BUSINESS__strategie_digitale",
    "BUSINESS::Orientation client":             "BUSINESS__orientation_client",
    "BUSINESS::Innovation":                     "BUSINESS__innovation",
    "BUSINESS::Modèle économique digital":      "BUSINESS__modele_economique_digital",
    # AXE 2 — PROCESS
    "PROCESS::Cartographie des processus":      "PROCESS__cartographie_processus",
    "PROCESS::Automatisation":                  "PROCESS__automatisation",
    "PROCESS::Agilité":                         "PROCESS__agilite",
    "PROCESS::Performance opérationnelle":      "PROCESS__performance_operationnelle",
    # AXE 3 — INFORMATION_SYSTEM
    "INFORMATION_SYSTEM::Infrastructure & Cloud":   "IS__infrastructure_cloud",
    "INFORMATION_SYSTEM::Cybersécurité":            "IS__cybersecurite",
    "INFORMATION_SYSTEM::Données & Analytics":      "IS__donnees_analytics",
    "INFORMATION_SYSTEM::Intégration & API":        "IS__integration_api",
    # AXE 4 — CANAUX_DISTRIBUTION
    "CANAUX_DISTRIBUTION::Canaux de distribution & expérience client": "CANAUX__canaux_experience_client",
    "CANAUX_DISTRIBUTION::Selfcare client":          "CANAUX__selfcare_client",
    # AXE 5 — MARKETING_COMMUNICATION
    "MARKETING_COMMUNICATION::Marketing & communication digitale": "MARKETING__marketing_digital",
    # AXE 6 — RH_CULTURE_DIGITALE
    "RH_CULTURE_DIGITALE::Culture digitale":                  "RH__culture_digitale",
    "RH_CULTURE_DIGITALE::Poste de travail du banquier":      "RH__poste_de_travail",
    "RH_CULTURE_DIGITALE::Collaboratif & digital working":    "RH__collaboratif_digital",
    "RH_CULTURE_DIGITALE::Digitalisation de la fonction RH":  "RH__digitalisation_rh",
    "RH_CULTURE_DIGITALE::Agilité":                           "RH__agilite",
    # AXE 7 — OFFRES_DIGITALES
    "OFFRES_DIGITALES::Offres digitales":              "OFFRES__offres_digitales",
    "OFFRES_DIGITALES::Open banking (BaaS, BaaP)":     "OFFRES__open_platform",
    # AXE 8 — MODELE_OPERATIONNEL_INNOVATION
    "MODELE_OPERATIONNEL_INNOVATION::Simplification & automatisation des processus": "MODELE_OP__simplification",
    "MODELE_OPERATIONNEL_INNOVATION::Gouvernance de la transformation digitale":     "MODELE_OP__gouvernance",
    "MODELE_OPERATIONNEL_INNOVATION::Développement de l'innovation":                 "MODELE_OP__innovation",
    # AXE 9 — IT_DATA
    "IT_DATA::Socle IT": "IT_DATA__socle_it",
    "IT_DATA::Data":     "IT_DATA__data",
}

# ── Internal helpers ───────────────────────────────────────────────────────────

@lru_cache(maxsize=32)
def _resolve_alias(sector: str) -> str:
    """
    Resolve a sector alias.
    Reads sectors/{sector}/_alias.json → { "alias": "target_sector" }.
    Returns the original sector name if no alias file exists.
    """
    if not sector:
        return sector
    alias_file = _SECTORS_DIR / sector / "_alias.json"
    if not alias_file.is_file():
        return sector
    try:
        data = json.loads(alias_file.read_text(encoding="utf-8"))
        target = data.get("alias", "").strip()
        if target and target != sector:
            log.debug("Sector alias: %s → %s", sector, target)
            return target
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("Could not read alias file %s: %s", alias_file, exc)
    return sector


@lru_cache(maxsize=512)
def _load_json_file(path: Path) -> dict | None:
    """
    Load, parse and cache a single JSON file.
    Returns None when the file does not exist.
    Returns None (with a warning) when JSON is malformed.
    Never raises.
    """
    if not path.is_file():
        return None
    try:
        content = path.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError as exc:
        log.error("Malformed JSON in %s — skipping: %s", path, exc)
        return None
    except OSError as exc:
        log.error("Cannot read %s: %s", path, exc)
        return None


def _file_path(sector: str, filename_stem: str) -> Path:
    return _SECTORS_DIR / sector / f"{filename_stem}.json"


# ── Public API ─────────────────────────────────────────────────────────────────

def load_sub_axis(axis: str, sub_axis: str, sector: str = "") -> dict:
    """
    Load extra knowledge for a (axis, sub_axis) pair with sector-aware fallback.

    Priority:
      1. sectors/{resolved_sector}/{file}.json  — sector override
      2. sectors/_generic/{file}.json           — cross-sector fallback
      3. {}                                     — safe empty dict

    Args:
        axis:      Axis key, e.g. "BUSINESS"
        sub_axis:  Sub-axis label, e.g. "Stratégie digitale"
        sector:    Sector slug (case-insensitive), e.g. "banque", "sante"

    Returns:
        dict with zoom_case_study, comparatif_organisations, trends, etc.
        Empty dict when no data is found (never raises).
    """
    key = f"{axis}::{sub_axis}"
    filename = _SUB_AXIS_FILE_MAP.get(key)

    if not filename:
        log.debug("No file mapping for key '%s' — returning empty dict", key)
        return {}

    sector_clean = sector.lower().strip()
    resolved = _resolve_alias(sector_clean) if sector_clean else ""

    # 1. Sector-specific override
    if resolved and resolved != "_generic":
        data = _load_json_file(_file_path(resolved, filename))
        if data is not None:
            log.debug("Loaded sector override: %s / %s", resolved, filename)
            return data

    # 2. Generic fallback
    data = _load_json_file(_file_path("_generic", filename))
    if data is not None:
        log.debug("Loaded _generic fallback: %s", filename)
        return data

    # 3. Nothing found
    log.debug("No knowledge file found for '%s' (sector=%s)", key, sector)
    return {}


def list_available_sectors() -> list[str]:
    """Return all sector folder names found under sectors/."""
    if not _SECTORS_DIR.is_dir():
        return []
    return [
        d.name for d in sorted(_SECTORS_DIR.iterdir())
        if d.is_dir() and not d.name.startswith(".")
    ]


def warmup_cache(sectors: list[str] | None = None) -> None:
    """
    Pre-load all JSON files into the lru_cache at startup.
    Call once from FastAPI lifespan to eliminate first-request latency.

    Args:
        sectors: list of sector slugs to warm up (default: all available sectors).
    """
    target_sectors = sectors or list_available_sectors()
    loaded = 0
    for sector in target_sectors:
        resolved = _resolve_alias(sector)
        for filename in _SUB_AXIS_FILE_MAP.values():
            path = _file_path(resolved, filename)
            if _load_json_file(path) is not None:
                loaded += 1
    log.info("Cache warmup complete — %d files loaded (%d sectors)", loaded, len(target_sectors))


def clear_cache() -> None:
    """Clear all lru_cache entries. Useful for testing."""
    _resolve_alias.cache_clear()
    _load_json_file.cache_clear()
    log.debug("Sector loader cache cleared")
