# YardOps Intelligence Mock Data Table Requirements

This document defines the mock data requirements for the **YardOps Intelligence** analytics project.

The project simulates two connected operational analytics problems:

1. **Yard allocation optimization**: placing vehicles in yard zones to reduce retrieval time and improve operational efficiency.
2. **Tow and yard pricing optimization**: optimizing tow and storage pricing for insurance partners while balancing acceptance probability, partner value, and margin.

The tables below are designed for synthetic data generation. Numeric ranges are suggested realistic ranges for simulation purposes. Some outliers are acceptable, especially to make the analytics more realistic.

---

## 1. `vehicles`

Core vehicle-level table. Each row represents one vehicle entering a Copart-style salvage yard.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `vehicle_id` | Unique vehicle identifier. | `VEH000001`, `VEH102938` | String, unique |
| `claim_id` | Mock insurance claim ID associated with the vehicle. | `CLM000493`, `CLM827331` | String, mostly unique but can repeat if needed |
| `partner_id` | Insurance partner or seller that sent the vehicle. | `P001`, `P024` | Foreign key to `insurance_partners.partner_id` |
| `yard_id` | Yard where the vehicle is stored. | `YARD_DAL_01`, `YARD_HOU_02` | Foreign key to `yard_locations.yard_id` |
| `arrival_date` | Date the vehicle arrived at the yard. | `2025-01-14`, `2025-09-03` | Date |
| `sale_date` | Date the vehicle was sold. | `2025-01-28`, `2025-10-11` | Date, can be null if unsold |
| `pickup_date` | Date the vehicle was picked up after sale or assignment. | `2025-02-01`, `2025-10-14` | Date, can be null |
| `vehicle_status` | Current lifecycle status. | `awaiting_sale`, `listed`, `sold_pending_pickup`, `picked_up`, `title_pending` | Categorical |
| `make` | Vehicle manufacturer. | `Toyota`, `Ford`, `Honda`, `Chevrolet`, `BMW` | Categorical |
| `model` | Vehicle model. | `Camry`, `F-150`, `Civic`, `Silverado`, `3 Series` | Categorical |
| `model_year` | Vehicle model year. | `2018`, `2021`, `2014` | 2000-2026, occasional older outliers acceptable |
| `vehicle_age` | Age of vehicle at time of arrival. | `5`, `9`, `13` | 0-25 years, occasional 30+ outliers acceptable |
| `vehicle_type` | Broad vehicle category. | `sedan`, `SUV`, `pickup`, `van`, `motorcycle`, `heavy_vehicle` | Categorical |
| `damage_type` | Primary damage category. | `front_end`, `rear_end`, `side`, `hail`, `flood`, `mechanical`, `burn`, `theft_recovery` | Categorical |
| `damage_severity` | Severity of damage. | `minor`, `moderate`, `severe`, `total_loss` | Categorical or ordinal |
| `drivability_status` | Whether and how the vehicle can move. | `runs_and_drives`, `non_running`, `forklift_required`, `heavy_equipment_required` | Categorical |
| `title_status` | Vehicle title condition. | `clean`, `salvage`, `rebuilt`, `missing_title`, `pending_title` | Categorical |
| `estimated_salvage_value` | Estimated resale or salvage value. | `8500`, `3200`, `15750` | $500-$45,000, high-end outliers up to $100,000 acceptable |
| `estimated_sale_probability` | Probability that the vehicle sells within target window. | `0.72`, `0.41`, `0.88` | 0.00-1.00 |
| `expected_days_to_sale` | Predicted number of days from arrival to sale. | `8`, `21`, `45` | 1-90 days, outliers up to 180 acceptable |
| `actual_days_to_sale` | Actual days from arrival to sale. | `10`, `34`, `NULL` | 1-120 days, null if unsold, outliers up to 240 acceptable |
| `pickup_required_flag` | Whether the vehicle requires retrieval/pickup. | `1`, `0` | Binary |
| `customer_pickup_flag` | Whether pickup is handled by buyer/customer. | `1`, `0` | Binary |
| `carrier_pickup_flag` | Whether pickup is handled by a transport carrier. | `1`, `0` | Binary |
| `partner_priority_score` | Priority score based on insurance partner value or SLA. | `82`, `55`, `94` | 0-100 |
| `operational_complexity_score` | Score representing retrieval/storage difficulty. | `15`, `60`, `88` | 0-100 |
| `priority_score` | Composite score used for yard placement decision. | `76.4`, `42.9`, `91.2` | 0-100 |
| `created_at` | Record creation timestamp for mock pipeline. | `2025-01-14 09:32:00` | Timestamp |
| `updated_at` | Record update timestamp. | `2025-01-20 16:45:00` | Timestamp |

