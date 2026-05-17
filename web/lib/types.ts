export type Metrics = {
  generated_at: string;
  source: string;
  summary: {
    total_vehicles: number;
    active_yards: number;
    average_retrieval_time_minutes: number;
    median_retrieval_time_minutes: number;
    percent_retrievals_under_15_minutes: number;
    average_customer_carrier_wait_minutes: number;
    average_yard_utilization: number;
    quote_acceptance_rate: number;
    average_expected_margin: number;
    average_partner_net_recovery: number;
  };
  table_row_counts: Record<string, number>;
};

export type YardZonePerformance = {
  summary: Record<string, number>;
  yards: Array<Record<string, string | number>>;
  records: Array<Record<string, string | number>>;
};

export type RetrievalDrivers = {
  summary: Record<string, number>;
  delay_reasons: Array<Record<string, string | number>>;
  equipment: Array<Record<string, string | number>>;
  blocked_vehicle_buckets: Array<Record<string, string | number>>;
  zone_types: Array<Record<string, string | number>>;
  pickup_types: Array<Record<string, string | number>>;
};

export type AllocationComparison = {
  summary: Record<string, string | number>;
  strategies: Array<Record<string, string | number>>;
  by_vehicle_type: Array<Record<string, string | number>>;
};

export type PartnerPerformance = {
  summary: Record<string, number>;
  tiers: Array<Record<string, string | number>>;
  partners: Array<Record<string, string | number>>;
};

export type PricingSummary = {
  summary: Record<string, number>;
  by_objective: Array<Record<string, string | number>>;
  by_pricing_strategy: Array<Record<string, string | number>>;
  recommended_summary: Array<Record<string, string | number>>;
};

export type VehiclesSample = {
  summary: Record<string, string | number>;
  records: Array<Record<string, string | number>>;
};

export type MethodologySummary = {
  summary: Record<string, string>;
  source_tables: Array<{ table: string; rows: number }>;
  assumptions: string[];
  exports: string[];
};
