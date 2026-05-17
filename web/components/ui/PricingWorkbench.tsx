"use client";

import { useMemo, useState } from "react";
import { currency, number, percent, titleize } from "@/lib/formatters";

type Tier = Record<string, string | number>;
type Recommendation = Record<string, string | number>;

export function PricingWorkbench({
  tiers,
  recommendations
}: {
  tiers: Tier[];
  recommendations: Recommendation[];
}) {
  const [tierName, setTierName] = useState(String(tiers[0]?.partner_tier ?? "strategic"));
  const [distance, setDistance] = useState(38);
  const [storageDays, setStorageDays] = useState(28);

  const tier = useMemo(() => tiers.find((item) => item.partner_tier === tierName) ?? tiers[0], [tierName, tiers]);
  const recommendation = recommendations[0] ?? {};
  const tow = Number(recommendation.avg_recommended_tow_price ?? 420) + distance * 2.15;
  const storageRate = Number(recommendation.avg_recommended_daily_storage_rate ?? 33);
  const partnerCost = tow + storageRate * storageDays;
  const acceptance = Math.max(12, Math.min(96, Number(tier.acceptance_rate ?? 60) - Math.max(0, distance - 40) * 0.18));
  const margin = partnerCost * 0.31;

  return (
    <section className="section">
      <div className="section-header">
        <div>
          <h2>Pricing Scenario Workbench</h2>
          <p className="chart-note">Estimate how tier, tow distance, and storage days affect acceptance and margin using the exported optimizer summaries.</p>
        </div>
      </div>
      <div className="toolbar">
        <select className="select" value={tierName} onChange={(event) => setTierName(event.target.value)} aria-label="Partner tier">
          {tiers.map((item) => (
            <option key={String(item.partner_tier)} value={String(item.partner_tier)}>
              {titleize(String(item.partner_tier))}
            </option>
          ))}
        </select>
        <input className="input" type="number" min="1" max="500" value={distance} onChange={(event) => setDistance(Number(event.target.value))} aria-label="Tow distance miles" />
        <input className="input" type="number" min="1" max="180" value={storageDays} onChange={(event) => setStorageDays(Number(event.target.value))} aria-label="Storage days" />
      </div>
      <div className="grid kpi-grid">
        <div className="panel panel-pad">
          <p className="metric-label">Recommended Tow Price</p>
          <strong className="metric-value">{currency(tow)}</strong>
        </div>
        <div className="panel panel-pad">
          <p className="metric-label">Daily Storage Rate</p>
          <strong className="metric-value">{currency(storageRate)}</strong>
        </div>
        <div className="panel panel-pad">
          <p className="metric-label">Acceptance Probability</p>
          <strong className="metric-value">{percent(acceptance)}</strong>
        </div>
        <div className="panel panel-pad">
          <p className="metric-label">Expected Margin</p>
          <strong className="metric-value">{currency(margin)}</strong>
          <span className="metric-note">Total partner cost {currency(partnerCost)}</span>
        </div>
      </div>
      <p className="chart-note section">Selected tier: {titleize(String(tier.partner_tier))}. Baseline tier acceptance is {percent(Number(tier.acceptance_rate))} across {number(Number(tier.quote_count))} quotes. The two inputs are tow distance in miles and expected storage days.</p>
    </section>
  );
}