---

## 2. `yard_locations`

Yard layout table. Each row can represent a zone, row, or slot depending on desired granularity. For simulation, one row per slot is ideal.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `yard_id` | Yard identifier. | `YARD_DAL_01`, `YARD_AUS_01` | String |
| `yard_name` | Human-readable yard name. | `Dallas North Yard`, `Austin Central Yard` | String |
| `region` | Geographic region. | `Texas`, `Southwest`, `Midwest` | Categorical |
| `zone_id` | Yard zone identifier. | `A`, `B`, `C`, `FAST_ACCESS`, `OVERFLOW` | String |
| `row_id` | Row identifier within the zone. | `A01`, `B12`, `OF03` | String |
| `slot_id` | Specific slot identifier. | `A01-034`, `B12-118` | String, unique within yard |
| `zone_type` | Operational zone type. | `fast_access`, `standard`, `overflow`, `heavy_vehicle`, `non_running`, `long_term_hold` | Categorical |
| `distance_to_gate_meters` | Distance from slot/zone to customer pickup gate. | `85`, `420`, `980` | 20-1,500 meters, outliers up to 2,500 acceptable |
| `distance_to_office_meters` | Distance from slot/zone to office/check-in. | `60`, `380`, `750` | 20-1,500 meters |
| `distance_to_loading_area_meters` | Distance from slot/zone to carrier loading area. | `120`, `300`, `900` | 20-1,500 meters |
| `capacity` | Capacity of the zone/row. If row is slot-level, use `1`. | `1`, `80`, `250` | 1 if slot-level, 20-500 if zone-level |
| `current_occupancy` | Number of occupied spaces in the zone/row. | `1`, `64`, `221` | 0 to `capacity` |
| `occupancy_rate` | Current occupancy divided by capacity. | `0.72`, `0.91`, `0.43` | 0.00-1.00, slight >1 outliers acceptable for overcapacity simulation |
| `congestion_score` | Operational congestion level. | `22`, `68`, `91` | 0-100 |
| `accessibility_score` | Ease of retrieving vehicles from this location. | `95`, `62`, `28` | 0-100, higher means easier access |
| `equipment_required` | Equipment typically required to retrieve from zone. | `none`, `forklift`, `loader`, `heavy_tow` | Categorical |
| `surface_type` | Yard surface type. | `paved`, `gravel`, `dirt`, `mixed` | Categorical |
| `indoor_flag` | Whether the location is covered/indoor. | `1`, `0` | Binary |
| `active_flag` | Whether the slot/zone is currently usable. | `1`, `0` | Binary |

---

## 3. `vehicle_location_history`

