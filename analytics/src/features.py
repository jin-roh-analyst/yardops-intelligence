"""Feature preparation for dashboard exports."""

from __future__ import annotations

import pandas as pd


def build_feature_tables(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Create joined datasets used by multiple export summaries."""
    vehicles = tables["vehicles"]
    partners = tables["insurance_partners"]
    yards = tables["yard_locations"]
    retrievals = tables["retrieval_events"]
    quotes = tables["quote_outcomes"]
    allocations = tables["yard_allocation_scenarios"]
    pricing = tables["pricing_scenarios"]

    yard_zone = yards.groupby(["yard_id", "zone_id", "zone_type"], as_index=False).agg(
        slots=("slot_id", "count"),
        occupancy_rate=("occupancy_rate", "mean"),
        congestion_score=("congestion_score", "mean"),
        accessibility_score=("accessibility_score", "mean"),
        avg_distance_to_gate_meters=("distance_to_gate_meters", "mean"),
    )

    location_current = tables["vehicle_location_history"].sort_values("assignment_date").drop_duplicates("vehicle_id", keep="last")
    vehicle_context = (
        vehicles.merge(partners[["partner_id", "partner_name", "partner_tier", "price_sensitivity_score"]], on="partner_id", how="left")
        .merge(location_current[["vehicle_id", "assigned_zone_id", "assigned_slot_id", "allocation_strategy"]], on="vehicle_id", how="left")
        .merge(
            yard_zone[["yard_id", "zone_id", "zone_type", "occupancy_rate", "congestion_score", "accessibility_score"]],
            left_on=["yard_id", "assigned_zone_id"],
            right_on=["yard_id", "zone_id"],
            how="left",
        )
    )

    retrieval_context = (
        retrievals.merge(vehicles[["vehicle_id", "partner_id", "vehicle_type", "drivability_status", "priority_score", "operational_complexity_score"]], on="vehicle_id", how="left")
        .merge(location_current[["vehicle_id", "assigned_zone_id", "assigned_slot_id", "allocation_strategy"]], on="vehicle_id", how="left")
        .merge(
            yard_zone[["yard_id", "zone_id", "zone_type", "congestion_score", "accessibility_score"]],
            left_on=["yard_id", "assigned_zone_id"],
            right_on=["yard_id", "zone_id"],
            how="left",
        )
    )

    quote_context = quotes.merge(partners[["partner_id", "partner_name", "partner_tier", "monthly_claim_volume", "relationship_score"]], on="partner_id", how="left")
    pricing_context = pricing.merge(quotes[["quote_id", "pricing_strategy", "accepted_flag", "estimated_total_cost_to_partner"]], on="quote_id", how="left")
    allocation_context = allocations.merge(vehicles[["vehicle_id", "vehicle_type", "drivability_status"]], on="vehicle_id", how="left")

    return {
        "yard_zone": yard_zone,
        "vehicle_context": vehicle_context,
        "retrieval_context": retrieval_context,
        "quote_context": quote_context,
        "pricing_context": pricing_context,
        "allocation_context": allocation_context,
    }
