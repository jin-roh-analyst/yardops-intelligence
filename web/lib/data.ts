import "server-only";
import { promises as fs } from "fs";
import path from "path";
import type {
  AllocationComparison,
  MethodologySummary,
  Metrics,
  PartnerPerformance,
  PricingSummary,
  RetrievalDrivers,
  VehiclesSample,
  YardZonePerformance
} from "./types";

const dataDir = path.join(process.cwd(), "public", "data");

async function readJson<T>(fileName: string): Promise<T> {
  const file = await fs.readFile(path.join(dataDir, fileName), "utf8");
  return JSON.parse(file) as T;
}

export async function getMetrics() {
  return readJson<Metrics>("metrics.json");
}

export async function getYardZonePerformance() {
  return readJson<YardZonePerformance>("yard_zone_performance.json");
}

export async function getRetrievalDrivers() {
  return readJson<RetrievalDrivers>("retrieval_drivers.json");
}

export async function getAllocationComparison() {
  return readJson<AllocationComparison>("allocation_strategy_comparison.json");
}

export async function getPartnerPerformance() {
  return readJson<PartnerPerformance>("partner_performance.json");
}

export async function getPricingSummary() {
  return readJson<PricingSummary>("pricing_scenarios_summary.json");
}

export async function getVehiclesSample() {
  return readJson<VehiclesSample>("vehicles_sample.json");
}

export async function getMethodologySummary() {
  return readJson<MethodologySummary>("methodology_summary.json");
}

export async function getAllDashboardData() {
  const [metrics, yard, retrieval, allocation, partner, pricing, vehicles, methodology] = await Promise.all([
    getMetrics(),
    getYardZonePerformance(),
    getRetrievalDrivers(),
    getAllocationComparison(),
    getPartnerPerformance(),
    getPricingSummary(),
    getVehiclesSample(),
    getMethodologySummary()
  ]);
  return { metrics, yard, retrieval, allocation, partner, pricing, vehicles, methodology };
}
