import type { LucideIcon } from "lucide-react";

type KpiCardProps = {
  label: string;
  value: string;
  note?: string;
  icon: LucideIcon;
};

export function KpiCard({ label, value, note, icon: Icon }: KpiCardProps) {
  return (
    <section className="panel panel-pad metric">
      <div className="metric-top">
        <p className="metric-label">{label}</p>
        <span className="icon-box"><Icon size={18} /></span>
      </div>
      <strong className="metric-value">{value}</strong>
      {note ? <span className="metric-note">{note}</span> : null}
    </section>
  );
}
