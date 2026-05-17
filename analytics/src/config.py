"""Shared paths and table names for the YardOps analytics pipeline."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
ANALYTICS_OUTPUT_DIR = PROJECT_ROOT / "analytics" / "outputs"
WEB_DATA_DIR = PROJECT_ROOT / "web" / "public" / "data"

REQUIRED_TABLES = [
    "insurance_partners",
    "yard_locations",
    "vehicles",
    "vehicle_location_history",
    "retrieval_events",
    "tow_events",
    "yard_storage_events",
    "quote_outcomes",
    "pricing_scenarios",
    "yard_allocation_scenarios",
]

REQUIRED_EXPORTS = [
    "metrics.json",
    "yard_zone_performance.json",
    "retrieval_drivers.json",
    "allocation_strategy_comparison.json",
    "partner_performance.json",
    "pricing_scenarios_summary.json",
    "vehicles_sample.json",
    "methodology_summary.json",
]