Tracks vehicle placement and relocation. Each row represents one location assignment event for a vehicle.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `location_event_id` | Unique location history event ID. | `LOC000001`, `LOC982133` | String, unique |
| `vehicle_id` | Vehicle assigned to location. | `VEH000001` | Foreign key to `vehicles.vehicle_id` |
| `yard_id` | Yard where the vehicle is located. | `YARD_DAL_01` | Foreign key |
| `assigned_zone_id` | Assigned yard zone. | `A`, `B`, `OVERFLOW` | Foreign key-like value |
| `assigned_row_id` | Assigned row. | `A01`, `B05` | String |
| `assigned_slot_id` | Assigned slot. | `A01-034`, `B05-211` | String |
| `assignment_date` | Date/time vehicle was assigned to location. | `2025-01-14 13:10:00` | Timestamp |
| `relocation_count` | Number of times the vehicle has been moved. | `0`, `1`, `3` | 0-5, outliers up to 10 acceptable |
| `relocated_flag` | Whether this event represents a relocation. | `1`, `0` | Binary |
| `current_location_flag` | Whether this is the current location. | `1`, `0` | Binary |
| `initial_priority_score` | Priority score when vehicle first arrived. | `71.5`, `39.2` | 0-100 |
| `final_priority_score` | Updated score after status/sale changes. | `83.1`, `44.8` | 0-100 |
| `allocation_strategy` | Strategy used to assign the vehicle. | `random`, `first_available`, `priority_based`, `optimized` | Categorical |
| `assigned_by` | System/user that assigned the location. | `system`, `yard_manager`, `simulation` | Categorical |
| `assignment_reason` | Reason for placement. | `high_priority`, `overflow_capacity`, `special_equipment`, `long_term_hold` | Categorical |

---

## 4. `retrieval_events`

Operational event table. Each row represents one vehicle retrieval request from the yard.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `retrieval_id` | Unique retrieval event ID. | `RET000001`, `RET873212` | String, unique |
| `vehicle_id` | Vehicle being retrieved. | `VEH000001` | Foreign key to `vehicles.vehicle_id` |
| `yard_id` | Yard where retrieval happened. | `YARD_DAL_01` | Foreign key |
| `request_time` | Time retrieval was requested. | `2025-02-01 10:05:00` | Timestamp |
| `retrieval_start_time` | Time staff started retrieval. | `2025-02-01 10:12:00` | Timestamp |
| `retrieval_end_time` | Time vehicle reached handoff/loading area. | `2025-02-01 10:31:00` | Timestamp |
| `handoff_time` | Time vehicle was handed off to buyer/carrier. | `2025-02-01 10:42:00` | Timestamp |
| `requested_by` | Who requested retrieval. | `buyer`, `carrier`, `insurance_partner`, `internal_ops` | Categorical |
| `pickup_type` | Type of pickup. | `customer_pickup`, `carrier_pickup`, `internal_move`, `auction_staging` | Categorical |
| `retrieval_duration_minutes` | Time from retrieval start to retrieval end. | `12.5`, `28.0`, `54.2` | 3-90 minutes, outliers up to 180 acceptable |
| `wait_time_minutes` | Time from request to handoff. | `22.0`, `45.5`, `96.0` | 5-120 minutes, outliers up to 240 acceptable |
| `start_delay_minutes` | Time from request to retrieval start. | `4`, `12`, `35` | 0-60 minutes, outliers up to 120 acceptable |
| `travel_distance_meters` | Estimated staff/equipment travel distance. | `180`, `780`, `1450` | 50-3,000 meters, outliers up to 5,000 acceptable |
| `blocked_vehicle_count` | Number of vehicles blocking retrieval path. | `0`, `2`, `7` | 0-12, outliers up to 20 acceptable |
| `equipment_used` | Equipment used during retrieval. | `none`, `forklift`, `loader`, `tow_truck`, `jump_starter` | Categorical |
| `staff_id` | Mock staff member assigned. | `STF001`, `STF044` | String |
| `retrieval_success_flag` | Whether retrieval completed successfully. | `1`, `0` | Binary |
| `delay_flag` | Whether retrieval exceeded target threshold. | `1`, `0` | Binary |
| `delay_reason` | Primary reason for delay. | `blocked_access`, `equipment_unavailable`, `vehicle_not_found`, `congestion`, `weather`, `title_issue`, `none` | Categorical |
| `weather_condition` | Weather during retrieval. | `clear`, `rain`, `storm`, `extreme_heat`, `snow` | Categorical |
| `time_of_day` | Time bucket. | `morning`, `midday`, `afternoon`, `evening` | Categorical |
| `day_of_week` | Day of week. | `Monday`, `Friday` | Categorical |

