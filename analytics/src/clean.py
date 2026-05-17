"""Load and validate raw YardOps CSV inputs."""

from __future__ import annotations

import pandas as pd

try:
    from .config import DATA_RAW_DIR, REQUIRED_TABLES
except ImportError:  # pragma: no cover - supports direct script execution
    from config import DATA_RAW_DIR, REQUIRED_TABLES


def load_raw_tables(raw_dir=DATA_RAW_DIR) -> dict[str, pd.DataFrame]:
    """Read every required raw CSV into a DataFrame."""
    tables: dict[str, pd.DataFrame] = {}
    missing = []
    for table in REQUIRED_TABLES:
        path = raw_dir / f"{table}.csv"
        if not path.exists():
            missing.append(str(path))
            continue
        tables[table] = pd.read_csv(path)
    if missing:
        raise FileNotFoundError("Missing raw CSV files: " + ", ".join(missing))
    return tables


def prepare_tables(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Apply lightweight type cleanup needed by the export aggregations."""
    prepared = {name: df.copy() for name, df in tables.items()}

    for name in ["vehicles", "retrieval_events", "quote_outcomes", "pricing_scenarios", "yard_allocation_scenarios", "yard_locations", "yard_storage_events", "insurance_partners"]:
        for column in prepared[name].columns:
            if column.endswith("_flag"):
                prepared[name][column] = pd.to_numeric(prepared[name][column], errors="coerce").fillna(0).astype(int)

    numeric_columns = {
        "vehicles": [
            "estimated_salvage_value",
            "estimated_sale_probability",
            "expected_days_to_sale",
            "actual_days_to_sale",
            "partner_priority_score",
            "operational_complexity_score",
            "priority_score",
        ],
        "retrieval_events": [
            "retrieval_duration_minutes",
            "wait_time_minutes",
            "start_delay_minutes",
            "travel_distance_meters",
            "blocked_vehicle_count",
        ],
        "yard_locations": [
            "distance_to_gate_meters",
            "current_occupancy",
            "occupancy_rate",
            "congestion_score",
            "accessibility_score",
        ],
        "quote_outcomes": [
            "quoted_tow_price",
            "quoted_daily_storage_rate",
            "expected_days_in_yard",
            "expected_billable_storage_days",
            "estimated_total_cost_to_partner",
            "estimated_salvage_value",
            "net_expected_recovery",
            "competitor_estimated_total_cost",
            "price_gap_vs_competitor",
            "partner_price_sensitivity_score",
            "yard_capacity_utilization",
            "predicted_acceptance_probability",
            "expected_margin",
            "recommended_tow_price",
            "recommended_daily_storage_rate",
        ],
        "pricing_scenarios": [
            "scenario_tow_price",
            "scenario_daily_storage_rate",
            "scenario_free_storage_days",
            "scenario_total_partner_cost",
            "scenario_expected_revenue",
            "scenario_expected_cost",
            "scenario_expected_margin",
            "scenario_acceptance_probability",
            "scenario_expected_value",
        ],
        "yard_allocation_scenarios": [
            "vehicle_priority_score",
            "zone_accessibility_score",
            "simulated_retrieval_duration_minutes",
            "simulated_wait_time_minutes",
            "simulated_travel_distance_meters",
            "blocked_vehicle_count_estimate",
            "priority_weighted_time",
            "allocation_efficiency_score",
        ],
        "insurance_partners": [
            "monthly_claim_volume",
            "avg_vehicle_salvage_value",
            "price_sensitivity_score",
            "historical_win_rate",
            "target_margin",
            "relationship_score",
        ],
        "yard_storage_events": [
            "days_in_yard",
            "billable_storage_days",
            "daily_storage_rate",
            "total_storage_fee",
            "yard_cost_per_day",
            "total_yard_cost",
            "storage_margin",
            "capacity_utilization_at_arrival",
        ],
    }
    for table, columns in numeric_columns.items():
        for column in columns:
            prepared[table][column] = pd.to_numeric(prepared[table][column], errors="coerce")

    for table, columns in {
        "vehicles": ["arrival_date", "sale_date", "pickup_date", "created_at", "updated_at"],
        "retrieval_events": ["request_time", "retrieval_start_time", "retrieval_end_time", "handoff_time"],
        "quote_outcomes": ["quote_date"],
        "vehicle_location_history": ["assignment_date"],
        "tow_events": ["tow_request_time", "tow_completed_time"],
        "yard_storage_events": ["arrival_date", "release_date"],
    }.items():
        for column in columns:
            prepared[table][column] = pd.to_datetime(prepared[table][column], errors="coerce")

    return prepared


def validate_relationships(tables: dict[str, pd.DataFrame]) -> None:
    """Fail fast if generated raw data has broken parent-child relationships."""
    partners = set(tables["insurance_partners"]["partner_id"])
    vehicles = set(tables["vehicles"]["vehicle_id"])
    yards = set(tables["yard_locations"]["yard_id"])
    quotes = set(tables["quote_outcomes"]["quote_id"])

    checks = [
        ("vehicles.partner_id", set(tables["vehicles"]["partner_id"]), partners),
        ("quote_outcomes.partner_id", set(tables["quote_outcomes"]["partner_id"]), partners),
        ("tow_events.partner_id", set(tables["tow_events"]["partner_id"]), partners),
        ("pricing_scenarios.partner_id", set(tables["pricing_scenarios"]["partner_id"]), partners),
        ("vehicles.yard_id", set(tables["vehicles"]["yard_id"]), yards),
        ("retrieval_events.yard_id", set(tables["retrieval_events"]["yard_id"]), yards),
        ("quote_outcomes.yard_id", set(tables["quote_outcomes"]["yard_id"]), yards),
        ("yard_allocation_scenarios.yard_id", set(tables["yard_allocation_scenarios"]["yard_id"]), yards),
        ("vehicle_location_history.vehicle_id", set(tables["vehicle_location_history"]["vehicle_id"]), vehicles),
        ("retrieval_events.vehicle_id", set(tables["retrieval_events"]["vehicle_id"]), vehicles),
        ("tow_events.vehicle_id", set(tables["tow_events"]["vehicle_id"]), vehicles),
        ("yard_storage_events.vehicle_id", set(tables["yard_storage_events"]["vehicle_id"]), vehicles),
        ("quote_outcomes.vehicle_id", set(tables["quote_outcomes"]["vehicle_id"]), vehicles),
        ("pricing_scenarios.vehicle_id", set(tables["pricing_scenarios"]["vehicle_id"]), vehicles),
        ("yard_allocation_scenarios.vehicle_id", set(tables["yard_allocation_scenarios"]["vehicle_id"]), vehicles),
        ("pricing_scenarios.quote_id", set(tables["pricing_scenarios"]["quote_id"]), quotes),
    ]
    for label, child_values, parent_values in checks:
        missing = child_values - parent_values
        if missing:
            sample = ", ".join(sorted(str(value) for value in list(missing)[:5]))
            raise ValueError(f"Broken relationship {label}: {sample}")
