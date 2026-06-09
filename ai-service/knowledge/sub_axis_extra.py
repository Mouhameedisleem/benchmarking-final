"""
Sub-axis extra knowledge public interface.

Thin facade over sector_loader — single entry point for the rest of the stack.
Import only this module; never import sector_loader directly from other layers.
"""

from __future__ import annotations

try:
    from knowledge.sector_loader import load_sub_axis, load_sub_axis_fuzzy, warmup_cache, clear_cache
except ImportError:
    from sector_loader import load_sub_axis, load_sub_axis_fuzzy, warmup_cache, clear_cache  # type: ignore[no-redef]


def _normalize_sector_json(raw: dict) -> dict:
    """Map sector JSON file field names to the canonical keys used by benchmarking_engine."""
    if not raw:
        return raw

    out = dict(raw)

    # trends → tendances
    if "trends" in raw and "tendances" not in raw:
        out["tendances"] = [
            {
                "titre":       t.get("title", ""),
                "description": t.get("description", ""),
                "source":      t.get("source", ""),
                "annee":       str(t.get("year", "")),
            }
            for t in raw["trends"]
        ]

    # market_leaders → leaders_nationaux / leaders_regionaux / leaders_internationaux
    ml = raw.get("market_leaders")
    if isinstance(ml, dict):
        if "national" in ml and "leaders_nationaux" not in raw:
            out["leaders_nationaux"] = [
                {
                    "entreprise": l.get("organisation", ""),
                    "pays":       l.get("country", ""),
                    "pratique":   l.get("key_practice", ""),
                    "source":     l.get("source", ""),
                }
                for l in ml.get("national", [])
            ]
        if "regional" in ml and "leaders_regionaux" not in raw:
            out["leaders_regionaux"] = [
                {
                    "entreprise": l.get("organisation", ""),
                    "pays":       l.get("country", ""),
                    "pratique":   l.get("key_practice", ""),
                    "source":     l.get("source", ""),
                }
                for l in ml.get("regional", [])
            ]
        if "international" in ml and "leaders_internationaux" not in raw:
            out["leaders_internationaux"] = [
                {
                    "entreprise": l.get("organisation", ""),
                    "pays":       l.get("country", ""),
                    "pratique":   l.get("key_practice", ""),
                    "source":     l.get("source", ""),
                }
                for l in ml.get("international", [])
            ]

    # regulations → cadre_juridique
    if "regulations" in raw and "cadre_juridique" not in raw:
        out["cadre_juridique"] = [
            {
                "texte":       r.get("name", ""),
                "description": (
                    f"{r.get('issuing_body', '')} — {r.get('key_requirement', '')}"
                    if r.get("issuing_body") else r.get("key_requirement", "")
                ),
                "impact":      r.get("compliance_deadline", ""),
            }
            for r in raw["regulations"]
        ]

    # ma_and_fundraising → ma_levees_fonds
    if "ma_and_fundraising" in raw and "ma_levees_fonds" not in raw:
        out["ma_levees_fonds"] = [
            {
                "operation": m.get("type", ""),
                "detail": (
                    f"{m.get('acquirer_or_investor', '')} / {m.get('target', '')}"
                    + (f" — {m.get('strategic_rationale', '')}" if m.get("strategic_rationale") else "")
                ),
                "montant":   m.get("amount", ""),
                "annee":     str(m.get("date", "")),
            }
            for m in raw["ma_and_fundraising"]
        ]

    # ai_context → analyse_statique + maturite_maximale
    ai_ctx = raw.get("ai_context")
    if isinstance(ai_ctx, dict):
        if "static_analysis" in ai_ctx and "analyse_statique" not in raw:
            out["analyse_statique"] = ai_ctx["static_analysis"]
        if "maturity_max_description" in ai_ctx and "maturite_maximale" not in raw:
            out["maturite_maximale"] = ai_ctx["maturity_max_description"]

    # risks → risques
    if "risks" in raw and "risques" not in raw:
        out["risques"] = raw["risks"]

    # opportunities → opportunites
    if "opportunities" in raw and "opportunites" not in raw:
        out["opportunites"] = raw["opportunities"]

    return out


def get_sub_axis_extra(axis: str, sub_axis: str, sector: str = "") -> dict:
    """
    Return enrichment data for a (axis, sub_axis) pair — exact key match only.
    Use get_sub_axis_extra_fuzzy for AI-generated sub-axis names.
    """
    raw = load_sub_axis(axis, sub_axis, sector)
    return _normalize_sector_json(raw)


def get_sub_axis_extra_fuzzy(axis: str, sub_axis: str, sector: str = "") -> dict:
    """
    Return enrichment data using fuzzy keyword matching.

    Designed for AI-generated sub-axis names that don't exactly match
    the static KB keys. Falls back to best keyword-overlap match.

    Args:
        axis:     e.g. "BUSINESS", "CANAUX_DISTRIBUTION"
        sub_axis: e.g. "Expérience assuré digitale", "Stratégie InsurTech"
        sector:   e.g. "insurance", "sante", "retail" (case-insensitive)

    Returns:
        dict with zoom_case_study, cadre_juridique, leaders, trends, etc.
        Empty dict when no match found — never raises.
    """
    raw = load_sub_axis_fuzzy(axis, sub_axis, sector)
    return _normalize_sector_json(raw)


__all__ = ["get_sub_axis_extra", "get_sub_axis_extra_fuzzy", "warmup_cache", "clear_cache"]
