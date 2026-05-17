import { currency, number, percent, titleize } from "@/lib/formatters";

type Row = Record<string, string | number | null>;

function formatCell(column: string, value: string | number | null) {
  if (value === null || value === undefined || value === "") {
    return "";
  }
  if (typeof value === "string") {
    return titleize(value);
  }

  if (column.includes("rate") || column.includes("pct") || column.includes("acceptance")) {
    return percent(value);
  }
  if (column.includes("minutes") || column.includes("time")) {
    return `${number(value, 1)} min`;
  }
  if (column.includes("price") || column.includes("margin") || column.includes("value") || column.includes("recovery") || column.includes("cost")) {
    return currency(value);
  }
  if (column.includes("score")) {
    return `${number(value, 1)} pts`;
  }
  if (column.includes("distance")) {
    return `${number(value, 1)} m`;
  }
  if (column.includes("count") || column.includes("rows") || column.includes("quotes") || column.includes("retrievals") || column.includes("scenarios")) {
    return `${number(value)} records`;
  }
  return number(value, Number.isInteger(value) ? 0 : 1);
}

export function DataTable({ rows, columns }: { rows: Row[]; columns: string[] }) {
  return (
    <div className="panel table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{titleize(column)}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column}>{formatCell(column, row[column])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
