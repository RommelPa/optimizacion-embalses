"use client";

import { useEffect, useState } from "react";
import AppNav from "@/components/AppNav";

type HealthResponse = {
  status: string;
  service: string;
  version: string;
};

export default function Home() {
  const [data, setData] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/health`
        );

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const json = (await response.json()) as HealthResponse;
        setData(json);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Error desconocido");
      }
    };

    fetchHealth();
  }, []);

  return (
    <>
      <AppNav />
      <main className="min-h-screen bg-slate-50 text-slate-900">
        <div className="mx-auto max-w-3xl px-6 py-12">
          <h1 className="text-3xl font-bold">
            Optimizacion de Embalses - V1
          </h1>
          <p className="mt-2 text-sm text-slate-600">
            Primera verificacion de conexion entre frontend y backend.
          </p>

          <section className="mt-8 rounded-2xl border bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold">Estado del backend</h2>

            {error && (
              <div className="mt-4 rounded-lg border border-red-300 bg-red-50 p-4 text-red-700">
                Error al conectar con el backend: {error}
              </div>
            )}

            {!error && !data && (
              <div className="mt-4 rounded-lg border border-slate-200 bg-slate-100 p-4">
                Consultando backend...
              </div>
            )}

            {data && (
              <div className="mt-4 rounded-lg border border-green-300 bg-green-50 p-4">
                <p>
                  <strong>Status:</strong> {data.status}
                </p>
                <p>
                  <strong>Service:</strong> {data.service}
                </p>
                <p>
                  <strong>Version:</strong> {data.version}
                </p>
              </div>
            )}
          </section>
        </div>
      </main>
    </>
  );
}