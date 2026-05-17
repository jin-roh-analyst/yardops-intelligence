"""Export dashboard-ready JSON files for the YardOps frontend."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from .clean import load_raw_tables, prepare_tables, validate_relationships
    from .config import ANALYTICS_OUTPUT_DIR, DATA_RAW_DIR, REQUIRED_EXPORTS, WEB_DATA_DIR
    from .features import build_feature_tables
    from .pricing_model import summarize_partner_performance
    from .pricing_optimizer import summarize_pricing_scenarios
    from .retrieval_model import summarize_by
    from .yard_allocation import summarize_allocation_strategies
except ImportError:  # pragma: no cover - supports direct script execution
    from clean import load_raw_tables, prepare_tables, validate_relationships
    from config import ANALYTICS_OUTPUT_DIR, DATA_RAW_DIR, REQUIRED_EXPORTS, WEB_DATA_DIR
    from features import build_feature_tables
    from pricing_model import summarize_partner_performance
    from pricing_optimizer import summarize_pricing_scenarios
    from retrieval_model import summarize_by
    from yard_allocation import summarize_allocation_strategies


def generated_at() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, pd.Timestamp):
        return None if pd.isna(value) else value.isoformat()
    if pd.isna(value):
        return None
    return value


def base_payload() -> dict[str, str]:
    return {
        "generated_at": generated_at(),
        "source": "data/raw synthetic CSVs",
    }


def build_metrics(tables: dict[str, pd.DataFrame], features: dict[str, pd.DataFrame]) -> dict[str, Any]:
    retrievals = features["retrieval_context"]
    quotes = tables["quote_outcomes"]
    yards = tables["yard_locations"]
    vehicles = tables["vehicles"]
    return {
        **base_payload(),
        "summary": {
            "total_vehicles": int(len(vehicles)),
            "active_yards": int(yards["yard_id"].nunique()),
            "average_retrieval_time_minutes": round(float(retrievals["retrieval_duration_minutes"].mean()), 2),
            "median_retrieval_time_minutes": round(float(retrievals["retrieval_duration_minutes"].median()), 2),
            "percent_retrievals_under_15_minutes": round(float((retrievals["retrieval_duration_minutes"] < 15).mean() * 100), 2),
            "average_customer_carrier_wait_minutes": round(float(retrievals["wait_time_minutes"].mean()), 2),
            "average_yard_utilization": round(float(yards["occupancy_rate"].mean() * 100), 2),
            "quote_acceptance_rate": round(float(quotes["accepted_flag"].mean() * 100), 2),
            "average_expected_margin": round(float(quotes["expected_margin"].mean()), 2),
            "average_partner_net_recovery": round(float(quotes["net_expected_recovery"].mean()), 2),
        },
        "table_row_counts": {name: int(len(df)) for name, df in tables.items()},
    }


def build_yard_zone_performance(tables: dict[str, pd.DataFrame], features: dict[str, pd.DataFrame]) -> dict[str, Any]:
    retrievals = features["retrieval_context"]
    yard_zone = features["yard_zone"]
    zone_retrieval = retrievals.groupby(["yard_id", "assigned_zone_id"], dropna=False, as_index=False).agg(
        retrieval_count=("retrieval_id", "count"),
        avg_retrieval_duration_minutes=("retrieval_duration_minutes", "mean"),
        avg_wait_time_minutes=("wait_time_minutes", "mean"),
        delay_rate=("delay_flag", "mean"),
    )
    records = yard_zone.merge(
        zone_retrieval,
        left_on=["yard_id", "zone_id"],
        right_on=["yard_id", "assigned_zone_id"],
        how="left",
    )
    records["retrieval_count"] = records["retrieval_count"].fillna(0).astype(int)
    records["delay_rate"] = records["delay_rate"].fillna(0) * 100
    records = records.drop(columns=["assigned_zone_id"])

    yard_summary = records.groupby("yard_id", as_index=False).agg(
        zones=("zone_id", "count"),
        avg_occupancy_rate=("occupancy_rate", "mean"),
        avg_congestion_score=("congestion_score", "mean"),
        avg_accessibility_score=("accessibility_score", "mean"),
        total_retrievals=("retrieval_count", "sum"),
        avg_retrieval_duration_minutes=("avg_retrieval_duration_minutes", "mean"),
    )
    yard_summary["avg_occupancy_rate"] *= 100

    return {
        **base_payload(),
        "summary": {
            "zone_count": int(len(records)),
            "fast_access_utilization": round(float(records.loc[records["zone_type"] == "fast_access", "occupancy_rate"].mean() * 100), 2),
            "overflow_usage_rate": round(float(records.loc[records["zone_type"] == "overflow", "occupancy_rate"].mean() * 100), 2),
            "avg_zone_congestion_score": round(float(records["congestion_score"].mean()), 2),
        },
        "yards": yard_summary.round(2).to_dict("records"),
        "records": records.round(2).to_dict("records"),
    }


def build_retrieval_drivers(features: dict[str, pd.DataFrame]) -> dict[str, Any]:
    retrievals = features["retrieval_context"]
    blocked_bins = retrievals.copy()
    blocked_bins["blocked_vehicle_bucket"] = pd.cut(
        blocked_bins["blocked_vehicle_count"],
        bins=[-1, 0, 2, 5, 20],
        labels=["0", "1-2", "3-5", "6+"],
    ).astype(str)
    return {
        **base_payload(),
        "summary": {
            "retrieval_count": int(len(retrievals)),
            "delay_rate": round(float(retrievals["delay_flag"].mean() * 100), 2),
            "avg_blocked_vehicle_count": round(float(retrievals["blocked_vehicle_count"].mean()), 2),
        },
        "delay_reasons": summarize_by(retrievals, "delay_reason"),
        "equipment": summarize_by(retrievals, "equipment_used"),
        "blocked_vehicle_buckets": summarize_by(blocked_bins, "blocked_vehicle_bucket"),
        "zone_types": summarize_by(retrievals, "zone_type"),
        "pickup_types": summarize_by(retrievals, "pickup_type"),
    }


def build_allocation_strategy_comparison(features: dict[str, pd.DataFrame]) -> dict[str, Any]:
    allocation = features["allocation_context"]
    strategies = summarize_allocation_strategies(allocation)
    by_vehicle_type = allocation.groupby(["allocation_strategy", "vehicle_type"], as_index=False).agg(
        scenario_count=("allocation_scenario_id", "count"),
        avg_retrieval_duration_minutes=("simulated_retrieval_duration_minutes", "mean"),
        avg_allocation_efficiency_score=("allocation_efficiency_score", "mean"),
    )
    return {
        **base_payload(),
        "summary": {
            "scenario_count": int(len(allocation)),
            "strategy_count": int(allocation["allocation_strategy"].nunique()),
            "best_strategy_by_efficiency": max(strategies, key=lambda item: item["avg_allocation_efficiency_score"])["allocation_strategy"],
        },
        "strategies": strategies,
        "by_vehicle_type": by_vehicle_type.round(2).to_dict("records"),
    }


def build_partner_performance(features: dict[str, pd.DataFrame]) -> dict[str, Any]:
    quote_context = features["quote_context"]
    tier = quote_context.groupby("partner_tier", as_index=False).agg(
        quote_count=("quote_id", "count"),
        acceptance_rate=("accepted_flag", "mean"),
        avg_expected_margin=("expected_margin", "mean"),
        avg_net_expected_recovery=("net_expected_recovery", "mean"),
        avg_price_gap_vs_competitor=("price_gap_vs_competitor", "mean"),
    )
    tier["acceptance_rate"] *= 100
    return {
        **base_payload(),
        "summary": {
            "partner_count": int(quote_context["partner_id"].nunique()),
            "quote_count": int(len(quote_context)),
            "overall_acceptance_rate": round(float(quote_context["accepted_flag"].mean() * 100), 2),
        },
        "tiers": tier.round(2).to_dict("records"),
        "partners": summarize_partner_performance(quote_context),
    }


def build_pricing_scenarios_summary(features: dict[str, pd.DataFrame]) -> dict[str, Any]:
    pricing = features["pricing_context"]
    summaries = summarize_pricing_scenarios(pricing)
    return {
        **base_payload(),
        "summary": {
            "scenario_count": int(len(pricing)),
            "recommended_scenario_count": int(pricing["recommended_flag"].sum()),
            "avg_scenario_expected_margin": round(float(pricing["scenario_expected_margin"].mean()), 2),
            "avg_scenario_expected_value": round(float(pricing["scenario_expected_value"].mean()), 2),
        },
        **summaries,
    }


def build_vehicles_sample(features: dict[str, pd.DataFrame], limit: int = 250) -> dict[str, Any]:
    vehicles = features["vehicle_context"].sort_values(["priority_score", "estimated_salvage_value"], ascending=[False, False]).head(limit)
    columns = [
        "vehicle_id",
        "claim_id",
        "partner_id",
        "partner_name",
        "partner_tier",
        "yard_id",
        "vehicle_status",
        "make",
        "model",
        "vehicle_type",
        "damage_type",
        "damage_severity",
        "drivability_status",
        "estimated_salvage_value",
        "expected_days_to_sale",
        "priority_score",
        "operational_complexity_score",
        "zone_type",
        "occupancy_rate",
        "congestion_score",
        "accessibility_score",
    ]
    return {
        **base_payload(),
        "summary": {
            "record_count": int(len(vehicles)),
            "selection": "Top vehicles by priority score and estimated salvage value",
        },
        "records": vehicles[columns].round(2).to_dict("records"),
    }


def build_methodology_summary(tables: dict[str, pd.DataFrame]) -> dict[str, Any]:
    return {
        **base_payload(),
        "summary": {
            "project": "YardOps Intelligence",
            "data_type": "Synthetic operational analytics data",
            "pipeline": "Raw CSVs are cleaned, joined, aggregated, and exported as static JSON for the frontend.",
        },
        "source_tables": [{"table": name, "rows": int(len(df))} for name, df in tables.items()],
        "assumptions": [
            "Vehicles in farther, more congested zones usually have longer retrieval times.",
            "Non-running and heavy vehicles require more equipment and take longer to retrieve.",
            "Higher quoted prices and storage rates reduce acceptance for price-sensitive partners.",
            "Optimized allocation improves retrieval outcomes for high-priority vehicles.",
            "The data is synthetic and does not contain confidential or real company records.",
        ],
        "exports": REQUIRED_EXPORTS,
    }


def write_json(name: str, payload: dict[str, Any], output_dirs: list[Path]) -> None:
    for output_dir in output_dirs:
        output_dir.mkdir(parents=True, exist_ok=True)
        with (output_dir / name).open("w") as f:
            json.dump(json_ready(payload), f, indent=2)
            f.write("\n")


def build_exports() -> dict[str, dict[str, Any]]:
    raw_tables = load_raw_tables(DATA_RAW_DIR)
    validate_relationships(raw_tables)
    tables = prepare_tables(raw_tables)
    features = build_feature_tables(tables)
    return {
        "metrics.json": build_metrics(tables, features),
        "yard_zone_performance.json": build_yard_zone_performance(tables, features),
        "retrieval_drivers.json": build_retrieval_drivers(features),
        "allocation_strategy_comparison.json": build_allocation_strategy_comparison(features),
        "partner_performance.json": build_partner_performance(features),
        "pricing_scenarios_summary.json": build_pricing_scenarios_summary(features),
        "vehicles_sample.json": build_vehicles_sample(features),
        "methodology_summary.json": build_methodology_summary(tables),
    }


def main() -> None:
    exports = build_exports()
    missing = set(REQUIRED_EXPORTS) - set(exports)
    if missing:
        raise RuntimeError(f"Missing required exports: {sorted(missing)}")
    for name, payload in exports.items():
        write_json(name, payload, [ANALYTICS_OUTPUT_DIR, WEB_DATA_DIR])
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
