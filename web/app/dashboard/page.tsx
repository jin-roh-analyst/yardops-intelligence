import { Clock, Gauge, MapPin, Percent } from "lucide-react";
import { getAllDashboardData } from "@/lib/data";
import { currency, number, percent } from "@/lib/formatters";
import { KpiCard } from "@/components/cards/KpiCard";
import { ChartPanel } from "@/components/charts/ChartPanel";
import { ComparisonChart, LineMetricChart, MultiBarChart, SimpleBarChart } from "@/components/charts/Charts";
import { SectionHeader } from "@/components/ui/SectionHeader";

export default async function DashboardPage() {
  const { metrics, yard, partner, pricing } = await getAllDashboardData();
  const summary = metrics.summary;
  const zoneNames: Record<string, string> = {
    A: "Standard Zone A",
    B: "Standard Zone B",
    FA: "Fast Access Zone",
    HV: "Heavy Vehicle Zone",
    LTH: "Long-Term Hold Zone",
    NR: "Non-Running Zone",
    OF: "Overflow Zone"
  };
  const zonePerformance = Object.values(
    yard.records.reduce<Record<string, { zone_id: string; full_zone_name: string; congestion_score: number; occupancy_percent: number; count: number }>>((acc, row) => {
      const zone = String(row.zone_id);
      if (!acc[zone]) {
        acc[zone] = { zone_id: zone, full_zone_name: `${zoneNames[zone] ?? `Zone ${zone}`} (all yards average)`, congestion_score: 0, occupancy_percent: 0, count: 0 };
      }
      acc[zone].congestion_score += Number(row.congestion_score);
      acc[zone].occupancy_percent += Number(row.occupancy_rate) * 100;
      acc[zone].count += 1;
      return acc;
    }, {})
  ).map((row) => ({
    zone_id: row.zone_id,
    full_zone_name: row.full_zone_name,
    congestion_score: Number((row.congestion_score / row.count).toFixed(2)),
    occupancy_percent: Number((row.occupancy_percent / row.count).toFixed(2))
  }));

  return (
    <main className="page">
      <SectionHeader
        eyebrow="Executive dashboard"
        title="Operational performance and pricing health"
        description="High-level yard, retrieval, and partner economics generated from the synthetic raw operations tables."
      />
      <div className="grid kpi-grid">
        <KpiCard label="Total Vehicles" value={number(summary.total_vehicles)} note={`${summary.active_yards} active yards`} icon={MapPin} />
        <KpiCard label="Average Retrieval" value={`${number(summary.average_retrieval_time_minutes, 1)}m`} note={`Median ${number(summary.median_retrieval_time_minutes, 1)}m`} icon={Clock} />
        <KpiCard label="Quote Acceptance" value={percent(summary.quote_acceptance_rate)} note={`${currency(summary.average_expected_margin)} avg margin`} icon={Percent} />
        <KpiCard label="Yard Utilization" value={percent(summary.average_yard_utilization)} note={`${percent(summary.percent_retrievals_under_15_minutes)} under 15m`} icon={Gauge} />
      </div>
      <section className="section grid two-col">
        <ChartPanel
          title="Retrieval Time by Yard"
          note="Average retrieval duration across each synthetic yard."
          xAxis="Each operating yard in the synthetic network."
          yAxis="Average minutes from retrieval start to handoff-ready movement."
          takeaway="Lower values indicate faster yard access and less internal travel time."
        >
          <LineMetricChart data={yard.yards} xKey="yard_id" yKey="avg_retrieval_duration_minutes" yUnit="minutes" angleLabels />
        </ChartPanel>
        <ChartPanel
          title="Quote Acceptance by Partner Tier"
          note="Strategic and national relationships should show stronger pricing resilience."
          xAxis="Partner commercial tier."
          yAxis="Accepted quotes as a percentage of all quotes."
          takeaway="Higher acceptance suggests stronger relationship fit or better price positioning."
        >
          <SimpleBarChart data={partner.tiers} xKey="partner_tier" yKey="acceptance_rate" color="#2563eb" yUnit="percent" />
        </ChartPanel>
        <ChartPanel
          title="Margin by Pricing Strategy"
          note="Scenario outputs summarize expected margin across optimizer strategies."
          xAxis="Pricing strategy used in the scenario."
          yAxis="Average expected gross margin in dollars. Axis is zoomed to show small differences."
          takeaway="Compare relative strategy profitability before considering partner acceptance tradeoffs."
        >
          <SimpleBarChart data={pricing.by_pricing_strategy} xKey="pricing_strategy" yKey="avg_expected_margin" color="#2563eb" yUnit="currency" angleLabels yDomainMode="tight" />
        </ChartPanel>
        <ChartPanel
          title="Yard Congestion by Zone"
          note="Congestion score and utilization show where retrieval pressure is building."
          xAxis="Zone identifier within each yard sample."
          yAxis="Left: congestion score from 0-100. Right: occupancy rate as a percent."
          legend="Bars are congestion score. The line is occupancy rate."
          takeaway="High congestion plus high utilization identifies zones that may slow retrieval."
        >
          <ComparisonChart data={zonePerformance} xKey="zone_id" fullLabelKey="full_zone_name" barKey="congestion_score" lineKey="occupancy_percent" barUnit="score" lineUnit="percent" />
        </ChartPanel>
      </section>
      <section className="section">
        <ChartPanel
          title="Partner Economics by Tier"
          note="Acceptance, margin, and recovery move together differently by partner segment."
          xAxis="Partner tier."
          yAxis="Mixed business metrics: percent acceptance plus dollar-value margin/recovery."
          legend="Use the legend to isolate one metric at a time."
          takeaway="This view is for relative comparison, not unit-for-unit scale comparison."
        >
          <MultiBarChart data={partner.tiers} xKey="partner_tier" bars={["acceptance_rate", "avg_expected_margin", "avg_net_expected_recovery"]} units={{ acceptance_rate: "percent", avg_expected_margin: "currency", avg_net_expected_recovery: "currency" }} />
        </ChartPanel>
      </section>
      <section className="section insight-strip">
        <div className="panel insight"><strong>Operational signal</strong><p className="chart-note">Average retrieval time is {number(summary.average_retrieval_time_minutes, 1)} minutes, while only {percent(summary.percent_retrievals_under_15_minutes)} finish under 15 minutes.</p></div>
        <div className="panel insight"><strong>Commercial signal</strong><p className="chart-note">Quote acceptance is {percent(summary.quote_acceptance_rate)} with average expected margin of {currency(summary.average_expected_margin)}.</p></div>
        <div className="panel insight"><strong>Capacity signal</strong><p className="chart-note">Average yard utilization is {percent(summary.average_yard_utilization)}, which makes congestion a material retrieval risk.</p></div>
      </section>
    </main>
  );
}
