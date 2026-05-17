import { getPartnerPerformance, getPricingSummary } from "@/lib/data";
import { ChartPanel } from "@/components/charts/ChartPanel";
import { ComparisonChart, SimpleBarChart } from "@/components/charts/Charts";
import { DataTable } from "@/components/tables/DataTable";
import { PricingWorkbench } from "@/components/ui/PricingWorkbench";
import { SectionHeader } from "@/components/ui/SectionHeader";

export default async function PricingPage() {
  const [partner, pricing] = await Promise.all([getPartnerPerformance(), getPricingSummary()]);

  return (
    <main className="page">
      <SectionHeader
        eyebrow="Pricing optimizer"
        title="Tow and storage pricing recommendations"
        description="Review strategy-level optimizer results and test how partner tier, tow distance, and storage duration affect expected outcomes."
      />
      <PricingWorkbench tiers={partner.tiers} recommendations={pricing.recommended_summary} />
      <section className="section grid two-col">
        <ChartPanel
          title="Expected Value by Objective"
          note="Scenario expected value combines margin and acceptance probability."
          xAxis="Optimization objective used to evaluate pricing scenarios."
          yAxis="Left: expected value in dollars. Right: acceptance probability percent."
          legend="Bar: expected value. Line: acceptance probability."
          takeaway="The best objective balances revenue quality with likelihood of winning the quote."
        >
          <ComparisonChart data={pricing.by_objective} xKey="optimization_objective" barKey="avg_expected_value" lineKey="avg_acceptance_probability" barUnit="currency" lineUnit="percent" angleLabels />
        </ChartPanel>
        <ChartPanel
          title="Margin by Pricing Strategy"
          note="Balanced strategies preserve margin while managing acceptance risk."
          xAxis="Pricing strategy assigned to the quote/scenario."
          yAxis="Average expected gross margin in dollars."
          takeaway="Higher margin is useful only when paired with acceptable win probability."
        >
          <SimpleBarChart data={pricing.by_pricing_strategy} xKey="pricing_strategy" yKey="avg_expected_margin" color="#b7791f" yUnit="currency" angleLabels />
        </ChartPanel>
      </section>
      <section className="section insight-strip">
        <div className="panel insight"><strong>How to read</strong><p className="chart-note">Expected value is the practical metric: it combines margin potential with the chance the partner accepts.</p></div>
        <div className="panel insight"><strong>Partner filter</strong><p className="chart-note">Use the tier control to see how relationship strength changes the recommended quote posture.</p></div>
        <div className="panel insight"><strong>Distance and storage</strong><p className="chart-note">Long tow distances and longer storage periods raise cost, so acceptance needs to be watched alongside margin.</p></div>
      </section>
      <section className="section">
        <DataTable rows={pricing.recommended_summary} columns={["pricing_strategy", "recommended_quotes", "avg_recommended_tow_price", "avg_recommended_daily_storage_rate", "avg_recommended_expected_value"]} />
      </section>
    </main>
  );
}
