"""Yard allocation analytics summaries."""

from __future__ import annotations

import pandas as pd


def summarize_allocation_strategies(allocation_context: pd.DataFrame) -> list[dict[str, object]]:
    grouped = allocation_context.groupby("allocation_strategy", as_index=False).agg(
        scenario_count=("allocation_scenario_id", "count"),
        avg_retrieval_duration_minutes=("simulated_retrieval_duration_minutes", "mean"),
        avg_wait_time_minutes=("simulated_wait_time_minutes", "mean"),
        avg_travel_distance_meters=("simulated_travel_distance_meters", "mean"),
        avg_blocked_vehicle_count=("blocked_vehicle_count_estimate", "mean"),
        pct_under_15_min=("retrieval_under_15_min_flag", "mean"),
        high_priority_count=("high_priority_flag", "sum"),
        avg_priority_weighted_time=("priority_weighted_time", "mean"),
        avg_allocation_efficiency_score=("allocation_efficiency_score", "mean"),
    )
    grouped["pct_under_15_min"] *= 100
    return grouped.round(2).to_dict("records")
