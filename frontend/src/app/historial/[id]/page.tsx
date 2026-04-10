"use client";

import AppNav from "@/components/AppNav";
import {
  formatDateTime,
  formatNumber,
  formatQOpt,
  formatSeconds,
} from "@/lib/formatters";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type CorridaDetail = {
  id: string;
  created_at: string;
  fecha_proceso: string;
  modo_operacion: string;
  escenario: string;
  origen_datos: string;
  observaciones?: string | null;
  estado: string;
  version_modelo: string;
  modo_ejecucion: string;
  mensaje_modelo: string;
  best_cost: number;
  execution_time_sec: number;
  q_opt: number[];
  v_cincel: number[];
  v_campanario: number[];
  cmg: number[];
  potencia_ch4: number[];
  potencia_ch6: number[];
  ingreso: number[];
  input_payload_json: string;
  error_message?: string | null;
};

export default function CorridaDetailPage() {
  const params = useParams();
  const corridaId = Array.isArray(params.id) ? params.id[0] : params.id;

  const [data, setData] = useState<CorridaDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!corridaId) return;

    const fetchDetalle = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/corridas/${encodeURIComponent(
            corridaId
          )}`
        );

        if (!response.ok) {
          let message = `HTTP ${response.status}`;

          try {
            const errorJson = await response.json();
            if (errorJson?.detail) {
              message = String(errorJson.detail);
            }
          } catch {
            // mantener mensaje genérico
          }

          throw new Error(message);
        }

        const json = (await response.json()) as CorridaDetail;
        setData(json);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error desconocido");
      } finally {
        setLoading(false);
      }
    };

    fetchDetalle();
  }, [corridaId]);

  const qOptRows =
    data?.q_opt.map((value, index) => ({
      periodo: index + 1,
      valor: value,
    })) ?? [];

  const qOptChartData = qOptRows.map((row) => ({
    periodo: row.periodo,
    valor: Number(row.valor.toFixed(4)),
  }));

  const volumenesChartData =
    data?.v_cincel.map((value, index) => ({
      periodo: index,
      v_cincel: Number(value.toFixed(2)),
      v_campanario: Number((data.v_campanario[index] ?? 0).toFixed(2)),
    })) ?? [];

  const volumenResumen = data
    ? {
        cincel: {
          inicial: data.v_cincel[0] ?? 0,
          final: data.v_cincel[data.v_cincel.length - 1] ?? 0,
          minimo: data.v_cincel.length ? Math.min(...data.v_cincel) : 0,
          maximo: data.v_cincel.length ? Math.max(...data.v_cincel) : 0,
        },
        campanario: {
          inicial: data.v_campanario[0] ?? 0,
          final: data.v_campanario[data.v_campanario.length - 1] ?? 0,
          minimo: data.v_campanario.length
            ? Math.min(...data.v_campanario)
            : 0,
          maximo: data.v_campanario.length
            ? Math.max(...data.v_campanario)
            : 0,
        },
      }
    : null;

  const economicoChartData = data
    ? data.cmg.map((value, index) => ({
        periodo: index + 1,
        cmg: Number(value.toFixed(2)),
        potencia_ch4: Number((data.potencia_ch4[index] ?? 0).toFixed(2)),
        potencia_ch6: Number((data.potencia_ch6[index] ?? 0).toFixed(2)),
      }))
    : [];

  const ingresoChartData = data
    ? data.ingreso.map((value, index) => ({
        periodo: index + 1,
        ingreso: Number(value.toFixed(2)),
      }))
    : [];

  const ingresoResumen = data
  ? {
      total: data.ingreso.length ? data.ingreso.reduce((acc, value) => acc + value, 0) : 0,
      promedio: data.ingreso.length
        ? data.ingreso.reduce((acc, value) => acc + value, 0) / data.ingreso.length
        : 0,
      minimo: data.ingreso.length ? Math.min(...data.ingreso) : 0,
      maximo: data.ingreso.length ? Math.max(...data.ingreso) : 0,
    }
  : null;

  return (
    <>
      <AppNav />
      <main className="min-h-screen bg-slate-50 text-slate-900">
        <div className="mx-auto max-w-5xl px-6 py-12">
          <h1 className="text-3xl font-bold">Detalle de corrida</h1>
          <p className="mt-2 text-sm text-slate-600">
            Consulta detallada de una corrida específica.
          </p>

          {loading && (
            <div className="mt-6 rounded-xl border bg-white p-4 shadow-sm">
              Cargando detalle...
            </div>
          )}

          {error && (
            <div className="mt-6 rounded-xl border border-red-300 bg-red-50 p-4 text-red-700">
              Error al cargar detalle: {error}
            </div>
          )}

          {!loading && !error && data && (
            <>
              <div className="mt-2 text-sm text-slate-600">
                Estado actual:{" "}
                <span className="font-medium text-slate-900">{data.estado}</span>
              </div>

              <div className="mt-4 flex flex-wrap justify-end gap-3">
                <a
                  href={`${process.env.NEXT_PUBLIC_API_URL}/api/v1/corridas/${data.id}/export`}
                  className="rounded-lg border bg-white px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
                >
                  Exportar JSON
                </a>
                <a
                  href={`${process.env.NEXT_PUBLIC_API_URL}/api/v1/corridas/${data.id}/export/csv`}
                  className="rounded-lg border bg-white px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
                >
                  Exportar CSV
                </a>
                <a
                  href={`${process.env.NEXT_PUBLIC_API_URL}/api/v1/corridas/${data.id}/export/xlsx`}
                  className="rounded-lg border bg-white px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
                >
                  Exportar Excel
                </a>
              </div>

              <section className="mt-6 rounded-2xl border bg-white p-6 shadow-sm">
                <div className="grid grid-cols-1 gap-4 text-sm md:grid-cols-2">
                  <p>
                    <strong>ID:</strong> {data.id}
                  </p>
                  <p>
                    <strong>Creada:</strong> {formatDateTime(data.created_at)}
                  </p>
                  <p>
                    <strong>Fecha:</strong> {data.fecha_proceso}
                  </p>
                  <p>
                    <strong>Modo operación:</strong> {data.modo_operacion}
                  </p>
                  <p>
                    <strong>Escenario:</strong> {data.escenario}
                  </p>
                  <p>
                    <strong>Origen datos:</strong> {data.origen_datos}
                  </p>
                  <p>
                    <strong>Estado:</strong> {data.estado}
                  </p>
                  <p>
                    <strong>Versión modelo:</strong> {data.version_modelo}
                  </p>
                  <p>
                    <strong>Modo ejecución:</strong> {data.modo_ejecucion}
                  </p>
                  <p>
                    <strong>Best cost:</strong>{" "}
                    {formatNumber(data.best_cost, 2)}
                  </p>
                  <p>
                    <strong>Tiempo ejecución:</strong>{" "}
                    {formatSeconds(data.execution_time_sec)}
                  </p>
                </div>

                <div className="mt-6">
                  <h2 className="text-lg font-semibold">Observaciones</h2>
                  <div className="mt-2 rounded-lg border bg-slate-50 p-4 text-sm">
                    {data.observaciones ?? "-"}
                  </div>
                </div>

                <div className="mt-6">
                  <h2 className="text-lg font-semibold">Mensaje del modelo</h2>
                  <div className="mt-2 rounded-lg border bg-slate-50 p-4 text-sm">
                    {data.mensaje_modelo}
                  </div>
                </div>

                {data.error_message && (
                  <div className="mt-6">
                    <h2 className="text-lg font-semibold">Error de corrida</h2>
                    <div className="mt-2 rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-700">
                      {data.error_message}
                    </div>
                  </div>
                )}
              </section>

              <details
                className="mt-6 rounded-2xl border bg-white p-4 shadow-sm"
                open
              >
                <summary className="cursor-pointer text-lg font-semibold">
                  Q opt
                </summary>

                <div className="mt-4">
                  <div className="rounded-lg border bg-white p-4">
                    <div className="h-72 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={qOptChartData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="periodo" />
                          <YAxis />
                          <Tooltip />
                          <Line
                            type="monotone"
                            dataKey="valor"
                            strokeWidth={2}
                            dot={{ r: 2 }}
                            activeDot={{ r: 4 }}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="mt-4 overflow-x-auto rounded-lg border bg-white">
                    <table className="min-w-full border-collapse text-sm">
                      <thead>
                        <tr className="border-b bg-slate-100 text-left">
                          <th className="px-3 py-2">Periodo</th>
                          <th className="px-3 py-2">Valor</th>
                        </tr>
                      </thead>
                      <tbody>
                        {qOptRows.map((row) => (
                          <tr key={row.periodo} className="border-b">
                            <td className="px-3 py-2">{row.periodo}</td>
                            <td className="px-3 py-2">
                              {formatNumber(row.valor, 4)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  <details className="mt-4 rounded-lg border bg-slate-50 p-4 text-sm">
                    <summary className="cursor-pointer font-medium text-slate-700">
                      Ver serie completa en una sola línea
                    </summary>
                    <div className="mt-3 leading-7 break-words">
                      {formatQOpt(data.q_opt)}
                    </div>
                  </details>
                </div>
              </details>

              <details
                className="mt-6 rounded-2xl border bg-white p-4 shadow-sm"
                open
              >
                <summary className="cursor-pointer text-lg font-semibold">
                  Volúmenes de embalses
                </summary>

                <div className="mt-4">
                  <div className="rounded-lg border bg-white p-4">
                    <div className="h-80 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={volumenesChartData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="periodo" />
                          <YAxis />
                          <Tooltip />
                          <Line
                            type="monotone"
                            dataKey="v_cincel"
                            name="Dique Cincel"
                            strokeWidth={2}
                            dot={false}
                          />
                          <Line
                            type="monotone"
                            dataKey="v_campanario"
                            name="Dique Campanario"
                            strokeWidth={2}
                            dot={false}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {volumenResumen && (
                    <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
                      <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <h3 className="text-base font-semibold">Dique Cincel</h3>
                        <div className="mt-3 space-y-2 text-sm">
                          <p>
                            <strong>Inicial:</strong>{" "}
                            {formatNumber(volumenResumen.cincel.inicial, 2)}
                          </p>
                          <p>
                            <strong>Final:</strong>{" "}
                            {formatNumber(volumenResumen.cincel.final, 2)}
                          </p>
                          <p>
                            <strong>Mínimo:</strong>{" "}
                            {formatNumber(volumenResumen.cincel.minimo, 2)}
                          </p>
                          <p>
                            <strong>Máximo:</strong>{" "}
                            {formatNumber(volumenResumen.cincel.maximo, 2)}
                          </p>
                        </div>
                      </div>

                      <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <h3 className="text-base font-semibold">
                          Dique Campanario
                        </h3>
                        <div className="mt-3 space-y-2 text-sm">
                          <p>
                            <strong>Inicial:</strong>{" "}
                            {formatNumber(
                              volumenResumen.campanario.inicial,
                              2
                            )}
                          </p>
                          <p>
                            <strong>Final:</strong>{" "}
                            {formatNumber(volumenResumen.campanario.final, 2)}
                          </p>
                          <p>
                            <strong>Mínimo:</strong>{" "}
                            {formatNumber(volumenResumen.campanario.minimo, 2)}
                          </p>
                          <p>
                            <strong>Máximo:</strong>{" "}
                            {formatNumber(volumenResumen.campanario.maximo, 2)}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </details>

              <details className="mt-6 rounded-2xl border bg-white p-4 shadow-sm">
                <summary className="cursor-pointer text-lg font-semibold">
                  CMG vs potencia
                </summary>

                <div className="mt-4">
                  <div className="rounded-lg border bg-white p-4">
                    <div className="h-80 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={economicoChartData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="periodo" />
                          <YAxis
                            yAxisId="cmg"
                            orientation="left"
                            label={{ value: "CMG", angle: -90, position: "insideLeft" }}
                          />
                          <YAxis
                            yAxisId="potencia"
                            orientation="right"
                            label={{ value: "Potencia", angle: 90, position: "insideRight" }}
                          />
                          <Tooltip />
                          <Legend />
                          <Line
                            yAxisId="cmg"
                            type="monotone"
                            dataKey="cmg"
                            name="CMG"
                            strokeWidth={2}
                            dot={false}
                          />
                          <Line
                            yAxisId="potencia"
                            type="monotone"
                            dataKey="potencia_ch4"
                            name="Potencia CH4"
                            strokeWidth={2}
                            dot={false}
                          />
                          <Line
                            yAxisId="potencia"
                            type="monotone"
                            dataKey="potencia_ch6"
                            name="Potencia CH6"
                            strokeWidth={2}
                            dot={false}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </details>

              <details className="mt-6 rounded-2xl border bg-white p-4 shadow-sm">
                <summary className="cursor-pointer text-lg font-semibold">
                  Ingreso estimado por período
                </summary>

                <div className="mt-4">
                  {ingresoResumen && (
                    <div className="mb-4 grid grid-cols-1 gap-4 md:grid-cols-4">
                      <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <h3 className="text-sm font-semibold text-slate-600">Total</h3>
                        <p className="mt-2 text-lg font-semibold">
                          {formatNumber(ingresoResumen.total, 2)}
                        </p>
                      </div>

                      <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <h3 className="text-sm font-semibold text-slate-600">Promedio</h3>
                        <p className="mt-2 text-lg font-semibold">
                          {formatNumber(ingresoResumen.promedio, 2)}
                        </p>
                      </div>

                      <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <h3 className="text-sm font-semibold text-slate-600">Mínimo</h3>
                        <p className="mt-2 text-lg font-semibold">
                          {formatNumber(ingresoResumen.minimo, 2)}
                        </p>
                      </div>

                      <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <h3 className="text-sm font-semibold text-slate-600">Máximo</h3>
                        <p className="mt-2 text-lg font-semibold">
                          {formatNumber(ingresoResumen.maximo, 2)}
                        </p>
                      </div>
                    </div>
                  )}

                  <div className="rounded-lg border bg-white p-4">
                    <div className="h-80 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={ingresoChartData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="periodo" />
                          <YAxis />
                          <Tooltip />
                          <Line
                            type="monotone"
                            dataKey="ingreso"
                            name="Ingreso"
                            strokeWidth={2}
                            dot={false}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </details>

              <details className="mt-6 rounded-2xl border bg-white p-4 shadow-sm">
                <summary className="cursor-pointer text-lg font-semibold">
                  Input payload
                </summary>

                <div className="mt-4">
                  <pre className="overflow-x-auto rounded-lg border bg-slate-50 p-4 text-sm whitespace-pre-wrap break-words">
                    {data.input_payload_json}
                  </pre>
                </div>
              </details>
            </>
          )}
        </div>
      </main>
    </>
  );
}