---

## 5. `insurance_partners`

Partner-level table. Each row represents one mock insurance company or seller partner.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `partner_id` | Unique partner identifier. | `P001`, `P024` | String, unique |
| `partner_name` | Mock partner name. | `NorthStar Insurance`, `Pioneer Mutual`, `MetroGuard Claims` | String |
| `partner_tier` | Strategic importance tier. | `national`, `regional`, `local`, `strategic` | Categorical |
| `monthly_claim_volume` | Average monthly vehicle assignment volume. | `45`, `320`, `1200` | 5-2,000, outliers up to 5,000 acceptable |
| `avg_vehicle_salvage_value` | Average salvage value of vehicles from partner. | `6200`, `9800`, `14200` | $1,000-$35,000 |
| `price_sensitivity_score` | Estimated sensitivity to tow/storage pricing. | `20`, `75`, `92` | 0-100, higher means more price sensitive |
| `service_level_requirement` | Required service level. | `standard`, `priority`, `premium` | Categorical |
| `contract_type` | Commercial agreement type. | `spot`, `annual`, `preferred_partner`, `volume_based` | Categorical |
| `current_tow_rate` | Current standard tow price charged to partner. | `175`, `240`, `325` | $75-$600, outliers up to $1,200 for long/heavy tows |
| `current_daily_storage_rate` | Current daily yard storage rate. | `25`, `35`, `50` | $10-$100 per day |
| `free_storage_days` | Number of free storage days included. | `0`, `3`, `7` | 0-14 days, outliers up to 30 acceptable |
| `historical_win_rate` | Share of prior assignments won/accepted. | `0.58`, `0.74`, `0.91` | 0.00-1.00 |
| `target_margin` | Target gross margin percentage or dollars depending on design. | `0.22`, `0.35` | If percentage: 0.05-0.50 |
| `relationship_score` | Relationship strength with partner. | `40`, `78`, `95` | 0-100 |
| `active_flag` | Whether partner is active. | `1`, `0` | Binary |

---

## 6. `tow_events`

Tow transaction table. Each row represents one vehicle tow from an origin location to a yard.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `tow_event_id` | Unique tow event ID. | `TOW000001`, `TOW347812` | String, unique |
| `claim_id` | Claim associated with tow. | `CLM000493` | Foreign key-like value |
| `vehicle_id` | Vehicle being towed. | `VEH000001` | Foreign key to `vehicles.vehicle_id` |
| `partner_id` | Insurance partner requesting tow. | `P001` | Foreign key to `insurance_partners.partner_id` |
| `origin_zip` | ZIP code where vehicle is picked up. | `75024`, `75201`, `76010` | String |
| `origin_city` | City where tow begins. | `Plano`, `Dallas`, `Arlington` | String |
| `origin_state` | State where tow begins. | `TX`, `OK`, `LA` | String |
| `yard_id` | Destination yard. | `YARD_DAL_01` | Foreign key |
| `tow_distance_miles` | Distance from origin to yard. | `12.4`, `38.0`, `112.7` | 1-250 miles, outliers up to 500 acceptable |
| `tow_request_time` | Time tow was requested. | `2025-03-04 08:20:00` | Timestamp |
| `tow_completed_time` | Time tow was completed. | `2025-03-04 12:40:00` | Timestamp |
| `tow_duration_hours` | Time from request to completion. | `2.5`, `6.0`, `18.5` | 0.5-48 hours, outliers up to 96 acceptable |
| `tow_type` | Tow category. | `standard`, `long_distance`, `heavy_vehicle`, `after_hours`, `priority` | Categorical |
| `base_tow_cost` | Internal base tow cost. | `95`, `180`, `420` | $50-$1,000 |
| `fuel_surcharge` | Fuel-related surcharge cost. | `12`, `35`, `80` | $0-$200 |
| `labor_cost` | Labor cost estimate. | `45`, `90`, `220` | $20-$500 |
| `third_party_tow_cost` | Cost paid to third-party tow provider, if outsourced. | `0`, `210`, `640` | $0-$1,500 |
| `internal_total_tow_cost` | Total internal/outsourced tow cost. | `165`, `390`, `870` | $50-$2,000 |
| `quoted_tow_price` | Price quoted to partner. | `225`, `475`, `1100` | $75-$2,500 |
| `accepted_flag` | Whether the tow quote was accepted. | `1`, `0` | Binary |
| `competitor_estimated_price` | Estimated competing tow price. | `200`, `430`, `950` | $50-$2,500 |
| `gross_tow_margin` | Tow revenue minus tow cost. | `60`, `85`, `230` | Can be negative; typical -$200 to $1,000 |
| `outsourced_flag` | Whether tow was outsourced. | `1`, `0` | Binary |

