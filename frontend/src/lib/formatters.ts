export function formatDateTime(value: string): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("es-PE", {
    dateStyle: "short",
    timeStyle: "medium",
  }).format(date);
}

export function formatNumber(value: number, maximumFractionDigits = 2): string {
  return new Intl.NumberFormat("es-PE", {
    minimumFractionDigits: 0,
    maximumFractionDigits,
  }).format(value);
}

export function formatSeconds(value: number): string {
  return `${formatNumber(value, 4)} s`;
}

export function formatQOpt(values: number[]): string {
  return values.map((v) => formatNumber(v, 4)).join(", ");
}