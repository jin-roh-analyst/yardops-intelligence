import { getMethodologySummary, getMetrics } from "@/lib/data";
import { DataTable } from "@/components/tables/DataTable";
import { SectionHeader } from "@/components/ui/SectionHeader";

export default async function MethodologyPage() {
  const [methodology, metrics] = await Promise.all([getMethodologySummary(), getMetrics()]);

  return (
    <main className="page">
      <SectionHeader
        eyebrow="Methodology"
        title="Synthetic data and analytics approach"
        description="The project uses simulated operations data, deterministic generation, pandas aggregation, and static JSON exports for Vercel deployment."
      />
      <section className="grid two-col">
        <div className="panel panel-pad">
          <h2>Pipeline</h2>
          <p className="chart-note section">{methodology.summary.pipeline}</p>
        </div>
        <div className="panel panel-pad">
          <h2>Data Boundary</h2>
          <p className="chart-note section">All records are synthetic and inspired by salvage vehicle logistics workflows. No confidential or real company data is used.</p>
        </div>
      </section>
      <section className="section">
        <div className="section-header"><h2>Data Generation Assumptions</h2></div>
        <ul className="method-list">
          {methodology.assumptions.map((assumption) => (
            <li key={assumption}>{assumption}</li>
          ))}
        </ul>
      </section>
      <section className="section">
        <div className="section-header">
          <h2>How to Read the Product</h2>
          <p className="chart-note">Each chart includes axis definitions and hover labels so a reviewer can interpret the metric without reading the code.</p>
        </div>
        <div className="grid three-col">
          <div className="panel panel-pad"><h3>Yard views</h3><p className="chart-note section">Focus on retrieval minutes, utilization, congestion, and efficiency score. Lower time and higher efficiency indicate better placement.</p></div>
          <div className="panel panel-pad"><h3>Retrieval views</h3><p className="chart-note section">Compare event count, duration, wait time, and delay rate. Frequent and severe drivers deserve the first operational response.</p></div>
          <div className="panel panel-pad"><h3>Pricing views</h3><p className="chart-note section">Read expected value as the combined business outcome from price, margin, and acceptance probability.</p></div>
        </div>
      </section>
      <section className="section grid two-col">
        <div className="panel panel-pad">
          <h2>Priority Score</h2>
          <p className="chart-note section">Priority blends partner value, operational complexity, and salvage value to guide zone assignment and simulation scoring.</p>
        </div>
        <div className="panel panel-pad">
          <h2>Pricing Optimizer</h2>
          <p className="chart-note section">Scenario outputs compare tow price, storage rate, free days, expected margin, and acceptance probability.</p>
        </div>
        <div className="panel panel-pad">
          <h2>Retrieval Model</h2>
          <p className="chart-note section">Retrieval duration is summarized from zone distance, congestion, blocked vehicles, equipment, pickup type, and wait time.</p>
        </div>
        <div className="panel panel-pad">
          <h2>Limitations</h2>
          <p className="chart-note section">The current MVP uses rule-based synthetic relationships and aggregate summaries, not a live optimization service.</p>
        </div>
      </section>
      <section className="section">
        <div className="section-header">
          <h2>Source Tables</h2>
          <p className="chart-note">Total vehicles modeled: {metrics.summary.total_vehicles}</p>
        </div>
        <DataTable rows={methodology.source_tables} columns={["table", "rows"]} />
      </section>
    </main>
  );
}