---

## 7. `yard_storage_events`

Storage economics table. Each row represents the storage period and fee/margin outcome for a vehicle.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `storage_event_id` | Unique storage event ID. | `STG000001`, `STG928301` | String, unique |
| `vehicle_id` | Vehicle stored. | `VEH000001` | Foreign key to `vehicles.vehicle_id` |
| `partner_id` | Partner associated with vehicle. | `P001` | Foreign key |
| `yard_id` | Yard where vehicle is stored. | `YARD_DAL_01` | Foreign key |
| `arrival_date` | Date vehicle arrived at yard. | `2025-01-14` | Date |
| `release_date` | Date vehicle left yard. | `2025-02-08` | Date, can be null if still present |
| `days_in_yard` | Total days stored. | `12`, `38`, `91` | 1-120 days, outliers up to 365 acceptable |
| `free_storage_days` | Free days before billing starts. | `0`, `3`, `7` | 0-14 days, outliers up to 30 acceptable |
| `billable_storage_days` | Storage days billed to partner. | `5`, `22`, `74` | 0 to `days_in_yard` |
| `daily_storage_rate` | Daily storage price charged. | `25`, `35`, `50` | $10-$100 per day |
| `total_storage_fee` | Total storage revenue. | `125`, `770`, `3700` | $0-$10,000, high outliers acceptable |
| `yard_cost_per_day` | Estimated internal yard cost per vehicle per day. | `6`, `12`, `22` | $3-$40 |
| `total_yard_cost` | Total internal yard storage cost. | `72`, `456`, `2002` | $3-$10,000 |
| `storage_margin` | Storage revenue minus yard storage cost. | `53`, `314`, `1698` | Can be negative; typical -$500 to $5,000 |
| `capacity_utilization_at_arrival` | Yard utilization when vehicle arrived. | `0.68`, `0.91`, `1.03` | 0.20-1.00, outliers up to 1.15 for overcapacity |
| `long_hold_flag` | Whether the vehicle stayed longer than target. | `1`, `0` | Binary |
| `storage_billing_status` | Billing status. | `not_billable`, `billable`, `waived`, `disputed`, `collected` | Categorical |

---

## 8. `quote_outcomes`

