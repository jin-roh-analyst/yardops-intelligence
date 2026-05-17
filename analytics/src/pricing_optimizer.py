"""Pricing scenario optimizer summaries."""

from __future__ import annotations

import pandas as pd


def summarize_pricing_scenarios(pricing_context: pd.DataFrame) -> dict[str, list[dict[str, object]]]:
    by_objective = pricing_context.groupby("optimization_objective", as_index=False).agg(
        scenario_count=("scenario_id", "count"),
        avg_acceptance_probability=("scenario_acceptance_probability", "mean"),
        avg_expected_margin=("scenario_expected_margin", "mean"),
        avg_expected_value=("scenario_expected_value", "mean"),
        recommended_count=("recommended_flag", "sum"),
    )
    by_objective["avg_acceptance_probability"] *= 100

    by_strategy = pricing_context.groupby("pricing_strategy", as_index=False).agg(
        scenario_count=("scenario_id", "count"),
        avg_total_partner_cost=("scenario_total_partner_cost", "mean"),
        avg_expected_margin=("scenario_expected_margin", "mean"),
        avg_expected_value=("scenario_expected_value", "mean"),
        recommended_count=("recommended_flag", "sum"),
    )

    recommended = pricing_context[pricing_context["recommended_flag"] == 1].copy()
    recommended_summary = recommended.groupby("pricing_strategy", as_index=False).agg(
        recommended_quotes=("quote_id", "count"),
        avg_recommended_tow_price=("scenario_tow_price", "mean"),
        avg_recommended_daily_storage_rate=("scenario_daily_storage_rate", "mean"),
        avg_recommended_partner_cost=("scenario_total_partner_cost", "mean"),
        avg_recommended_expected_value=("scenario_expected_value", "mean"),
    )

    return {
        "by_objective": by_objective.round(2).to_dict("records"),
        "by_pricing_strategy": by_strategy.round(2).to_dict("records"),
        "recommended_summary": recommended_summary.round(2).to_dict("records"),
    }
