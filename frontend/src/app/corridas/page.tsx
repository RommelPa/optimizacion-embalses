"use client";

import { FormEvent, useState } from "react";
import AppNav from "@/components/AppNav"

type CorridaResponse = {
  status: string;
  message: string;
  data: {
    id: string;
    estado: string;
    modo_operacion: string;
    fecha_proceso: string;
    escenario: string;
    origen_datos: string;
    observaciones?: string | null;
    version_modelo: string;
    modo_ejecucion: string;
    mensaje_modelo: string;
    best_cost: number;
    execution_time_sec: number;
    q_opt: number[];
  };
};

export default function CorridasPage() {
  const [modoOperacion, setModoOperacion] = useState("inicial");
  const [fechaProceso, setFechaProceso] = useState("2026-04-08");
  const [escenario, setEscenario] = useState("base");
  const [origenDatos, setOrigenDatos] = useState("manual");
  const [archivoEntrada, setArchivoEntrada] = useState("../data_samples/Datos_Entrada.xlsx");
  const [observaciones, setObservaciones] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<CorridaResponse | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/corridas`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
            body: JSON.stringify({
            modo_operacion: modoOperacion,
            fecha_proceso: fechaProceso,
            escenario,
            origen_datos: origenDatos,
            observaciones: observaciones || null,
            archivo_entrada: origenDatos === "excel" ? archivoEntrada : null,
            }),
        }
      );

      if (!response.ok) {
        let message = `HTTP ${response.status}`;

        try {
            const errorJson = await response.json();
            if (errorJson?.detail) {
            message = String(errorJson.detail);
            }
        } catch {
            // si no viene JSON válido, mantenemos el mensaje HTTP genérico
        }

        throw new Error(message);
      }

      const json = (await response.json()) as CorridaResponse;
      setResult(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
        <AppNav />
        <main className="min-h-screen bg-slate-50 text-slate-900">
        <div className="mx-auto max-w-3xl px-6 py-12">
            <h1 className="text-3xl font-bold">Crear corrida</h1>
            <p className="mt-2 text-sm text-slate-600">
            Formulario refinado para representar mejor una corrida operativa.
            </p>

            <form
            onSubmit={handleSubmit}
            className="mt-8 rounded-2xl border bg-white p-6 shadow-sm space-y-5"
            >
            <div>
                <label className="mb-2 block text-sm font-medium">Modo de operación</label>
                <select
                value={modoOperacion}
                onChange={(e) => setModoOperacion(e.target.value)}
                className="w-full rounded-lg border px-3 py-2"
                >
                <option value="inicial">inicial</option>
                <option value="reprograma">reprograma</option>
                </select>
            </div>

            <div>
                <label className="mb-2 block text-sm font-medium">Fecha de proceso</label>
                <input
                type="date"
                value={fechaProceso}
                onChange={(e) => setFechaProceso(e.target.value)}
                className="w-full rounded-lg border px-3 py-2"
                />
            </div>

            <div>
                <label className="mb-2 block text-sm font-medium">Escenario</label>
                <input
                type="text"
                value={escenario}
                onChange={(e) => setEscenario(e.target.value)}
                className="w-full rounded-lg border px-3 py-2"
                />
            </div>

            <div>
                <label className="mb-2 block text-sm font-medium">Origen de datos</label>
                <select
                value={origenDatos}
                onChange={(e) => setOrigenDatos(e.target.value)}
                className="w-full rounded-lg border px-3 py-2"
                >
                <option value="manual">manual</option>
                <option value="csv">csv</option>
                <option value="excel">excel</option>
                </select>

                {origenDatos === "excel" && (
                <div>
                    <label className="mb-2 block text-sm font-medium">Ruta del archivo de entrada</label>
                    <input
                    type="text"
                    value={archivoEntrada}
                    onChange={(e) => setArchivoEntrada(e.target.value)}
                    className="w-full rounded-lg border px-3 py-2"
                    placeholder="../data_samples/Datos_Entrada.xlsx"
                    />
                    <p className="mt-1 text-xs text-slate-500">
                    Ruta temporal de desarrollo. Aún no es carga real de archivo.
                    </p>
                </div>
                )}
            </div>

            <div>
                <label className="mb-2 block text-sm font-medium">Observaciones</label>
                <textarea
                value={observaciones}
                onChange={(e) => setObservaciones(e.target.value)}
                className="w-full rounded-lg border px-3 py-2"
                rows={3}
                />
            </div>

            <button
                type="submit"
                disabled={loading}
                className="rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-60"
            >
                {loading ? "Enviando..." : "Crear corrida"}
            </button>
            </form>

            {error && (
            <div className="mt-6 rounded-xl border border-red-300 bg-red-50 p-4 text-red-700">
                Error al crear la corrida: {error}
            </div>
            )}

            {result && (
            <section className="mt-6 rounded-2xl border bg-white p-6 shadow-sm">
                <h2 className="text-xl font-semibold">Respuesta del backend</h2>
                <div className="mt-4 space-y-2 text-sm">
                <p><strong>Status:</strong> {result.status}</p>
                <p><strong>Message:</strong> {result.message}</p>
                <p><strong>ID:</strong> {result.data.id}</p>
                <p><strong>Estado:</strong> {result.data.estado}</p>
                <p><strong>Modo operación:</strong> {result.data.modo_operacion}</p>
                <p><strong>Fecha:</strong> {result.data.fecha_proceso}</p>
                <p><strong>Escenario:</strong> {result.data.escenario}</p>
                <p><strong>Origen datos:</strong> {result.data.origen_datos}</p>
                <p><strong>Observaciones:</strong> {result.data.observaciones ?? "-"}</p>
                <p><strong>Versión modelo:</strong> {result.data.version_modelo}</p>
                <p><strong>Modo ejecución:</strong> {result.data.modo_ejecucion}</p>
                <p><strong>Mensaje modelo:</strong> {result.data.mensaje_modelo}</p>
                <p><strong>Best cost:</strong> {result.data.best_cost}</p>
                <p><strong>Tiempo ejecución (s):</strong> {result.data.execution_time_sec}</p>
                <p><strong>Q opt:</strong> {result.data.q_opt.join(", ")}</p>
                </div>
            </section>
            )}
        </div>
        </main>
    </>
  );
}