Pricing quote outcome table. Each row represents a tow/storage pricing quote offered to a partner.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `quote_id` | Unique quote identifier. | `QTE000001`, `QTE782311` | String, unique |
| `partner_id` | Partner receiving the quote. | `P001` | Foreign key to `insurance_partners.partner_id` |
| `claim_id` | Claim related to the quote. | `CLM000493` | String |
| `vehicle_id` | Vehicle related to the quote. | `VEH000001` | Foreign key to `vehicles.vehicle_id` |
| `yard_id` | Yard proposed for tow/storage. | `YARD_DAL_01` | Foreign key |
| `quote_date` | Date quote was generated. | `2025-03-04` | Date |
| `quoted_tow_price` | Tow price quoted to partner. | `225`, `475`, `900` | $75-$2,500 |
| `quoted_daily_storage_rate` | Daily storage rate quoted to partner. | `25`, `35`, `55` | $10-$100 per day |
| `free_storage_days` | Free days included in offer. | `0`, `3`, `7` | 0-14 days, outliers up to 30 acceptable |
| `expected_days_in_yard` | Expected total days in yard. | `14`, `35`, `72` | 1-120 days, outliers up to 240 acceptable |
| `expected_billable_storage_days` | Expected billable days after free period. | `7`, `28`, `65` | 0 to `expected_days_in_yard` |
| `estimated_total_cost_to_partner` | Tow plus expected billable storage cost. | `400`, `1455`, `3200` | $75-$15,000 |
| `estimated_salvage_value` | Expected salvage value of the vehicle. | `6200`, `12800`, `2800` | $500-$45,000, outliers up to $100,000 acceptable |
| `net_expected_recovery` | Estimated salvage value minus total partner cost. | `5800`, `11345`, `-400` | Can be negative; typical -$5,000 to $100,000 |
| `competitor_estimated_total_cost` | Estimated competitor tow plus storage cost. | `375`, `1320`, `3500` | $75-$15,000 |
| `price_gap_vs_competitor` | Quote cost minus competitor cost. | `25`, `135`, `-300` | Can be negative; typical -$2,000 to $2,000 |
| `partner_price_sensitivity_score` | Partner price sensitivity at quote time. | `22`, `74`, `91` | 0-100 |
| `yard_capacity_utilization` | Yard utilization at time of quote. | `0.62`, `0.87`, `1.04` | 0.20-1.00, outliers up to 1.15 |
| `predicted_acceptance_probability` | Model-estimated probability of quote acceptance. | `0.72`, `0.38`, `0.91` | 0.00-1.00 |
| `accepted_flag` | Whether partner accepted quote. | `1`, `0` | Binary |
| `lost_reason` | Reason for rejected quote. | `price_too_high`, `distance_too_far`, `competitor_relationship`, `storage_fee_too_high`, `slow_pickup`, `unknown`, `accepted` | Categorical |
| `expected_margin` | Expected margin if quote is accepted. | `85`, `350`, `-50` | Can be negative; typical -$500 to $3,000 |
| `recommended_tow_price` | Optimizer-recommended tow price. | `210`, `450`, `850` | $75-$2,500 |
| `recommended_daily_storage_rate` | Optimizer-recommended daily storage rate. | `22`, `32`, `48` | $10-$100 |
| `pricing_strategy` | Strategy used for quote. | `margin_max`, `acceptance_max`, `balanced`, `partner_retention`, `capacity_control` | Categorical |

---

## 9. `pricing_scenarios`

