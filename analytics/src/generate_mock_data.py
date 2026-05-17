"""Generate synthetic YardOps raw CSV data.

The generator is deterministic and uses only the Python standard library so it
can run before the analytics environment has third-party dependencies.
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


SEED = 42
BASE_DATE = datetime(2025, 1, 1, 8, 0, 0)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

ROW_COUNTS = {
    "insurance_partners": 40,
    "yard_locations": 2_000,
    "vehicles": 10_000,
    "vehicle_location_history": 12_000,
    "retrieval_events": 5_000,
    "tow_events": 6_000,
    "yard_storage_events": 10_000,
    "quote_outcomes": 5_000,
    "pricing_scenarios": 50_000,
    "yard_allocation_scenarios": 30_000,
}

PARTNER_COLUMNS = [
    "partner_id",
    "partner_name",
    "partner_tier",
    "monthly_claim_volume",
    "avg_vehicle_salvage_value",
    "price_sensitivity_score",
    "service_level_requirement",
    "contract_type",
    "current_tow_rate",
    "current_daily_storage_rate",
    "free_storage_days",
    "historical_win_rate",
    "target_margin",
    "relationship_score",
    "active_flag",
]

YARD_COLUMNS = [
    "yard_id",
    "yard_name",
    "region",
    "zone_id",
    "row_id",
    "slot_id",
    "zone_type",
    "distance_to_gate_meters",
    "distance_to_office_meters",
    "distance_to_loading_area_meters",
    "capacity",
    "current_occupancy",
    "occupancy_rate",
    "congestion_score",
    "accessibility_score",
    "equipment_required",
    "surface_type",
    "indoor_flag",
    "active_flag",
]

VEHICLE_COLUMNS = [
    "vehicle_id",
    "claim_id",
    "partner_id",
    "yard_id",
    "arrival_date",
    "sale_date",
    "pickup_date",
    "vehicle_status",
    "make",
    "model",
    "model_year",
    "vehicle_age",
    "vehicle_type",
    "damage_type",
    "damage_severity",
    "drivability_status",
    "title_status",
    "estimated_salvage_value",
    "estimated_sale_probability",
    "expected_days_to_sale",
    "actual_days_to_sale",
    "pickup_required_flag",
    "customer_pickup_flag",
    "carrier_pickup_flag",
    "partner_priority_score",
    "operational_complexity_score",
    "priority_score",
    "created_at",
    "updated_at",
]

LOCATION_HISTORY_COLUMNS = [
    "location_event_id",
    "vehicle_id",
    "yard_id",
    "assigned_zone_id",
    "assigned_row_id",
    "assigned_slot_id",
    "assignment_date",
    "relocation_count",
    "relocated_flag",
    "current_location_flag",
    "initial_priority_score",
    "final_priority_score",
    "allocation_strategy",
    "assigned_by",
    "assignment_reason",
]

RETRIEVAL_COLUMNS = [
    "retrieval_id",
    "vehicle_id",
    "yard_id",
    "request_time",
    "retrieval_start_time",
    "retrieval_end_time",
    "handoff_time",
    "requested_by",
    "pickup_type",
    "retrieval_duration_minutes",
    "wait_time_minutes",
    "start_delay_minutes",
    "travel_distance_meters",
    "blocked_vehicle_count",
    "equipment_used",
    "staff_id",
    "retrieval_success_flag",
    "delay_flag",
    "delay_reason",
    "weather_condition",
    "time_of_day",
    "day_of_week",
]

PARTNER_EVENT_COLUMNS = [
    "tow_event_id",
    "claim_id",
    "vehicle_id",
    "partner_id",
    "origin_zip",
    "origin_city",
    "origin_state",
    "yard_id",
    "tow_distance_miles",
    "tow_request_time",
    "tow_completed_time",
    "tow_duration_hours",
    "tow_type",
    "base_tow_cost",
    "fuel_surcharge",
    "labor_cost",
    "third_party_tow_cost",
    "internal_total_tow_cost",
    "quoted_tow_price",
    "accepted_flag",
    "competitor_estimated_price",
    "gross_tow_margin",
    "outsourced_flag",
]

STORAGE_COLUMNS = [
    "storage_event_id",
    "vehicle_id",
    "partner_id",
    "yard_id",
    "arrival_date",
    "release_date",
    "days_in_yard",
    "free_storage_days",
    "billable_storage_days",
    "daily_storage_rate",
    "total_storage_fee",
    "yard_cost_per_day",
    "total_yard_cost",
    "storage_margin",
    "capacity_utilization_at_arrival",
    "long_hold_flag",
    "storage_billing_status",
]

QUOTE_COLUMNS = [
    "quote_id",
    "partner_id",
    "claim_id",
    "vehicle_id",
    "yard_id",
    "quote_date",
    "quoted_tow_price",
    "quoted_daily_storage_rate",
    "free_storage_days",
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
    "accepted_flag",
    "lost_reason",
    "expected_margin",
    "recommended_tow_price",
    "recommended_daily_storage_rate",
    "pricing_strategy",
]

PRICING_SCENARIO_COLUMNS = [
    "scenario_id",
    "quote_id",
    "partner_id",
    "vehicle_id",
    "scenario_tow_price",
    "scenario_daily_storage_rate",
    "scenario_free_storage_days",
    "scenario_total_partner_cost",
    "scenario_expected_revenue",
    "scenario_expected_cost",
    "scenario_expected_margin",
    "scenario_acceptance_probability",
    "scenario_expected_value",
    "meets_margin_threshold_flag",
    "meets_acceptance_threshold_flag",
    "recommended_flag",
    "optimization_objective",
]

ALLOCATION_COLUMNS = [
    "allocation_scenario_id",
    "simulation_run_id",
    "vehicle_id",
    "yard_id",
    "allocation_strategy",
    "assigned_zone_id",
    "assigned_slot_id",
    "vehicle_priority_score",
    "zone_accessibility_score",
    "simulated_retrieval_duration_minutes",
    "simulated_wait_time_minutes",
    "simulated_travel_distance_meters",
    "blocked_vehicle_count_estimate",
    "high_priority_flag",
    "retrieval_under_15_min_flag",
    "priority_weighted_time",
    "allocation_efficiency_score",
]


@dataclass(frozen=True)
class YardProfile:
    yard_id: str
    yard_name: str
    region: str


YARDS = [
    YardProfile("YARD_DAL_01", "Dallas North Yard", "Texas"),
    YardProfile("YARD_HOU_01", "Houston East Yard", "Texas"),
    YardProfile("YARD_AUS_01", "Austin Central Yard", "Texas"),
    YardProfile("YARD_OKC_01", "Oklahoma City Yard", "South Central"),
]

ZONE_PROFILES = {
    "fast_access": {"distance": (40, 180), "congestion": (10, 45), "access": (82, 99), "equipment": "none"},
    "standard": {"distance": (180, 750), "congestion": (25, 70), "access": (55, 85), "equipment": "none"},
    "overflow": {"distance": (850, 1_900), "congestion": (60, 98), "access": (15, 45), "equipment": "forklift"},
    "heavy_vehicle": {"distance": (450, 1_300), "congestion": (35, 75), "access": (35, 65), "equipment": "heavy_tow"},
    "non_running": {"distance": (350, 1_100), "congestion": (40, 85), "access": (35, 70), "equipment": "forklift"},
    "long_term_hold": {"distance": (700, 1_600), "congestion": (25, 65), "access": (25, 55), "equipment": "loader"},
}

ZONE_SEQUENCE = [
    ("fast_access", "FA"),
    ("standard", "A"),
    ("standard", "B"),
    ("overflow", "OF"),
    ("heavy_vehicle", "HV"),
    ("non_running", "NR"),
    ("long_term_hold", "LTH"),
]

MAKE_MODELS = {
    "Toyota": ["Camry", "Corolla", "RAV4", "Tacoma"],
    "Ford": ["F-150", "Escape", "Explorer", "Mustang"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
    "Chevrolet": ["Silverado", "Malibu", "Equinox", "Tahoe"],
    "BMW": ["3 Series", "5 Series", "X3", "X5"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Frontier"],
    "Kia": ["Sorento", "Optima", "Telluride", "Sportage"],
    "Ram": ["1500", "2500", "3500", "ProMaster"],
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def weighted_choice(rng: random.Random, choices: list[tuple[str, float]]) -> str:
    labels, weights = zip(*choices)
    return rng.choices(labels, weights=weights, k=1)[0]


def money(value: float) -> int:
    return int(round(value))


def pct(value: float) -> str:
    return f"{clamp(value, 0, 1):.2f}"


def dt(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def d(value: datetime | None) -> str:
    return "" if value is None else value.strftime("%Y-%m-%d")


def write_csv(path: Path, columns: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def generate_partners(rng: random.Random) -> list[dict[str, object]]:
    prefixes = ["NorthStar", "LonePeak", "Riverbend", "Summit", "MetroGuard", "Pioneer", "Canyon", "Harbor", "Prairie", "Evergreen"]
    suffixes = ["Mutual", "Casualty", "Claims", "Insurance", "Assurance"]
    partners = []
    tiers = [("strategic", 0.12), ("national", 0.20), ("regional", 0.43), ("local", 0.25)]
    for i in range(1, ROW_COUNTS["insurance_partners"] + 1):
        tier = weighted_choice(rng, tiers)
        sensitivity_base = {"strategic": 30, "national": 45, "regional": 62, "local": 78}[tier]
        sensitivity = int(clamp(rng.gauss(sensitivity_base, 14), 8, 96))
        volume = int(clamp(rng.lognormvariate(5.2, 0.9), 8, 4_800))
        if tier == "strategic":
            volume = int(volume * 2.2)
        salvage_value = int(clamp(rng.gauss(12_500 - sensitivity * 55, 4_200), 1_100, 35_000))
        service = weighted_choice(rng, [("premium", 0.18), ("priority", 0.36), ("standard", 0.46)])
        contract = weighted_choice(
            rng,
            [("spot", 0.20), ("annual", 0.30), ("preferred_partner", 0.22), ("volume_based", 0.28)],
        )
        current_tow = money(clamp(170 + volume * 0.03 + salvage_value * 0.006 - sensitivity * 0.7, 75, 1_200))
        daily_rate = money(clamp(18 + salvage_value / 850 - sensitivity * 0.06, 10, 100))
        free_days = rng.choice([0, 0, 3, 3, 5, 7, 10, 14] if tier in {"strategic", "national"} else [0, 0, 3, 5, 7])
        partners.append(
            {
                "partner_id": f"P{i:03d}",
                "partner_name": f"{prefixes[(i - 1) % len(prefixes)]} {suffixes[(i + rng.randrange(len(suffixes))) % len(suffixes)]}",
                "partner_tier": tier,
                "monthly_claim_volume": volume,
                "avg_vehicle_salvage_value": salvage_value,
                "price_sensitivity_score": sensitivity,
                "service_level_requirement": service,
                "contract_type": contract,
                "current_tow_rate": current_tow,
                "current_daily_storage_rate": daily_rate,
                "free_storage_days": free_days,
                "historical_win_rate": pct(0.92 - sensitivity / 180 + rng.gauss(0, 0.06)),
                "target_margin": pct(0.18 + (100 - sensitivity) / 500 + rng.gauss(0, 0.03)),
                "relationship_score": int(clamp(95 - sensitivity * 0.45 + rng.gauss(0, 12), 20, 99)),
                "active_flag": 1 if rng.random() > 0.05 else 0,
            }
        )
    return partners


def generate_yard_locations(rng: random.Random) -> list[dict[str, object]]:
    rows = []
    slots_per_yard = ROW_COUNTS["yard_locations"] // len(YARDS)
    for yard in YARDS:
        for slot_idx in range(1, slots_per_yard + 1):
            zone_type, zone_prefix = ZONE_SEQUENCE[(slot_idx - 1) % len(ZONE_SEQUENCE)]
            profile = ZONE_PROFILES[zone_type]
            row_num = ((slot_idx - 1) // 25) + 1
            slot_num = ((slot_idx - 1) % 25) + 1
            distance = rng.randint(*profile["distance"])
            congestion = rng.randint(*profile["congestion"])
            access = rng.randint(*profile["access"])
            occupancy = 1 if rng.random() < {"fast_access": 0.92, "standard": 0.83, "overflow": 0.95, "heavy_vehicle": 0.70, "non_running": 0.80, "long_term_hold": 0.65}[zone_type] else 0
            rows.append(
                {
                    "yard_id": yard.yard_id,
                    "yard_name": yard.yard_name,
                    "region": yard.region,
                    "zone_id": zone_prefix,
                    "row_id": f"{zone_prefix}{row_num:02d}",
                    "slot_id": f"{zone_prefix}{row_num:02d}-{slot_num:03d}",
                    "zone_type": zone_type,
                    "distance_to_gate_meters": distance,
                    "distance_to_office_meters": max(20, distance + rng.randint(-160, 180)),
                    "distance_to_loading_area_meters": max(20, distance + rng.randint(-220, 220)),
                    "capacity": 1,
                    "current_occupancy": occupancy,
                    "occupancy_rate": f"{occupancy:.2f}",
                    "congestion_score": congestion,
                    "accessibility_score": access,
                    "equipment_required": profile["equipment"],
                    "surface_type": weighted_choice(rng, [("paved", 0.34), ("gravel", 0.36), ("dirt", 0.18), ("mixed", 0.12)]),
                    "indoor_flag": 1 if zone_type == "fast_access" and rng.random() < 0.08 else 0,
                    "active_flag": 1 if rng.random() > 0.02 else 0,
                }
            )
    return rows


def vehicle_type_for_model(make: str, model: str) -> str:
    if model in {"F-150", "Tacoma", "Silverado", "Frontier", "1500", "2500"}:
        return "pickup"
    if model in {"3500"}:
        return "heavy_vehicle"
    if model in {"RAV4", "Escape", "Explorer", "CR-V", "Pilot", "Equinox", "Tahoe", "X3", "X5", "Rogue", "Sorento", "Telluride", "Sportage"}:
        return "SUV"
    if model == "ProMaster":
        return "van"
    return "sedan"


def generate_vehicles(rng: random.Random, partners: list[dict[str, object]]) -> list[dict[str, object]]:
    partner_weights = [max(1, int(p["monthly_claim_volume"])) for p in partners]
    vehicles = []
    for i in range(1, ROW_COUNTS["vehicles"] + 1):
        partner = rng.choices(partners, weights=partner_weights, k=1)[0]
        yard = rng.choice(YARDS)
        make = rng.choice(list(MAKE_MODELS))
        model = rng.choice(MAKE_MODELS[make])
        model_year = rng.randint(2004, 2026)
        age = 2026 - model_year
        vehicle_type = vehicle_type_for_model(make, model)
        damage_type = weighted_choice(
            rng,
            [
                ("front_end", 0.22),
                ("rear_end", 0.14),
                ("side", 0.16),
                ("hail", 0.10),
                ("flood", 0.08),
                ("mechanical", 0.15),
                ("burn", 0.04),
                ("theft_recovery", 0.11),
            ],
        )
        severity = weighted_choice(rng, [("minor", 0.19), ("moderate", 0.43), ("severe", 0.27), ("total_loss", 0.11)])
        drivability = weighted_choice(
            rng,
            [
                ("runs_and_drives", 0.42),
                ("non_running", 0.28),
                ("forklift_required", 0.23),
                ("heavy_equipment_required", 0.07 if vehicle_type == "heavy_vehicle" else 0.02),
            ],
        )
        title_status = weighted_choice(rng, [("clean", 0.22), ("salvage", 0.45), ("rebuilt", 0.12), ("missing_title", 0.07), ("pending_title", 0.14)])
        complexity = int(
            clamp(
                {"runs_and_drives": 18, "non_running": 50, "forklift_required": 68, "heavy_equipment_required": 86}[drivability]
                + {"minor": 4, "moderate": 12, "severe": 20, "total_loss": 27}[severity]
                + rng.gauss(0, 9),
                0,
                100,
            )
        )
        partner_priority = int(clamp(100 - int(partner["price_sensitivity_score"]) * 0.45 + int(partner["relationship_score"]) * 0.45 + rng.gauss(0, 8), 0, 100))
        priority = round(clamp(partner_priority * 0.58 + (100 - complexity) * 0.18 + int(partner["avg_vehicle_salvage_value"]) / 650, 0, 100), 1)
        salvage_base = int(partner["avg_vehicle_salvage_value"]) * rng.uniform(0.45, 1.8)
        salvage = money(clamp(salvage_base - age * 290 - {"minor": 0, "moderate": 1_200, "severe": 3_600, "total_loss": 5_500}[severity], 500, 100_000))
        sale_probability = clamp(0.90 - age * 0.018 - complexity * 0.003 + salvage / 100_000 + rng.gauss(0, 0.08), 0.05, 0.98)
        expected_days = int(clamp(8 + age * 1.4 + complexity * 0.32 + rng.gauss(0, 8), 1, 180))
        arrival = BASE_DATE + timedelta(days=rng.randint(0, 210), hours=rng.randint(0, 8), minutes=rng.randint(0, 59))
        sold = rng.random() < sale_probability
        actual_days = int(clamp(expected_days + rng.gauss(0, 9), 1, 240)) if sold else ""
        sale_date = arrival + timedelta(days=actual_days) if sold else None
        pickup_required = 1 if rng.random() < 0.86 else 0
        picked_up = bool(sold and pickup_required and rng.random() < 0.62)
        pickup_date = sale_date + timedelta(days=rng.randint(1, 8)) if picked_up and sale_date else None
        status = (
            "picked_up"
            if picked_up
            else "sold_pending_pickup"
            if sold and pickup_required
            else weighted_choice(rng, [("awaiting_sale", 0.25), ("listed", 0.45), ("title_pending", 0.30)])
        )
        carrier_pickup = 1 if pickup_required and rng.random() < 0.55 else 0
        customer_pickup = 1 if pickup_required and not carrier_pickup else 0
        vehicles.append(
            {
                "vehicle_id": f"VEH{i:06d}",
                "claim_id": f"CLM{i:06d}",
                "partner_id": partner["partner_id"],
                "yard_id": yard.yard_id,
                "arrival_date": d(arrival),
                "sale_date": d(sale_date),
                "pickup_date": d(pickup_date),
                "vehicle_status": status,
                "make": make,
                "model": model,
                "model_year": model_year,
                "vehicle_age": age,
                "vehicle_type": vehicle_type,
                "damage_type": damage_type,
                "damage_severity": severity,
                "drivability_status": drivability,
                "title_status": title_status,
                "estimated_salvage_value": salvage,
                "estimated_sale_probability": pct(sale_probability),
                "expected_days_to_sale": expected_days,
                "actual_days_to_sale": actual_days,
                "pickup_required_flag": pickup_required,
                "customer_pickup_flag": customer_pickup,
                "carrier_pickup_flag": carrier_pickup,
                "partner_priority_score": partner_priority,
                "operational_complexity_score": complexity,
                "priority_score": priority,
                "created_at": dt(arrival + timedelta(hours=1)),
                "updated_at": dt(arrival + timedelta(days=rng.randint(1, 45), hours=rng.randint(0, 8))),
            }
        )
    return vehicles


def slot_for_vehicle(rng: random.Random, vehicle: dict[str, object], slots_by_yard: dict[str, list[dict[str, object]]], strategy: str = "priority_based") -> dict[str, object]:
    yard_slots = slots_by_yard[str(vehicle["yard_id"])]
    drivability = str(vehicle["drivability_status"])
    vehicle_type = str(vehicle["vehicle_type"])
    priority = float(vehicle["priority_score"])
    if strategy == "optimized" or (strategy == "priority_based" and priority >= 75):
        preferred = ["fast_access", "standard"]
    elif vehicle_type == "heavy_vehicle":
        preferred = ["heavy_vehicle"]
    elif drivability in {"forklift_required", "non_running"}:
        preferred = ["non_running", "standard"]
    elif drivability == "heavy_equipment_required":
        preferred = ["heavy_vehicle"]
    elif strategy == "random":
        preferred = list(ZONE_PROFILES)
    else:
        preferred = ["standard", "overflow", "long_term_hold"]
    candidates = [s for s in yard_slots if s["zone_type"] in preferred] or yard_slots
    return rng.choice(candidates)


def generate_location_history(rng: random.Random, vehicles: list[dict[str, object]], slots_by_yard: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows = []
    event_id = 1
    for vehicle in vehicles:
        if event_id > ROW_COUNTS["vehicle_location_history"]:
            break
        strategy = weighted_choice(rng, [("random", 0.10), ("first_available", 0.32), ("priority_based", 0.38), ("optimized", 0.20)])
        slot = slot_for_vehicle(rng, vehicle, slots_by_yard, strategy)
        arrival = datetime.strptime(str(vehicle["arrival_date"]), "%Y-%m-%d")
        rows.append(
            {
                "location_event_id": f"LOC{event_id:06d}",
                "vehicle_id": vehicle["vehicle_id"],
                "yard_id": vehicle["yard_id"],
                "assigned_zone_id": slot["zone_id"],
                "assigned_row_id": slot["row_id"],
                "assigned_slot_id": slot["slot_id"],
                "assignment_date": dt(arrival + timedelta(hours=rng.randint(1, 8), minutes=rng.randint(0, 59))),
                "relocation_count": 0,
                "relocated_flag": 0,
                "current_location_flag": 1,
                "initial_priority_score": vehicle["priority_score"],
                "final_priority_score": vehicle["priority_score"],
                "allocation_strategy": strategy,
                "assigned_by": weighted_choice(rng, [("system", 0.48), ("yard_manager", 0.38), ("simulation", 0.14)]),
                "assignment_reason": weighted_choice(
                    rng,
                    [("high_priority", 0.22), ("overflow_capacity", 0.20), ("special_equipment", 0.24), ("long_term_hold", 0.16), ("standard_storage", 0.18)],
                ),
            }
        )
        event_id += 1
    relocate_candidates = rng.sample(vehicles, ROW_COUNTS["vehicle_location_history"] - len(rows))
    for vehicle in relocate_candidates:
        slot = slot_for_vehicle(rng, vehicle, slots_by_yard, "optimized")
        arrival = datetime.strptime(str(vehicle["arrival_date"]), "%Y-%m-%d")
        new_priority = round(clamp(float(vehicle["priority_score"]) + rng.uniform(3, 14), 0, 100), 1)
        rows.append(
            {
                "location_event_id": f"LOC{event_id:06d}",
                "vehicle_id": vehicle["vehicle_id"],
                "yard_id": vehicle["yard_id"],
                "assigned_zone_id": slot["zone_id"],
                "assigned_row_id": slot["row_id"],
                "assigned_slot_id": slot["slot_id"],
                "assignment_date": dt(arrival + timedelta(days=rng.randint(3, 45), hours=rng.randint(1, 8))),
                "relocation_count": rng.randint(1, 3),
                "relocated_flag": 1,
                "current_location_flag": 1,
                "initial_priority_score": vehicle["priority_score"],
                "final_priority_score": new_priority,
                "allocation_strategy": "optimized",
                "assigned_by": weighted_choice(rng, [("system", 0.70), ("yard_manager", 0.25), ("simulation", 0.05)]),
                "assignment_reason": weighted_choice(rng, [("high_priority", 0.40), ("sold_pickup_staging", 0.34), ("special_equipment", 0.18), ("overflow_capacity", 0.08)]),
            }
        )
        event_id += 1
    return rows


def location_index(location_rows: list[dict[str, object]], yard_rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    slot_lookup = {(r["yard_id"], r["slot_id"]): r for r in yard_rows}
    current = {}
    for row in location_rows:
        if row["current_location_flag"] == 1:
            current[str(row["vehicle_id"])] = slot_lookup[(row["yard_id"], row["assigned_slot_id"])]
    return current


def generate_retrieval_events(rng: random.Random, vehicles: list[dict[str, object]], current_locations: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    eligible = [v for v in vehicles if int(v["pickup_required_flag"]) == 1]
    selected = rng.sample(eligible, ROW_COUNTS["retrieval_events"])
    rows = []
    for i, vehicle in enumerate(selected, 1):
        loc = current_locations[str(vehicle["vehicle_id"])]
        request_base = datetime.strptime(str(vehicle["arrival_date"]), "%Y-%m-%d") + timedelta(days=rng.randint(3, 75), hours=rng.randint(8, 16), minutes=rng.randint(0, 59))
        complexity = int(vehicle["operational_complexity_score"])
        blocked = int(clamp(rng.gauss(int(loc["congestion_score"]) / 15, 2), 0, 20))
        distance = int(loc["distance_to_gate_meters"]) + rng.randint(20, 360)
        equipment = str(loc["equipment_required"])
        if vehicle["drivability_status"] == "runs_and_drives" and equipment == "none":
            equipment = weighted_choice(rng, [("none", 0.88), ("jump_starter", 0.12)])
        elif vehicle["drivability_status"] == "heavy_equipment_required":
            equipment = "tow_truck"
        duration = clamp(5 + distance / 80 + blocked * 3.8 + complexity * 0.23 + rng.gauss(0, 6), 3, 180)
        start_delay = int(clamp(rng.gauss(8 + int(loc["congestion_score"]) / 5, 8), 0, 120))
        wait = duration + start_delay + rng.randint(4, 18)
        start = request_base + timedelta(minutes=start_delay)
        end = start + timedelta(minutes=duration)
        handoff = request_base + timedelta(minutes=wait)
        delay = 1 if wait > 45 or duration > 25 else 0
        rows.append(
            {
                "retrieval_id": f"RET{i:06d}",
                "vehicle_id": vehicle["vehicle_id"],
                "yard_id": vehicle["yard_id"],
                "request_time": dt(request_base),
                "retrieval_start_time": dt(start),
                "retrieval_end_time": dt(end),
                "handoff_time": dt(handoff),
                "requested_by": weighted_choice(rng, [("buyer", 0.35), ("carrier", 0.38), ("insurance_partner", 0.15), ("internal_ops", 0.12)]),
                "pickup_type": "carrier_pickup" if int(vehicle["carrier_pickup_flag"]) else weighted_choice(rng, [("customer_pickup", 0.70), ("internal_move", 0.18), ("auction_staging", 0.12)]),
                "retrieval_duration_minutes": f"{duration:.1f}",
                "wait_time_minutes": f"{wait:.1f}",
                "start_delay_minutes": start_delay,
                "travel_distance_meters": distance,
                "blocked_vehicle_count": blocked,
                "equipment_used": equipment,
                "staff_id": f"STF{rng.randint(1, 80):03d}",
                "retrieval_success_flag": 1 if rng.random() > 0.025 else 0,
                "delay_flag": delay,
                "delay_reason": "none" if not delay else weighted_choice(rng, [("blocked_access", 0.32), ("equipment_unavailable", 0.18), ("vehicle_not_found", 0.08), ("congestion", 0.26), ("weather", 0.10), ("title_issue", 0.06)]),
                "weather_condition": weighted_choice(rng, [("clear", 0.64), ("rain", 0.18), ("storm", 0.06), ("extreme_heat", 0.10), ("snow", 0.02)]),
                "time_of_day": weighted_choice(rng, [("morning", 0.32), ("midday", 0.28), ("afternoon", 0.34), ("evening", 0.06)]),
                "day_of_week": request_base.strftime("%A"),
            }
        )
    return rows


def generate_tow_events(rng: random.Random, vehicles: list[dict[str, object]], partner_by_id: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    cities = [("Plano", "75024"), ("Dallas", "75201"), ("Arlington", "76010"), ("Mesquite", "75149"), ("Houston", "77002"), ("Baytown", "77520"), ("Austin", "78701"), ("Round Rock", "78664"), ("Oklahoma City", "73102")]
    selected = rng.sample(vehicles, ROW_COUNTS["tow_events"])
    rows = []
    for i, vehicle in enumerate(selected, 1):
        partner = partner_by_id[str(vehicle["partner_id"])]
        city, zip_code = rng.choice(cities)
        distance = round(clamp(rng.lognormvariate(3.1, 0.75), 1, 500), 1)
        tow_type = "heavy_vehicle" if vehicle["vehicle_type"] == "heavy_vehicle" else weighted_choice(rng, [("standard", 0.55), ("long_distance", 0.18), ("after_hours", 0.12), ("priority", 0.15)])
        outsourced = 1 if distance > 70 or rng.random() < 0.18 else 0
        base = clamp(75 + distance * 3.1 + (220 if tow_type == "heavy_vehicle" else 0), 50, 1_000)
        fuel = clamp(distance * rng.uniform(0.55, 1.2), 0, 200)
        labor = clamp(35 + distance * 1.8 + (130 if tow_type == "heavy_vehicle" else 0), 20, 500)
        third_party = clamp(base + fuel + labor + rng.uniform(40, 240), 0, 1_500) if outsourced else 0
        internal_cost = money(third_party if outsourced else base + fuel + labor)
        quote = money(clamp(internal_cost * rng.uniform(1.12, 1.55), 75, 2_500))
        competitor = money(clamp(quote + rng.gauss(0, quote * 0.12), 50, 2_500))
        accepted_probability = clamp(0.75 - (quote - competitor) / 900 - int(partner["price_sensitivity_score"]) / 220, 0.05, 0.95)
        request = datetime.strptime(str(vehicle["arrival_date"]), "%Y-%m-%d") - timedelta(hours=rng.randint(2, 18))
        duration = clamp(distance / 18 + rng.uniform(1, 8) + (4 if tow_type == "heavy_vehicle" else 0), 0.5, 96)
        rows.append(
            {
                "tow_event_id": f"TOW{i:06d}",
                "claim_id": vehicle["claim_id"],
                "vehicle_id": vehicle["vehicle_id"],
                "partner_id": vehicle["partner_id"],
                "origin_zip": zip_code,
                "origin_city": city,
                "origin_state": "OK" if city == "Oklahoma City" else "TX",
                "yard_id": vehicle["yard_id"],
                "tow_distance_miles": f"{distance:.1f}",
                "tow_request_time": dt(request),
                "tow_completed_time": dt(request + timedelta(hours=duration)),
                "tow_duration_hours": f"{duration:.1f}",
                "tow_type": tow_type,
                "base_tow_cost": money(base),
                "fuel_surcharge": money(fuel),
                "labor_cost": money(labor),
                "third_party_tow_cost": money(third_party),
                "internal_total_tow_cost": internal_cost,
                "quoted_tow_price": quote,
                "accepted_flag": 1 if rng.random() < accepted_probability else 0,
                "competitor_estimated_price": competitor,
                "gross_tow_margin": quote - internal_cost,
                "outsourced_flag": outsourced,
            }
        )
    return rows


def generate_storage_events(rng: random.Random, vehicles: list[dict[str, object]], partner_by_id: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for i, vehicle in enumerate(vehicles[: ROW_COUNTS["yard_storage_events"]], 1):
        partner = partner_by_id[str(vehicle["partner_id"])]
        arrival = datetime.strptime(str(vehicle["arrival_date"]), "%Y-%m-%d")
        if vehicle["pickup_date"]:
            release = datetime.strptime(str(vehicle["pickup_date"]), "%Y-%m-%d")
            days = max(1, (release - arrival).days)
        else:
            days = int(clamp(int(vehicle["expected_days_to_sale"]) + rng.gauss(8, 20), 1, 365))
            release = None
        free_days = int(partner["free_storage_days"])
        billable = max(0, days - free_days)
        daily_rate = int(partner["current_daily_storage_rate"])
        fee = billable * daily_rate
        cost_per_day = money(clamp(5 + int(vehicle["operational_complexity_score"]) / 8 + rng.gauss(0, 2), 3, 40))
        total_cost = days * cost_per_day
        status = "collected" if release else weighted_choice(rng, [("billable", 0.55), ("waived", 0.10), ("disputed", 0.12), ("not_billable", 0.08), ("collected", 0.15)])
        rows.append(
            {
                "storage_event_id": f"STG{i:06d}",
                "vehicle_id": vehicle["vehicle_id"],
                "partner_id": vehicle["partner_id"],
                "yard_id": vehicle["yard_id"],
                "arrival_date": vehicle["arrival_date"],
                "release_date": d(release),
                "days_in_yard": days,
                "free_storage_days": free_days,
                "billable_storage_days": billable,
                "daily_storage_rate": daily_rate,
                "total_storage_fee": fee,
                "yard_cost_per_day": cost_per_day,
                "total_yard_cost": total_cost,
                "storage_margin": fee - total_cost,
                "capacity_utilization_at_arrival": f"{clamp(rng.gauss(0.82, 0.16), 0.20, 1.15):.2f}",
                "long_hold_flag": 1 if days > 35 else 0,
                "storage_billing_status": status,
            }
        )
    return rows


def generate_quotes(rng: random.Random, vehicles: list[dict[str, object]], partner_by_id: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    selected = rng.sample(vehicles, ROW_COUNTS["quote_outcomes"])
    rows = []
    for i, vehicle in enumerate(selected, 1):
        partner = partner_by_id[str(vehicle["partner_id"])]
        free_days = int(partner["free_storage_days"])
        expected_days = int(clamp(int(vehicle["expected_days_to_sale"]) + rng.gauss(5, 14), 1, 240))
        billable = max(0, expected_days - free_days)
        tow_price = money(clamp(int(partner["current_tow_rate"]) * rng.uniform(0.82, 1.35) + int(vehicle["operational_complexity_score"]) * 2.2, 75, 2_500))
        storage_rate = money(clamp(int(partner["current_daily_storage_rate"]) * rng.uniform(0.85, 1.25), 10, 100))
        total_cost = tow_price + billable * storage_rate
        salvage = int(vehicle["estimated_salvage_value"])
        competitor = money(clamp(total_cost + rng.gauss(0, total_cost * 0.12), 75, 15_000))
        price_gap = total_cost - competitor
        sensitivity = int(partner["price_sensitivity_score"])
        utilization = clamp(rng.gauss(0.82, 0.15), 0.20, 1.15)
        acceptance = clamp(
            0.82
            - sensitivity / 180
            - max(0, price_gap) / 2_800
            + int(partner["relationship_score"]) / 400
            + salvage / 140_000
            - max(0, utilization - 0.92) * 0.35,
            0.03,
            0.97,
        )
        accepted = 1 if rng.random() < acceptance else 0
        expected_internal_cost = tow_price * 0.66 + expected_days * (7 + int(vehicle["operational_complexity_score"]) / 12)
        expected_margin = money(total_cost - expected_internal_cost)
        recommended_tow = money(clamp(tow_price * (0.92 if sensitivity > 70 else 1.03), 75, 2_500))
        recommended_storage = money(clamp(storage_rate * (0.90 if sensitivity > 70 else 1.04), 10, 100))
        quote_date = datetime.strptime(str(vehicle["arrival_date"]), "%Y-%m-%d") - timedelta(days=rng.randint(0, 3))
        rows.append(
            {
                "quote_id": f"QTE{i:06d}",
                "partner_id": vehicle["partner_id"],
                "claim_id": vehicle["claim_id"],
                "vehicle_id": vehicle["vehicle_id"],
                "yard_id": vehicle["yard_id"],
                "quote_date": d(quote_date),
                "quoted_tow_price": tow_price,
                "quoted_daily_storage_rate": storage_rate,
                "free_storage_days": free_days,
                "expected_days_in_yard": expected_days,
                "expected_billable_storage_days": billable,
                "estimated_total_cost_to_partner": total_cost,
                "estimated_salvage_value": salvage,
                "net_expected_recovery": salvage - total_cost,
                "competitor_estimated_total_cost": competitor,
                "price_gap_vs_competitor": price_gap,
                "partner_price_sensitivity_score": sensitivity,
                "yard_capacity_utilization": f"{utilization:.2f}",
                "predicted_acceptance_probability": pct(acceptance),
                "accepted_flag": accepted,
                "lost_reason": "accepted" if accepted else weighted_choice(rng, [("price_too_high", 0.36), ("distance_too_far", 0.13), ("competitor_relationship", 0.19), ("storage_fee_too_high", 0.20), ("slow_pickup", 0.07), ("unknown", 0.05)]),
                "expected_margin": expected_margin,
                "recommended_tow_price": recommended_tow,
                "recommended_daily_storage_rate": recommended_storage,
                "pricing_strategy": weighted_choice(rng, [("margin_max", 0.20), ("acceptance_max", 0.22), ("balanced", 0.34), ("partner_retention", 0.14), ("capacity_control", 0.10)]),
            }
        )
    return rows


def generate_pricing_scenarios(rng: random.Random, quotes: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    per_quote = ROW_COUNTS["pricing_scenarios"] // len(quotes)
    scenario_id = 1
    for quote in quotes:
        best_id = None
        best_value = -1_000_000.0
        quote_rows = []
        for option in range(per_quote):
            tow_factor = 0.78 + option * (0.52 / max(1, per_quote - 1)) + rng.uniform(-0.015, 0.015)
            storage_factor = 0.80 + option * (0.45 / max(1, per_quote - 1)) + rng.uniform(-0.015, 0.015)
            tow_price = money(clamp(int(quote["quoted_tow_price"]) * tow_factor, 75, 2_500))
            storage_rate = money(clamp(int(quote["quoted_daily_storage_rate"]) * storage_factor, 10, 100))
            free_days = max(0, int(quote["free_storage_days"]) + rng.choice([-2, 0, 0, 2]))
            billable = max(0, int(quote["expected_days_in_yard"]) - free_days)
            total = tow_price + billable * storage_rate
            expected_revenue = money(total * float(quote["predicted_acceptance_probability"]))
            expected_cost = money(int(quote["quoted_tow_price"]) * 0.60 + int(quote["expected_days_in_yard"]) * rng.uniform(7, 18))
            margin = expected_revenue - expected_cost
            acceptance = clamp(float(quote["predicted_acceptance_probability"]) - (total - int(quote["estimated_total_cost_to_partner"])) / 4_500, 0.02, 0.98)
            value = round(acceptance * margin, 2)
            scenario = {
                "scenario_id": f"SCN{scenario_id:06d}",
                "quote_id": quote["quote_id"],
                "partner_id": quote["partner_id"],
                "vehicle_id": quote["vehicle_id"],
                "scenario_tow_price": tow_price,
                "scenario_daily_storage_rate": storage_rate,
                "scenario_free_storage_days": free_days,
                "scenario_total_partner_cost": total,
                "scenario_expected_revenue": expected_revenue,
                "scenario_expected_cost": expected_cost,
                "scenario_expected_margin": margin,
                "scenario_acceptance_probability": pct(acceptance),
                "scenario_expected_value": f"{value:.2f}",
                "meets_margin_threshold_flag": 1 if margin >= 100 else 0,
                "meets_acceptance_threshold_flag": 1 if acceptance >= 0.45 else 0,
                "recommended_flag": 0,
                "optimization_objective": weighted_choice(rng, [("maximize_expected_margin", 0.28), ("maximize_acceptance", 0.24), ("balanced_score", 0.48)]),
            }
            if value > best_value and margin >= 50:
                best_value = value
                best_id = scenario["scenario_id"]
            quote_rows.append(scenario)
            scenario_id += 1
        for scenario in quote_rows:
            scenario["recommended_flag"] = 1 if scenario["scenario_id"] == best_id else 0
        rows.extend(quote_rows)
    return rows[: ROW_COUNTS["pricing_scenarios"]]


def generate_allocation_scenarios(rng: random.Random, vehicles: list[dict[str, object]], slots_by_yard: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows = []
    strategies = ["random", "first_available", "priority_based", "optimized"]
    selected = vehicles[: ROW_COUNTS["yard_allocation_scenarios"] // len(strategies)]
    scenario_id = 1
    strategy_effect = {"random": 1.35, "first_available": 1.12, "priority_based": 0.94, "optimized": 0.82}
    for vehicle in selected:
        for strategy in strategies:
            slot = slot_for_vehicle(rng, vehicle, slots_by_yard, strategy)
            distance = int(slot["distance_to_gate_meters"]) + rng.randint(20, 260)
            blocked = int(clamp(rng.gauss(int(slot["congestion_score"]) / 18, 2), 0, 20))
            duration = clamp((5 + distance / 85 + blocked * 3.2 + int(vehicle["operational_complexity_score"]) * 0.18) * strategy_effect[strategy] + rng.gauss(0, 3), 3, 180)
            wait = clamp(duration + rng.gauss(10 + int(slot["congestion_score"]) / 6, 7), 5, 240)
            priority = float(vehicle["priority_score"])
            efficiency = int(clamp(100 - duration * 0.75 - blocked * 2 + int(slot["accessibility_score"]) * 0.35 + (8 if strategy == "optimized" else 0), 0, 100))
            rows.append(
                {
                    "allocation_scenario_id": f"ALC{scenario_id:06d}",
                    "simulation_run_id": f"RUN{1 + ((scenario_id - 1) // 10_000):03d}",
                    "vehicle_id": vehicle["vehicle_id"],
                    "yard_id": vehicle["yard_id"],
                    "allocation_strategy": strategy,
                    "assigned_zone_id": slot["zone_id"],
                    "assigned_slot_id": slot["slot_id"],
                    "vehicle_priority_score": vehicle["priority_score"],
                    "zone_accessibility_score": slot["accessibility_score"],
                    "simulated_retrieval_duration_minutes": f"{duration:.1f}",
                    "simulated_wait_time_minutes": f"{wait:.1f}",
                    "simulated_travel_distance_meters": distance,
                    "blocked_vehicle_count_estimate": blocked,
                    "high_priority_flag": 1 if priority >= 75 else 0,
                    "retrieval_under_15_min_flag": 1 if duration < 15 else 0,
                    "priority_weighted_time": f"{duration * priority / 100:.1f}",
                    "allocation_efficiency_score": efficiency,
                }
            )
            scenario_id += 1
    return rows


def validate(
    partners: list[dict[str, object]],
    yards: list[dict[str, object]],
    vehicles: list[dict[str, object]],
    locations: list[dict[str, object]],
    retrievals: list[dict[str, object]],
    tows: list[dict[str, object]],
    storage: list[dict[str, object]],
    quotes: list[dict[str, object]],
    pricing: list[dict[str, object]],
    allocations: list[dict[str, object]],
) -> None:
    partner_ids = {str(r["partner_id"]) for r in partners}
    yard_ids = {str(r["yard_id"]) for r in yards}
    vehicle_ids = {str(r["vehicle_id"]) for r in vehicles}
    quote_ids = {str(r["quote_id"]) for r in quotes}
    assert len(partner_ids) == ROW_COUNTS["insurance_partners"]
    assert len(vehicle_ids) == ROW_COUNTS["vehicles"]
    for table_name, rows in {
        "vehicles": vehicles,
        "tow_events": tows,
        "yard_storage_events": storage,
        "quote_outcomes": quotes,
        "pricing_scenarios": pricing,
    }.items():
        if rows and "partner_id" in rows[0]:
            assert {str(r["partner_id"]) for r in rows} <= partner_ids, table_name
    for table_name, rows in {
        "vehicle_location_history": locations,
        "retrieval_events": retrievals,
        "tow_events": tows,
        "yard_storage_events": storage,
        "quote_outcomes": quotes,
        "pricing_scenarios": pricing,
        "yard_allocation_scenarios": allocations,
    }.items():
        assert {str(r["vehicle_id"]) for r in rows} <= vehicle_ids, table_name
    for table_name, rows in {
        "vehicles": vehicles,
        "vehicle_location_history": locations,
        "retrieval_events": retrievals,
        "tow_events": tows,
        "yard_storage_events": storage,
        "quote_outcomes": quotes,
        "yard_allocation_scenarios": allocations,
    }.items():
        assert {str(r["yard_id"]) for r in rows} <= yard_ids, table_name
    assert {str(r["quote_id"]) for r in pricing} <= quote_ids
    assert any(int(r["accepted_flag"]) == 1 for r in quotes)
    assert any(int(r["accepted_flag"]) == 0 for r in quotes)
    assert any(int(r["delay_flag"]) == 1 for r in retrievals)
    assert any(int(r["retrieval_under_15_min_flag"]) == 1 for r in allocations)


def main() -> None:
    rng = random.Random(SEED)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    partners = generate_partners(rng)
    yards = generate_yard_locations(rng)
    vehicles = generate_vehicles(rng, partners)
    slots_by_yard: dict[str, list[dict[str, object]]] = {}
    for slot in yards:
        slots_by_yard.setdefault(str(slot["yard_id"]), []).append(slot)
    locations = generate_location_history(rng, vehicles, slots_by_yard)
    current_locations = location_index(locations, yards)
    retrievals = generate_retrieval_events(rng, vehicles, current_locations)
    partner_by_id = {str(p["partner_id"]): p for p in partners}
    tows = generate_tow_events(rng, vehicles, partner_by_id)
    storage = generate_storage_events(rng, vehicles, partner_by_id)
    quotes = generate_quotes(rng, vehicles, partner_by_id)
    pricing = generate_pricing_scenarios(rng, quotes)
    allocations = generate_allocation_scenarios(rng, vehicles, slots_by_yard)

    validate(partners, yards, vehicles, locations, retrievals, tows, storage, quotes, pricing, allocations)

    tables = [
        ("insurance_partners", PARTNER_COLUMNS, partners),
        ("yard_locations", YARD_COLUMNS, yards),
        ("vehicles", VEHICLE_COLUMNS, vehicles),
        ("vehicle_location_history", LOCATION_HISTORY_COLUMNS, locations),
        ("retrieval_events", RETRIEVAL_COLUMNS, retrievals),
        ("tow_events", PARTNER_EVENT_COLUMNS, tows),
        ("yard_storage_events", STORAGE_COLUMNS, storage),
        ("quote_outcomes", QUOTE_COLUMNS, quotes),
        ("pricing_scenarios", PRICING_SCENARIO_COLUMNS, pricing),
        ("yard_allocation_scenarios", ALLOCATION_COLUMNS, allocations),
    ]
    for name, columns, rows in tables:
        write_csv(RAW_DIR / f"{name}.csv", columns, rows)
        print(f"{name}: {len(rows):,} rows")
    print(f"Wrote raw CSVs to {RAW_DIR}")


if __name__ == "__main__":
    main()
