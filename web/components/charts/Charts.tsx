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

const colors = ["#257653", "#2563eb", "#b7791f", "#b42318", "#0f766e", "#6b7280"];

type RecordRow = Record<string, string | number>;
type Unit = "count" | "minutes" | "percent" | "currency" | "score" | "meters" | "none";

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

const tooltipStyle = {
  border: "1px solid #dce4dd",
  borderRadius: 8,
  boxShadow: "0 12px 28px rgba(23, 32, 26, 0.12)"
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
  color = "#257653",
  yUnit = "none",
  fullLabelKey,
  angleLabels = false
}: {
  data: RecordRow[];
  xKey: string;
  yKey: string;
  color?: string;
  yUnit?: Unit;
  fullLabelKey?: string;
  angleLabels?: boolean;
}) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={data} margin={{ top: 14, right: 18, left: 18, bottom: angleLabels ? 58 : 26 }}>
        <CartesianGrid stroke="#e5ece5" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fontSize: 12 }} tickFormatter={label} tickLine={false} axisLine={false} angle={angleLabels ? -35 : 0} textAnchor={angleLabels ? "end" : "middle"} interval={0} />
        <YAxis tick={{ fontSize: 12 }} tickLine={false} axisLine={false} tickFormatter={(value) => metricValue(Number(value), yUnit)} label={unitLabel(yUnit) ? { value: unitLabel(yUnit), angle: -90, position: "insideLeft", style: { fontSize: 12, fill: "#62706a" } } : undefined} />
        <Tooltip content={<CustomTooltip fullLabelKey={fullLabelKey} units={{ [yKey]: yUnit }} />} contentStyle={tooltipStyle} />
        <Bar dataKey={yKey} name={valueLabel(yKey)} fill={color} radius={[4, 4, 0, 0]} />
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
        <CartesianGrid stroke="#e5ece5" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fontSize: 12 }} tickFormatter={label} tickLine={false} axisLine={false} angle={angleLabels ? -35 : 0} textAnchor={angleLabels ? "end" : "middle"} interval={0} />
        <YAxis tick={{ fontSize: 12 }} tickLine={false} axisLine={false} />
        <Tooltip content={<CustomTooltip units={units} />} contentStyle={tooltipStyle} />
        <Legend />
        {bars.map((bar, index) => (
          <Bar key={bar} dataKey={bar} name={valueLabel(bar)} fill={colors[index % colors.length]} radius={[4, 4, 0, 0]} />
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
        <CartesianGrid stroke="#e5ece5" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fontSize: 12 }} tickFormatter={label} tickLine={false} axisLine={false} angle={angleLabels ? -35 : 0} textAnchor={angleLabels ? "end" : "middle"} interval={0} />
        <YAxis tick={{ fontSize: 12 }} tickLine={false} axisLine={false} tickFormatter={(value) => metricValue(Number(value), yUnit)} label={unitLabel(yUnit) ? { value: unitLabel(yUnit), angle: -90, position: "insideLeft", style: { fontSize: 12, fill: "#62706a" } } : undefined} />
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
  angleLabels = false
}: {
  data: RecordRow[];
  xKey: string;
  barKey: string;
  lineKey: string;
  barUnit?: Unit;
  lineUnit?: Unit;
  fullLabelKey?: string;
  angleLabels?: boolean;
}) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <ComposedChart data={data} margin={{ top: 14, right: 28, left: 18, bottom: angleLabels ? 86 : 42 }}>
        <CartesianGrid stroke="#e5ece5" vertical={false} />
        <XAxis dataKey={xKey} tick={{ fontSize: 12 }} tickFormatter={label} tickLine={false} axisLine={false} angle={angleLabels ? -35 : 0} textAnchor={angleLabels ? "end" : "middle"} interval={0} />
        <YAxis yAxisId="left" tick={{ fontSize: 12 }} tickLine={false} axisLine={false} tickFormatter={(value) => metricValue(Number(value), barUnit)} label={unitLabel(barUnit) ? { value: unitLabel(barUnit), angle: -90, position: "insideLeft", style: { fontSize: 12, fill: "#62706a" } } : undefined} />
        <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 12 }} tickLine={false} axisLine={false} tickFormatter={(value) => metricValue(Number(value), lineUnit)} label={unitLabel(lineUnit) ? { value: unitLabel(lineUnit), angle: 90, position: "insideRight", style: { fontSize: 12, fill: "#62706a" } } : undefined} />
        <Tooltip content={<CustomTooltip fullLabelKey={fullLabelKey} units={{ [barKey]: barUnit, [lineKey]: lineUnit }} />} contentStyle={tooltipStyle} />
        <Legend verticalAlign="top" align="center" wrapperStyle={{ paddingBottom: 12 }} />
        <Bar yAxisId="left" dataKey={barKey} name={valueLabel(barKey)} radius={[4, 4, 0, 0]}>
          {data.map((_, index) => (
            <Cell key={index} fill={colors[index % colors.length]} />
          ))}
        </Bar>
        <Line yAxisId="right" dataKey={lineKey} name={valueLabel(lineKey)} stroke="#0f766e" strokeWidth={3} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