Optional table used for the pricing optimizer. Each row represents one possible tow/storage pricing combination tested for a quote.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `scenario_id` | Unique scenario identifier. | `SCN000001`, `SCN673211` | String, unique |
| `quote_id` | Quote associated with scenario. | `QTE000001` | Foreign key to `quote_outcomes.quote_id` |
| `partner_id` | Partner for the pricing scenario. | `P001` | Foreign key |
| `vehicle_id` | Vehicle related to scenario. | `VEH000001` | Foreign key |
| `scenario_tow_price` | Candidate tow price. | `175`, `225`, `275` | $75-$2,500 |
| `scenario_daily_storage_rate` | Candidate daily storage rate. | `20`, `30`, `40` | $10-$100 |
| `scenario_free_storage_days` | Candidate free storage period. | `0`, `3`, `7` | 0-14 days |
| `scenario_total_partner_cost` | Expected partner cost under scenario. | `450`, `1100`, `2800` | $75-$15,000 |
| `scenario_expected_revenue` | Expected revenue under scenario. | `420`, `980`, `2400` | $0-$15,000 |
| `scenario_expected_cost` | Expected internal cost under scenario. | `260`, `610`, `1750` | $0-$10,000 |
| `scenario_expected_margin` | Expected revenue minus expected cost. | `160`, `370`, `650` | Can be negative; typical -$500 to $5,000 |
| `scenario_acceptance_probability` | Estimated acceptance probability for scenario. | `0.81`, `0.64`, `0.42` | 0.00-1.00 |
| `scenario_expected_value` | Acceptance probability multiplied by expected margin or selected objective. | `129.6`, `236.8`, `273.0` | Can be negative; depends on objective |
| `meets_margin_threshold_flag` | Whether scenario meets minimum margin rule. | `1`, `0` | Binary |
| `meets_acceptance_threshold_flag` | Whether scenario meets minimum acceptance rule. | `1`, `0` | Binary |
| `recommended_flag` | Whether scenario is selected by optimizer. | `1`, `0` | Binary |
| `optimization_objective` | Objective used to choose scenario. | `maximize_expected_margin`, `maximize_acceptance`, `balanced_score` | Categorical |

---

## 10. `yard_allocation_scenarios`

Optional simulation table used for comparing yard allocation strategies.

| Column | Description | Example Values | Suggested Range / Notes |
|---|---|---|---|
| `allocation_scenario_id` | Unique allocation scenario ID. | `ALC000001`, `ALC762812` | String, unique |
| `simulation_run_id` | Simulation run identifier. | `RUN001`, `RUN025` | String |
| `vehicle_id` | Vehicle assigned in simulation. | `VEH000001` | Foreign key |
| `yard_id` | Yard used in simulation. | `YARD_DAL_01` | Foreign key |
| `allocation_strategy` | Strategy being tested. | `random`, `first_available`, `priority_based`, `optimized` | Categorical |
| `assigned_zone_id` | Zone assigned by scenario. | `A`, `B`, `OVERFLOW` | String |
| `assigned_slot_id` | Slot assigned by scenario. | `A01-034`, `C05-220` | String |
| `vehicle_priority_score` | Priority score used for assignment. | `84.5`, `39.2` | 0-100 |
| `zone_accessibility_score` | Accessibility of assigned zone. | `92`, `55`, `21` | 0-100 |
| `simulated_retrieval_duration_minutes` | Simulated retrieval time under scenario. | `11.5`, `28.3`, `63.0` | 3-90 minutes, outliers up to 180 acceptable |
| `simulated_wait_time_minutes` | Simulated request-to-handoff wait time. | `20.5`, `44.0`, `102.0` | 5-120 minutes, outliers up to 240 acceptable |
| `simulated_travel_distance_meters` | Simulated yard travel distance. | `160`, `740`, `1800` | 50-3,000 meters, outliers up to 5,000 acceptable |
| `blocked_vehicle_count_estimate` | Estimated vehicles blocking access. | `0`, `3`, `9` | 0-12, outliers up to 20 acceptable |
| `high_priority_flag` | Whether vehicle is high-priority. | `1`, `0` | Binary |
| `retrieval_under_15_min_flag` | Whether simulated retrieval time is under 15 minutes. | `1`, `0` | Binary |
| `priority_weighted_time` | Retrieval time weighted by vehicle priority. | `8.4`, `35.2`, `72.9` | 0-200+ depending on formula |
| `allocation_efficiency_score` | Overall assignment quality score. | `88`, `61`, `34` | 0-100 |

---

# Recommended Data Volumes

For a realistic but manageable project:

