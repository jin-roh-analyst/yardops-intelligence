"""Pricing outcome summaries."""

from __future__ import annotations

import pandas as pd


def summarize_partner_performance(quote_context: pd.DataFrame) -> list[dict[str, object]]:
    grouped = quote_context.groupby(["partner_id", "partner_name", "partner_tier"], as_index=False).agg(
        quote_count=("quote_id", "count"),
        acceptance_rate=("accepted_flag", "mean"),
        avg_expected_margin=("expected_margin", "mean"),
        avg_net_expected_recovery=("net_expected_recovery", "mean"),
        avg_price_gap_vs_competitor=("price_gap_vs_competitor", "mean"),
        avg_predicted_acceptance_probability=("predicted_acceptance_probability", "mean"),
        monthly_claim_volume=("monthly_claim_volume", "first"),
        relationship_score=("relationship_score", "first"),
    )
    grouped["acceptance_rate"] *= 100
    grouped["avg_predicted_acceptance_probability"] *= 100
    return grouped.round(2).sort_values(["quote_count", "acceptance_rate"], ascending=[False, False]).to_dict("records")
