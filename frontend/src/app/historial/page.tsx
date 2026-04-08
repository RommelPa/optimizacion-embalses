"use client";

import { useEffect, useState } from "react";
import AppNav from "@/components/AppNav";
import Link from "next/link";
import { formatDateTime, formatNumber, formatSeconds } from "@/lib/formatters";

type CorridaListItem = {
  id: string;
  created_at: string;
  fecha_proceso: string;
  modo_operacion: string;
  escenario: string;
  origen_datos: string;
  estado: string;
  version_modelo: string;
  modo_ejecucion: string;
  best_cost: number;
  execution_time_sec: number;
};

type CorridasListResponse = {
  items: CorridaListItem[];
  total: number;
};

export default function HistorialPage() {
  const [data, setData] = useState<CorridasListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filterOrigen, setFilterOrigen] = useState("todos");
  const [filterEstado, setFilterEstado] = useState("todos");
  const [filterId, setFilterId] = useState("");
  const [filterFechaProceso, setFilterFechaProceso] = useState("");
  const handleClearFilters = () => {
  setFilterOrigen("todos");
  setFilterEstado("todos");
  setFilterId("");
  setFilterFechaProceso("");
};

  useEffect(() => {
  const fetchHistorial = async () => {
    try {
      setLoading(true);
      setError("");

      const params = new URLSearchParams();

      if (filterOrigen !== "todos") {
        params.set("origen_datos", filterOrigen);
      }

      if (filterEstado !== "todos") {
        params.set("estado", filterEstado);
      }

      if (filterFechaProceso.trim() !== "") {
        params.set("fecha_proceso", filterFechaProceso.trim());
      }

      if (filterId.trim() !== "") {
        params.set("id_contains", filterId.trim());
      }

      const queryString = params.toString();
      const url = `${process.env.NEXT_PUBLIC_API_URL}/api/v1/corridas${
        queryString ? `?${queryString}` : ""
      }`;

      const response = await fetch(url);

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

      const json = (await response.json()) as CorridasListResponse;
      setData(json);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error desconocido");
    } finally {
      setLoading(false);
    }
  };

  fetchHistorial();
}, [filterOrigen, filterEstado, filterId, filterFechaProceso]);