| Table | Recommended Rows |
|---|---:|
| `vehicles` | 50,000 |
| `yard_locations` | 8,000-16,000 slot-level rows |
| `vehicle_location_history` | 50,000-75,000 |
| `retrieval_events` | 25,000-40,000 |
| `insurance_partners` | 40-80 |
| `tow_events` | 20,000-40,000 |
| `yard_storage_events` | 40,000-50,000 |
| `quote_outcomes` | 20,000-40,000 |
| `pricing_scenarios` | 200,000-1,000,000 if testing many price combinations |
| `yard_allocation_scenarios` | 150,000-300,000 if testing multiple strategies |

For the first MVP, use smaller samples:

| Table | MVP Rows |
|---|---:|
| `vehicles` | 10,000 |
| `yard_locations` | 2,000 |
| `retrieval_events` | 5,000 |
| `insurance_partners` | 40 |
| `quote_outcomes` | 5,000 |
| `pricing_scenarios` | 50,000 |
| `yard_allocation_scenarios` | 30,000 |

---

# Suggested Relationships Between Tables

| Parent Table | Child Table | Join Key |
|---|---|---|
| `vehicles` | `retrieval_events` | `vehicle_id` |
| `vehicles` | `vehicle_location_history` | `vehicle_id` |
| `vehicles` | `tow_events` | `vehicle_id` |
| `vehicles` | `yard_storage_events` | `vehicle_id` |
| `vehicles` | `quote_outcomes` | `vehicle_id` |
| `insurance_partners` | `vehicles` | `partner_id` |
| `insurance_partners` | `quote_outcomes` | `partner_id` |
| `insurance_partners` | `tow_events` | `partner_id` |
| `yard_locations` | `vehicles` | `yard_id` |
| `yard_locations` | `retrieval_events` | `yard_id` |
| `quote_outcomes` | `pricing_scenarios` | `quote_id` |
| `vehicles` | `yard_allocation_scenarios` | `vehicle_id` |

---

# Important Synthetic Data Logic

The mock data should contain realistic relationships so the analysis can discover meaningful patterns.

## Yard Operations Logic

- Vehicles in farther zones should usually have longer retrieval times.
- Higher congestion should increase retrieval time.
- More blocked vehicles should increase retrieval time.
- Non-running vehicles should require more equipment and take longer.
- High-priority vehicles should perform better under optimized allocation.
- Overflow zones should be slower and more congested.
- Fast-access zones should have lower retrieval times but limited capacity.

## Pricing Logic

- Higher quoted tow prices should reduce acceptance probability.
- Higher daily storage rates should reduce acceptance probability.
- Strategic partners should have higher acceptance probabilities if service quality is strong.
- More price-sensitive partners should reject expensive quotes more often.
- Higher salvage value should allow more pricing flexibility.
- Competitor prices below the quote should reduce acceptance probability.
- High yard utilization should increase internal cost and may justify higher storage prices.
- Long expected yard stay should reduce partner net recovery.

---

# MVP Recommendation

For the first version of the project, generate these tables first:

1. `vehicles`
2. `yard_locations`
3. `retrieval_events`
4. `insurance_partners`
5. `quote_outcomes`
6. `pricing_scenarios`
7. `yard_allocation_scenarios`

Add these later if the first version works well:

1. `vehicle_location_history`
2. `tow_events`
3. `yard_storage_events`

This gives you enough data to build:

- Executive dashboard
- Yard allocation simulator
- Retrieval performance analysis
- Pricing optimizer
- Methodology page

---

# Final Website Data Exports

The analytics pipeline should eventually export summarized JSON files for the Vercel frontend:

| Export File | Purpose |
|---|---|
| `metrics.json` | Executive KPI cards |
| `yard_zone_performance.json` | Zone-level yard performance |
| `retrieval_drivers.json` | Retrieval delay and driver analysis |
| `allocation_strategy_comparison.json` | Random vs first-available vs optimized allocation |
| `partner_performance.json` | Partner-level quote and margin metrics |
| `pricing_scenarios_summary.json` | Optimizer results |
| `vehicles_sample.json` | Limited vehicle-level sample for explorer page |
| `methodology_summary.json` | Data generation assumptions and model notes |
