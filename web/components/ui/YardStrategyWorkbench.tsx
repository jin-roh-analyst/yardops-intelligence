"use client";

import { useMemo, useState } from "react";
import { ComparisonChart } from "@/components/charts/Charts";
import { ChartPanel } from "@/components/charts/ChartPanel";
import { number, percent, titleize } from "@/lib/formatters";

type Strategy = Record<string, string | number>;

export function YardStrategyWorkbench({ strategies }: { strategies: Strategy[] }) {
  const [selected, setSelected] = useState(String(strategies[0]?.allocation_strategy ?? "optimized"));
  const selectedStrategy = useMemo(
    () => strategies.find((strategy) => strategy.allocation_strategy === selected) ?? strategies[0],
    [selected, strategies]
  );

  return (
    <section className="section">
      <div className="section-header">
        <div>
          <h2>Allocation Strategy Simulator</h2>
          <p className="chart-note">Compare simulated yard assignment strategies across retrieval speed, wait time, and priority-weighted performance.</p>
        </div>
        <select className="select" value={selected} onChange={(event) => setSelected(event.target.value)} aria-label="Allocation strategy">
          {strategies.map((strategy) => (
            <option key={String(strategy.allocation_strategy)} value={String(strategy.allocation_strategy)}>
              {titleize(String(strategy.allocation_strategy))}
            </option>
          ))}
        </select>
      </div>
      <div className="grid kpi-grid">
        <div className="panel panel-pad">
          <p className="metric-label">Average Retrieval</p>
          <strong className="metric-value">{number(Number(selectedStrategy.avg_retrieval_duration_minutes), 1)}m</strong>
        </div>
        <div className="panel panel-pad">
          <p className="metric-label">Priority-Weighted Time</p>
          <strong className="metric-value">{number(Number(selectedStrategy.avg_priority_weighted_time), 1)}</strong>
        </div>
        <div className="panel panel-pad">
          <p className="metric-label">Under 15 Minutes</p>
          <strong className="metric-value">{percent(Number(selectedStrategy.pct_under_15_min))}</strong>
        </div>
        <div className="panel panel-pad">
          <p className="metric-label">Efficiency Score</p>
          <strong className="metric-value">{number(Number(selectedStrategy.avg_allocation_efficiency_score), 1)}</strong>
        </div>
      </div>
      <div className="section">
        <ChartPanel
          title="Strategy Comparison"
          note="Bars show average retrieval duration; the line shows allocation efficiency."
          xAxis="Allocation strategy tested in the simulation."
          yAxis="Left: average retrieval duration in minutes. Right: allocation efficiency score."
          legend="Bar: retrieval minutes. Line: efficiency score."
          takeaway="The best strategy keeps retrieval time low while preserving a high efficiency score."
        >
          <ComparisonChart data={strategies} xKey="allocation_strategy" barKey="avg_retrieval_duration_minutes" lineKey="avg_allocation_efficiency_score" barUnit="minutes" lineUnit="score" angleLabels />
        </ChartPanel>
      </div>
    </section>
  );
}