const stats = {
  total: data?.items.length ?? 0,
  completadas:
    data?.items.filter((item) => item.estado === "completada").length ?? 0,
  fallidas:
    data?.items.filter((item) => item.estado === "fallida").length ?? 0,
  manual:
    data?.items.filter((item) => item.origen_datos === "manual").length ?? 0,
  excel:
    data?.items.filter((item) => item.origen_datos === "excel").length ?? 0,
};

  return (
    <>
        <AppNav />
        <main className="min-h-screen bg-slate-50 text-slate-900">
        <div className="mx-auto max-w-6xl px-6 py-12">
            <h1 className="text-3xl font-bold">Historial de corridas</h1>
            <p className="mt-2 text-sm text-slate-600">
            Consulta básica de corridas registradas en la base local.
            </p>

            {loading && (
            <div className="mt-6 rounded-xl border bg-white p-4 shadow-sm">
                Cargando historial...
            </div>
            )}

            {error && (
            <div className="mt-6 rounded-xl border border-red-300 bg-red-50 p-4 text-red-700">
                Error al cargar historial: {error}
            </div>
            )}

            {!loading && !error && data && (
            <section className="mt-6 rounded-2xl border bg-white p-6 shadow-sm">
                <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-5">
                    <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <p className="text-sm text-slate-600">Total mostrado</p>
                        <p className="mt-2 text-2xl font-bold">{stats.total}</p>
                    </div>

                    <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <p className="text-sm text-slate-600">Completadas</p>
                        <p className="mt-2 text-2xl font-bold">{stats.completadas}</p>
                    </div>

                    <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <p className="text-sm text-slate-600">Fallidas</p>
                        <p className="mt-2 text-2xl font-bold">{stats.fallidas}</p>
                    </div>

                    <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <p className="text-sm text-slate-600">Manual</p>
                        <p className="mt-2 text-2xl font-bold">{stats.manual}</p>
                    </div>

                    <div className="rounded-2xl border bg-white p-4 shadow-sm">
                        <p className="text-sm text-slate-600">Excel</p>
                        <p className="mt-2 text-2xl font-bold">{stats.excel}</p>
                    </div>
                </div>
                <div className="mt-6 rounded-2xl border bg-white p-4 shadow-sm">
                    <div className="mb-4 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                        <div>
                        <h2 className="text-lg font-semibold">Filtros</h2>
                        <p className="text-sm text-slate-600">
                            Refina el historial por origen, estado, fecha o identificador.
                        </p>
                        </div>

                        <button
                        type="button"
                        onClick={handleClearFilters}
                        className="rounded-lg border px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
                        >
                        Limpiar filtros
                        </button>
                    </div>

                    <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
                        <div>
                        <label className="mb-2 block text-sm font-medium">Filtrar por origen</label>
                        <select
                            value={filterOrigen}
                            onChange={(e) => setFilterOrigen(e.target.value)}
                            className="w-full rounded-lg border px-3 py-2"
                        >
                            <option value="todos">Todos</option>
                            <option value="manual">manual</option>
                            <option value="excel">excel</option>
                            <option value="csv">csv</option>
                        </select>
                        </div>

                        <div>
                        <label className="mb-2 block text-sm font-medium">Filtrar por estado</label>
                        <select
                            value={filterEstado}
                            onChange={(e) => setFilterEstado(e.target.value)}
                            className="w-full rounded-lg border px-3 py-2"
                        >
                            <option value="todos">Todos</option>
                            <option value="completada">completada</option>
                            <option value="fallida">fallida</option>
                        </select>
                        </div>

                        <div>
                        <label className="mb-2 block text-sm font-medium">Buscar por ID</label>
                        <input
                            type="text"
                            value={filterId}
                            onChange={(e) => setFilterId(e.target.value)}
                            placeholder="Parte del ID"
                            className="w-full rounded-lg border px-3 py-2"
                        />
                        </div>

                        <div>
                        <label className="mb-2 block text-sm font-medium">Filtrar por fecha</label>
                        <input
                            type="date"
                            value={filterFechaProceso}
                            onChange={(e) => setFilterFechaProceso(e.target.value)}
                            className="w-full rounded-lg border px-3 py-2"
                        />
                        </div>
                    </div>
                </div>
                <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-semibold">Corridas registradas</h2>
                <span className="text-sm text-slate-600">
                    Mostrando: {data.total} resultado(s)
                </span>
                </div>

                {data.items.length === 0 ? (
                <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
                    No hay corridas registradas.
                </div>
                ) : (
                <div className="overflow-x-auto">
                    <table className="min-w-full border-collapse text-sm">
                    <thead>
                        <tr className="border-b bg-slate-100 text-left">
                        <th className="px-3 py-2">ID</th>
                        <th className="px-3 py-2">Creada</th>
                        <th className="px-3 py-2">Fecha</th>
                        <th className="px-3 py-2">Modo</th>
                        <th className="px-3 py-2">Escenario</th>
                        <th className="px-3 py-2">Origen</th>
                        <th className="px-3 py-2">Estado</th>
                        <th className="px-3 py-2">Modelo</th>
                        <th className="px-3 py-2">Ejecución</th>
                        <th className="px-3 py-2">Best cost</th>
                        <th className="px-3 py-2">Tiempo (s)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.items.map((item) => (
                        <tr key={item.id} className="border-b">
                            <td className="px-3 py-2">
                            <Link
                                href={`/historial/${item.id}`}
                                className="text-blue-600 underline hover:text-blue-800"
                            >
                                {item.id}
                            </Link>
                            </td>
                            <td className="px-3 py-2">{formatDateTime(item.created_at)}</td>
                            <td className="px-3 py-2">{item.fecha_proceso}</td>
                            <td className="px-3 py-2">{item.modo_operacion}</td>
                            <td className="px-3 py-2">{item.escenario}</td>
                            <td className="px-3 py-2">{item.origen_datos}</td>
                            <td className="px-3 py-2">{item.estado}</td>
                            <td className="px-3 py-2">{item.version_modelo}</td>
                            <td className="px-3 py-2">{item.modo_ejecucion}</td>
                            <td className="px-3 py-2">{formatNumber(item.best_cost, 2)}</td>
                            <td className="px-3 py-2">{formatSeconds(item.execution_time_sec)}</td>
                        </tr>
                        ))}
                    </tbody>
                    </table>
                </div>
                )}
            </section>
            )}
        </div>
        </main>
    </>
  );
}