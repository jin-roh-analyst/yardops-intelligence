import { getRetrievalDrivers } from "@/lib/data";
import { ChartPanel } from "@/components/charts/ChartPanel";
import { ComparisonChart, SimpleBarChart } from "@/components/charts/Charts";
import { DataTable } from "@/components/tables/DataTable";
import { SectionHeader } from "@/components/ui/SectionHeader";

export default async function RetrievalPage() {
  const retrieval = await getRetrievalDrivers();

  return (
    <main className="page">
      <SectionHeader
        eyebrow="Retrieval performance"
        title="Delay drivers across yard operations"
        description="Analyze how blocked access, equipment, zone type, and pickup type affect retrieval duration and customer/carrier wait time."
      />
      <section className="grid kpi-grid">
        <div className="panel panel-pad"><p className="metric-label">Retrieval Events</p><strong className="metric-value">{retrieval.summary.retrieval_count}</strong></div>
        <div className="panel panel-pad"><p className="metric-label">Delay Rate</p><strong className="metric-value">{retrieval.summary.delay_rate}%</strong></div>
        <div className="panel panel-pad"><p className="metric-label">Avg Blocked Vehicles</p><strong className="metric-value">{retrieval.summary.avg_blocked_vehicle_count}</strong></div>
        <div className="panel panel-pad"><p className="metric-label">Driver Groups</p><strong className="metric-value">5</strong></div>
      </section>
      <section className="section grid two-col">
        <ChartPanel
          title="Delay Reasons"
          note="Delay rate is highest when operational blockers are present."
          xAxis="Primary delay reason recorded on each retrieval event."
          yAxis="Number of retrieval events."
          takeaway="Large bars show the most frequent operational causes to investigate first."
        >
          <SimpleBarChart data={retrieval.delay_reasons} xKey="delay_reason" yKey="retrieval_count" color="#1d4ed8" yUnit="count" angleLabels />
        </ChartPanel>
        <ChartPanel
          title="Equipment Impact"
          note="Equipment requirements increase duration and wait time."
          xAxis="Equipment used during retrieval."
          yAxis="Left: average retrieval minutes. Right: delay rate percent."
          legend="Bar: duration. Line: delay rate."
          takeaway="Specialized equipment raises both handling time and scheduling risk."
        >
          <ComparisonChart data={retrieval.equipment} xKey="equipment_used" barKey="avg_retrieval_duration_minutes" lineKey="delay_rate" barUnit="minutes" lineUnit="percent" angleLabels />
        </ChartPanel>
        <ChartPanel
          title="Blocked Vehicle Buckets"
          note="Blocked access is a core retrieval driver."
          xAxis="Number of vehicles blocking the retrieval path."
          yAxis="Left: average wait minutes. Right: average retrieval minutes."
          legend="Bar: wait time. Line: active retrieval duration."
          takeaway="The gap between wait and duration shows queueing and start-delay pressure."
        >
          <ComparisonChart data={retrieval.blocked_vehicle_buckets} xKey="blocked_vehicle_bucket" barKey="avg_wait_time_minutes" lineKey="avg_retrieval_duration_minutes" barUnit="minutes" lineUnit="minutes" />
        </ChartPanel>
        <ChartPanel
          title="Pickup Type Impact"
          note="Carrier pickups and internal moves behave differently operationally."
          xAxis="Pickup workflow type."
          yAxis="Average request-to-handoff wait time in minutes. Axis is zoomed to show small differences."
          takeaway="Higher relative wait times indicate where yard coordination or staging can improve."
        >
          <SimpleBarChart data={retrieval.pickup_types} xKey="pickup_type" yKey="avg_wait_time_minutes" color="#2563eb" yUnit="minutes" angleLabels yDomainMode="tight" />
        </ChartPanel>
      </section>
      <section className="section insight-strip">
        <div className="panel insight"><strong>Primary read</strong><p className="chart-note">Use event count to find frequent issues, then duration and delay rate to judge operational severity.</p></div>
        <div className="panel insight"><strong>Blocked access</strong><p className="chart-note">The blocked-vehicle view separates physical retrieval work from customer/carrier waiting time.</p></div>
        <div className="panel insight"><strong>Equipment planning</strong><p className="chart-note">Forklift, loader, and tow-truck events should be interpreted as capacity scheduling problems, not only vehicle problems.</p></div>
      </section>
      <section className="section">
        <DataTable rows={retrieval.zone_types} columns={["zone_type", "retrieval_count", "avg_retrieval_duration_minutes", "avg_wait_time_minutes", "delay_rate"]} />
      </section>
    </main>
  );
}
