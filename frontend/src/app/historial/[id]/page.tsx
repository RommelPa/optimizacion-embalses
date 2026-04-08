"use client";

import AppNav from "@/components/AppNav";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  formatDateTime,
  formatNumber,
  formatQOpt,
  formatSeconds,
} from "@/lib/formatters";

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
            <section className="mt-6 rounded-2xl border bg-white p-6 shadow-sm">
              <div className="grid grid-cols-1 gap-4 text-sm md:grid-cols-2">
                <p><strong>ID:</strong> {data.id}</p>
                <p><strong>Creada:</strong> {formatDateTime(data.created_at)}</p>
                <p><strong>Fecha:</strong> {data.fecha_proceso}</p>
                <p><strong>Modo operación:</strong> {data.modo_operacion}</p>
                <p><strong>Escenario:</strong> {data.escenario}</p>
                <p><strong>Origen datos:</strong> {data.origen_datos}</p>
                <p><strong>Estado:</strong> {data.estado}</p>
                <p><strong>Versión modelo:</strong> {data.version_modelo}</p>
                <p><strong>Modo ejecución:</strong> {data.modo_ejecucion}</p>
                <p><strong>Best cost:</strong> {formatNumber(data.best_cost, 2)}</p>
                <p><strong>Tiempo ejecución:</strong> {formatSeconds(data.execution_time_sec)}</p>
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

              <div className="mt-6">
                <h2 className="text-lg font-semibold">Q opt</h2>
                <div className="mt-2 rounded-lg border bg-slate-50 p-4 text-sm leading-7 break-words">
                  {formatQOpt(data.q_opt)}
                </div>
              </div>

              <div className="mt-6">
                <h2 className="text-lg font-semibold">Input payload</h2>
                <pre className="mt-2 overflow-x-auto rounded-lg border bg-slate-50 p-4 text-sm whitespace-pre-wrap break-words">
                    {data.input_payload_json}
                </pre>
               </div>
            </section>
          )}
        </div>
      </main>
    </>
  );
}