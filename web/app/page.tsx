import Link from "next/link";
import { ArrowRight, Calculator, Clock, Database, FileJson, Map, Route, TriangleAlert } from "lucide-react";
import { getAllDashboardData } from "@/lib/data";
import { compact, currency, number, percent } from "@/lib/formatters";
import { KpiCard } from "@/components/cards/KpiCard";

export default async function HomePage() {
  const { metrics, allocation, pricing, retrieval } = await getAllDashboardData();
  const summary = metrics.summary;
  const optimized = allocation.strategies.find((strategy) => strategy.allocation_strategy === "optimized") ?? allocation.strategies[0];
  const random = allocation.strategies.find((strategy) => strategy.allocation_strategy === "random") ?? allocation.strategies[0];
  const retrievalLift = Number(random.avg_retrieval_duration_minutes) - Number(optimized.avg_retrieval_duration_minutes);
  const topDelayReason = retrieval.delay_reasons[0];

  return (
    <main className="page">
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">Synthetic operations analytics</span>
          <h1>YardOps Intelligence</h1>
          <p className="lead">
            Analytics platform for salvage yard placement, retrieval performance, and tow/storage pricing decisions.
          </p>
          <div className="hero-actions">
            <Link className="button" href="/dashboard">Open Dashboard <ArrowRight size={18} /></Link>
            <Link className="button secondary" href="/methodology">View Methodology</Link>
          </div>
          <div className="grid three-col">
            <KpiCard label="Vehicles Modeled" value={compact(summary.total_vehicles)} note={`${number(metrics.table_row_counts.retrieval_events)} retrieval events`} icon={Map} />
            <KpiCard label="Avg Retrieval" value={`${number(summary.average_retrieval_time_minutes, 1)}m`} note={`${percent(summary.percent_retrievals_under_15_minutes)} under 15 minutes`} icon={Clock} />
            <KpiCard label="Avg Margin" value={currency(summary.average_expected_margin)} note={`${percent(summary.quote_acceptance_rate)} quote acceptance`} icon={Calculator} />
          </div>
        </div>
        <div className="context-panel panel" aria-label="Project context">
          <div className="context-step problem">
            <span><TriangleAlert size={18} /> Problem</span>
            <h2>Yard decisions are operationally connected.</h2>
            <p>Vehicle placement affects retrieval time. Retrieval time affects buyer and carrier waiting. Pricing affects whether insurance partners accept tow and storage quotes.</p>
          </div>
          <div className="context-step">
            <span><Map size={18} /> Analytics Response</span>
            <h2>Simulate the system before making tradeoffs.</h2>
            <p>The project generates synthetic operations data, scores vehicle placement, summarizes retrieval drivers, and compares pricing scenarios as static dashboard outputs.</p>
          </div>
          <div className="context-flow" aria-label="Analytics pipeline flow">
            <div><Database size={17} /><span>Raw CSVs</span></div>
            <ArrowRight size={16} />
            <div><Calculator size={17} /><span>Models</span></div>
            <ArrowRight size={16} />
            <div><FileJson size={17} /><span>JSON</span></div>
          </div>
          <div className="context-outcome">
            <div>
              <small>Best allocation strategy</small>
              <strong>{String(allocation.summary.best_strategy_by_efficiency).replaceAll("_", " ")}</strong>
            </div>
            <div>
              <small>Scenario simulations</small>
              <strong>{number(Number(allocation.summary.scenario_count))}</strong>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <h2>The Operational Problem</h2>
          <p className="chart-note">A salvage yard is not just storage space. It is a routing, capacity, labor, equipment, and pricing problem.</p>
        </div>
        <div className="problem-grid">
          <div className="panel panel-pad">
            <span className="problem-icon"><Map size={18} /></span>
            <span className="eyebrow">Placement</span>
            <h3>High-priority vehicles can be buried in slow zones.</h3>
            <p className="chart-note">If vehicles are assigned by first available space, retrieval teams may spend more time traveling, moving blocked vehicles, or waiting for equipment.</p>
          </div>
          <div className="panel panel-pad">
            <span className="problem-icon"><Route size={18} /></span>
            <span className="eyebrow">Retrieval</span>
            <h3>Delays are caused by multiple interacting drivers.</h3>
            <p className="chart-note">Congestion, blocked access, non-running vehicles, equipment availability, and pickup type all influence the handoff experience.</p>
          </div>
          <div className="panel panel-pad">
            <span className="problem-icon"><Calculator size={18} /></span>
            <span className="eyebrow">Pricing</span>
            <h3>Higher price does not always mean better economics.</h3>
            <p className="chart-note">Tow and storage quotes must balance partner sensitivity, expected recovery, competitor price, yard utilization, and margin.</p>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <h2>What the Analytics Solves</h2>
          <p className="chart-note">The Python pipeline turns synthetic raw tables into compact JSON files that power each dashboard page without a live backend.</p>
        </div>
        <div className="solution-map panel">
          <div>
            <span className="solution-index">01</span>
            <h3>Allocate vehicles more deliberately</h3>
            <p>Compare random, first-available, priority-based, and optimized placement strategies against retrieval time and efficiency score.</p>
            <span className="solution-metric">{number(Number(optimized.avg_retrieval_duration_minutes), 1)} min optimized retrieval</span>
          </div>
          <div>
            <span className="solution-index">02</span>
            <h3>Diagnose retrieval delay drivers</h3>
            <p>Separate physical retrieval time from customer/carrier wait time and identify the largest contributors to operational delay.</p>
            <span className="solution-metric">{String(topDelayReason.delay_reason).replaceAll("_", " ")} is the top driver</span>
          </div>
          <div>
            <span className="solution-index">03</span>
            <h3>Optimize pricing scenarios</h3>
            <p>Evaluate tow price, storage rate, free days, expected margin, and acceptance probability before recommending a pricing posture.</p>
            <span className="solution-metric">{currency(Number(pricing.summary.avg_scenario_expected_value))} avg expected value</span>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-header">
          <h2>Featured Insight</h2>
          <p className="chart-note">Recommended scenarios produce an average expected value of {currency(Number(pricing.summary.avg_scenario_expected_value))}.</p>
        </div>
        <div className="featured-insight panel">
          <div className="featured-copy">
            <span className="eyebrow">Portfolio readout</span>
            <h2>Optimized placement cuts simulated retrieval time while preserving pricing margin.</h2>
            <p>
              The model compares yard assignment strategies against quote economics. Optimized allocation reduces retrieval duration by {number(retrievalLift, 1)} minutes versus random placement, while recommended pricing scenarios keep expected value at {currency(Number(pricing.summary.avg_scenario_expected_value))}.
            </p>
            <Link className="button secondary" href="/yard-simulator">Inspect Simulator <ArrowRight size={18} /></Link>
          </div>
          <div className="featured-metrics">
            <div>
              <span>Optimized Retrieval</span>
              <strong>{number(Number(optimized.avg_retrieval_duration_minutes), 1)} min</strong>
              <small>{number(retrievalLift, 1)} min faster than random</small>
            </div>
            <div>
              <span>Top Delay Driver</span>
              <strong>{String(topDelayReason.delay_reason).replaceAll("_", " ")}</strong>
              <small>{number(Number(topDelayReason.retrieval_count))} retrieval events</small>
            </div>
            <div>
              <span>Recommended Scenario Value</span>
              <strong>{currency(Number(pricing.summary.avg_scenario_expected_value))}</strong>
              <small>{number(Number(pricing.summary.recommended_scenario_count))} recommended scenarios</small>
            </div>
          </div>
          <div className="featured-flow" aria-label="Insight flow">
            <div><Map size={18} /><span>Place priority vehicles closer</span></div>
            <div><Route size={18} /><span>Reduce blocked-path retrieval time</span></div>
            <div><Calculator size={18} /><span>Protect expected quote value</span></div>
          </div>
        </div>
      </section>
    </main>
  );
}
