export function ChartPanel({
  title,
  note,
  xAxis,
  yAxis,
  legend,
  takeaway,
  children
}: {
  title: string;
  note?: string;
  xAxis?: string;
  yAxis?: string;
  legend?: string;
  takeaway?: string;
  children: React.ReactNode;
}) {
  return (
    <section className="panel chart-panel">
      <div className="chart-title">
        <h3>{title}</h3>
        {note ? <p className="chart-note">{note}</p> : null}
      </div>
      <div className="chart-body">{children}</div>
      {(xAxis || yAxis || legend || takeaway) ? (
        <div className="chart-explainer">
          {xAxis ? <span><strong>X-axis</strong> {xAxis}</span> : null}
          {yAxis ? <span><strong>Y-axis</strong> {yAxis}</span> : null}
          {legend ? <span><strong>Legend</strong> {legend}</span> : null}
          {takeaway ? <span><strong>Readout</strong> {takeaway}</span> : null}
        </div>
      ) : null}
    </section>
  );
}
