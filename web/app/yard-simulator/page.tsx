import { getAllocationComparison, getYardZonePerformance } from "@/lib/data";
import { ChartPanel } from "@/components/charts/ChartPanel";
import { SimpleBarChart } from "@/components/charts/Charts";
import { DataTable } from "@/components/tables/DataTable";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { YardStrategyWorkbench } from "@/components/ui/YardStrategyWorkbench";

export default async function YardSimulatorPage() {
  const [allocation, yard] = await Promise.all([getAllocationComparison(), getYardZonePerformance()]);
  const zoneNames: Record<string, string> = {
    A: "Standard Zone A",
    B: "Standard Zone B",
    FA: "Fast Access Zone",
    HV: "Heavy Vehicle Zone",
    LTH: "Long-Term Hold Zone",
    NR: "Non-Running Zone",
    OF: "Overflow Zone"
  };
  const zoneUtilization = Object.values(
    yard.records.reduce<Record<string, { zone_id: string; full_zone_name: string; occupancy_percent: number; count: number }>>((acc, row) => {
      const zone = String(row.zone_id);
      if (!acc[zone]) {
        acc[zone] = { zone_id: zone, full_zone_name: `${zoneNames[zone] ?? `Zone ${zone}`} (all yards average)`, occupancy_percent: 0, count: 0 };
      }
      acc[zone].occupancy_percent += Number(row.occupancy_rate) * 100;
      acc[zone].count += 1;
      return acc;
    }, {})
  ).map((row) => ({
    zone_id: row.zone_id,
    full_zone_name: row.full_zone_name,
    occupancy_percent: Number((row.occupancy_percent / row.count).toFixed(2))
  }));
  const optimizedVehicleEfficiency = allocation.by_vehicle_type
    .filter((row) => row.allocation_strategy === "optimized")
    .map((row) => ({
      ...row,
      vehicle_type_label: String(row.vehicle_type)
    }));

  return (
    <main className="page">
      <SectionHeader
        eyebrow="Yard simulator"
        title="Allocation strategy comparison"
        description="Compare how assignment logic changes retrieval time, wait time, travel distance, and priority-weighted performance."
      />
      <YardStrategyWorkbench strategies={allocation.strategies} />
      <section className="section grid two-col">
        <ChartPanel
          title="Zone Utilization"
          note="Fast-access and overflow zones are intentionally capacity-sensitive."
          xAxis="Zone identifier from the yard layout table."
          yAxis="Average occupancy rate as a percent."
          takeaway="High utilization in access-critical zones can reduce the benefit of optimized placement."
        >
          <SimpleBarChart data={zoneUtilization} xKey="zone_id" yKey="occupancy_percent" color="#0ea5e9" yUnit="percent" fullLabelKey="full_zone_name" />
        </ChartPanel>
        <ChartPanel
          title="Optimized Efficiency by Vehicle Type"
          note="Vehicle mix affects allocation outcomes and equipment needs."
          xAxis="Vehicle type under the optimized allocation strategy."
          yAxis="Allocation efficiency score on a 0-100 scale."
          takeaway="Heavy and non-running mixes usually need more deliberate slot assignment."
        >
          <SimpleBarChart data={optimizedVehicleEfficiency} xKey="vehicle_type_label" yKey="avg_allocation_efficiency_score" color="#2563eb" yUnit="score" angleLabels />
        </ChartPanel>
      </section>
      <section className="section insight-strip">
        <div className="panel insight"><strong>How to compare</strong><p className="chart-note">Start with retrieval duration, then check priority-weighted time to see whether high-value vehicles are being served faster.</p></div>
        <div className="panel insight"><strong>Best overall</strong><p className="chart-note">The exported simulation identifies {allocation.summary.best_strategy_by_efficiency} as the highest efficiency strategy.</p></div>
        <div className="panel insight"><strong>Capacity tradeoff</strong><p className="chart-note">Fast zones help retrieval speed, but limited capacity means optimized placement must reserve them for priority vehicles.</p></div>
      </section>
      <section className="section">
        <DataTable rows={allocation.strategies} columns={["allocation_strategy", "scenario_count", "avg_retrieval_duration_minutes", "pct_under_15_min", "avg_allocation_efficiency_score"]} />
      </section>
    </main>
  );
}
