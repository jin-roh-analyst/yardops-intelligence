"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

const colors = ["#1d4ed8", "#2563eb", "#3b82f6", "#60a5fa", "#7dd3fc", "#93c5fd"];

type RecordRow = Record<string, string | number>;
type Unit = "count" | "minutes" | "percent" | "currency" | "score" | "meters" | "none";
type DomainMode = "zero" | "tight";

function label(value: string | number) {
  return String(value).replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function valueLabel(value: string) {
  return label(value)
    .replace("Avg ", "Average ")
    .replace("Pct ", "Percent ")
    .replace("Under 15 Min", "Under 15 Minutes");
}

function metricValue(value: string | number, unit: Unit = "none") {
  if (typeof value !== "number") {
    return label(value);
  }
  const scaled = unit === "percent" && Math.abs(value) <= 1 ? value * 100 : value;
  const formatted = new Intl.NumberFormat("en-US", { maximumFractionDigits: 2 }).format(scaled);
  if (unit === "percent") {
    return `${formatted}%`;
  }
  if (unit === "currency") {
    return `$${formatted}`;
  }
  if (unit === "minutes") {
    return `${formatted} min`;
  }
  if (unit === "meters") {
    return `${formatted} m`;
  }
  if (unit === "score") {
    return `${formatted} pts`;
  }
  return formatted;
}

function unitLabel(unit: Unit) {
  if (unit === "percent") return "%";
  if (unit === "currency") return "$";
  if (unit === "minutes") return "min";
  if (unit === "meters") return "m";
  if (unit === "score") return "score";
  if (unit === "count") return "count";
  return "";
}

function numericDomain(data: RecordRow[], key: string, mode: DomainMode) {
  if (mode !== "tight") {
    return undefined;
  }
  const values = data.map((row) => Number(row[key])).filter(Number.isFinite);
  if (!values.length) {
    return undefined;
  }
  const min = Math.min(...values);
  const max = Math.max(...values);
  const spread = max - min;
  const pad = spread === 0 ? Math.max(Math.abs(max) * 0.02, 1) : spread * 0.18;
  return [Math.max(0, min - pad), max + pad] as [number, number];
}

const tooltipStyle = {
  border: "1px solid rgba(148, 163, 184, 0.28)",
  borderRadius: 14,
  boxShadow: "0 18px 50px rgba(15, 23, 42, 0.12)"
};

function CustomTooltip({
  active,
  payload,
  label: rawTooltipLabel,
  fullLabelKey,
  units
}: {
  active?: boolean;
  payload?: Array<{ name?: string; value?: string | number; dataKey?: string; payload?: RecordRow; color?: string }>;
  label?: string | number;
  fullLabelKey?: string;
  units: Record<string, Unit>;
}) {
  if (!active || !payload?.length) {
    return null;
  }
  const row = payload[0]?.payload;
  const displayLabel = fullLabelKey && row?.[fullLabelKey] ? String(row[fullLabelKey]) : label(rawTooltipLabel ?? "");
  return (
    <div className="chart-tooltip">
      <strong>{displayLabel}</strong>
      {payload.map((entry) => {
        const key = String(entry.dataKey ?? "");
        return (
          <span key={key}>
            <i style={{ background: entry.color }} />
            {entry.name ?? valueLabel(key)}: {metricValue(entry.value ?? "", units[key] ?? "none")}
          </span>
        );
      })}
    </div>
  );
}

export function SimpleBarChart({
  data,
  xKey,
  yKey,
  color = "#2563eb",
  yUnit = "none",
  fullLabelKey,
  angleLabels = false,
  yDomainMode = "zero"
}: {
  data: RecordRow[];
  xKey: string;
  yKey: string;
  color?: string;
  yUnit?: Unit;
  fullLabelKey?: string;
  angleLabels?: boolean;
  yDomainMode?: DomainMode;
}) {
  const yDomain = numericDomain(data, yKey, yDomainMode);
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 14, right: 18, left: 18, bottom: angleLabels ? 58 : 26 }}>
        <CartesianGrid stroke="#dbe7f6" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fontSize: 12, fill: "#667085" }} tickFormatter={label} tickLine={false} axisLine={false} angle={angleLabels ? -35 : 0} textAnchor={angleLabels ? "end" : "middle"} interval={0} />
        <YAxis domain={yDomain} tick={{ fontSize: 12, fill: "#667085" }} tickLine={false} axisLine={false} tickFormatter={(value) => metricValue(Number(value), yUnit)} label={unitLabel(yUnit) ? { value: unitLabel(yUnit), angle: -90, position: "insideLeft", style: { fontSize: 12, fill: "#667085" } } : undefined} />
        <Tooltip content={<CustomTooltip fullLabelKey={fullLabelKey} units={{ [yKey]: yUnit }} />} contentStyle={tooltipStyle} />
        <Bar dataKey={yKey} name={valueLabel(yKey)} fill={color} radius={[8, 8, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function MultiBarChart({
  data,
  xKey,
  bars,
  units = {},
  angleLabels = false
}: {
  data: RecordRow[];
  xKey: string;
  bars: string[];
  units?: Record<string, Unit>;
  angleLabels?: boolean;
}) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 14, right: 18, left: 18, bottom: angleLabels ? 58 : 26 }}>
        <CartesianGrid stroke="#dbe7f6" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fontSize: 12, fill: "#667085" }} tickFormatter={label} tickLine={false} axisLine={false} angle={angleLabels ? -35 : 0} textAnchor={angleLabels ? "end" : "middle"} interval={0} />
        <YAxis tick={{ fontSize: 12, fill: "#667085" }} tickLine={false} axisLine={false} />
        <Tooltip content={<CustomTooltip units={units} />} contentStyle={tooltipStyle} />
        <Legend />
        {bars.map((bar, index) => (
          <Bar key={bar} dataKey={bar} name={valueLabel(bar)} fill={colors[index % colors.length]} radius={[8, 8, 0, 0]} />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}

export function LineMetricChart({
  data,
  xKey,
  yKey,
  color = "#2563eb",
  yUnit = "none",
  angleLabels = false
}: {
  data: RecordRow[];
  xKey: string;
  yKey: string;
  color?: string;
  yUnit?: Unit;
  angleLabels?: boolean;
}) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data} margin={{ top: 14, right: 18, left: 18, bottom: angleLabels ? 58 : 26 }}>
        <CartesianGrid stroke="#dbe7f6" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fontSize: 12, fill: "#667085" }} tickFormatter={label} tickLine={false} axisLine={false} angle={angleLabels ? -35 : 0} textAnchor={angleLabels ? "end" : "middle"} interval={0} />
        <YAxis tick={{ fontSize: 12, fill: "#667085" }} tickLine={false} axisLine={false} tickFormatter={(value) => metricValue(Number(value), yUnit)} label={unitLabel(yUnit) ? { value: unitLabel(yUnit), angle: -90, position: "insideLeft", style: { fontSize: 12, fill: "#667085" } } : undefined} />
        <Tooltip content={<CustomTooltip units={{ [yKey]: yUnit }} />} contentStyle={tooltipStyle} />
        <Line dataKey={yKey} name={valueLabel(yKey)} stroke={color} strokeWidth={3} dot={{ r: 3 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function ComparisonChart({
  data,
  xKey,
  barKey,
  lineKey,
  barUnit = "none",
  lineUnit = "none",
  fullLabelKey,
  angleLabels = false,
  barDomainMode = "zero",
  lineDomainMode = "zero"
}: {
  data: RecordRow[];
  xKey: string;
  barKey: string;
  lineKey: string;
  barUnit?: Unit;
  lineUnit?: Unit;
  fullLabelKey?: string;
  angleLabels?: boolean;
  barDomainMode?: DomainMode;
  lineDomainMode?: DomainMode;
}) {
  const barDomain = numericDomain(data, barKey, barDomainMode);
  const lineDomain = numericDomain(data, lineKey, lineDomainMode);
  return (
    <ResponsiveContainer width="100%" height="100%">
      <ComposedChart data={data} margin={{ top: 14, right: 28, left: 18, bottom: angleLabels ? 86 : 42 }}>
        <CartesianGrid stroke="#dbe7f6" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fontSize: 12, fill: "#667085" }} tickFormatter={label} tickLine={false} axisLine={false} angle={angleLabels ? -35 : 0} textAnchor={angleLabels ? "end" : "middle"} interval={0} />
        <YAxis yAxisId="left" domain={barDomain} tick={{ fontSize: 12, fill: "#667085" }} tickLine={false} axisLine={false} tickFormatter={(value) => metricValue(Number(value), barUnit)} label={unitLabel(barUnit) ? { value: unitLabel(barUnit), angle: -90, position: "insideLeft", style: { fontSize: 12, fill: "#667085" } } : undefined} />
        <YAxis yAxisId="right" domain={lineDomain} orientation="right" tick={{ fontSize: 12, fill: "#667085" }} tickLine={false} axisLine={false} tickFormatter={(value) => metricValue(Number(value), lineUnit)} label={unitLabel(lineUnit) ? { value: unitLabel(lineUnit), angle: 90, position: "insideRight", style: { fontSize: 12, fill: "#667085" } } : undefined} />
        <Tooltip content={<CustomTooltip fullLabelKey={fullLabelKey} units={{ [barKey]: barUnit, [lineKey]: lineUnit }} />} contentStyle={tooltipStyle} />
        <Legend verticalAlign="top" align="center" wrapperStyle={{ paddingBottom: 12 }} />
        <Bar yAxisId="left" dataKey={barKey} name={valueLabel(barKey)} radius={[8, 8, 0, 0]}>
          {data.map((_, index) => (
            <Cell key={index} fill={colors[index % colors.length]} />
          ))}
        </Bar>
        <Line yAxisId="right" dataKey={lineKey} name={valueLabel(lineKey)} stroke="#0ea5e9" strokeWidth={3} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
