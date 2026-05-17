"""Retrieval performance summary helpers."""

from __future__ import annotations

import pandas as pd


def summarize_by(df: pd.DataFrame, column: str) -> list[dict[str, object]]:
    summary = df.groupby(column, dropna=False, as_index=False).agg(
        retrieval_count=("retrieval_id", "count"),
        avg_retrieval_duration_minutes=("retrieval_duration_minutes", "mean"),
        median_retrieval_duration_minutes=("retrieval_duration_minutes", "median"),
        avg_wait_time_minutes=("wait_time_minutes", "mean"),
        delay_rate=("delay_flag", "mean"),
        avg_blocked_vehicle_count=("blocked_vehicle_count", "mean"),
    )
    summary["delay_rate"] *= 100
    return summary.round(2).sort_values("retrieval_count", ascending=False).to_dict("records")
