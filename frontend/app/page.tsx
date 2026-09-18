"use client";

import { useEffect, useState } from "react";

type CampaignStatus = {
  status: string;
  total: number;
  processed: number;
  sent: number;
  failed: number;
  current_lead: string | null;
  error: string | null;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<CampaignStatus>({
    status: "idle",
    total: 0,
    processed: 0,
    sent: 0,
    failed: 0,
    current_lead: null,
    error: null,
  });

  const [uploading, setUploading] = useState(false);
  const [starting, setStarting] = useState(false);
  const [message, setMessage] = useState("");

  async function uploadCSV() {
    if (!file) {
      setMessage("Please select a CSV file.");
      return;
    }

    setUploading(true);
    setMessage("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(
        `${API_URL}/api/campaign/upload`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Upload failed"
        );
      }

      setMessage(
        `Successfully loaded ${data.total_leads} leads.`
      );

      await fetchStatus();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Upload failed"
      );
    } finally {
      setUploading(false);
    }
  }

  async function startCampaign() {
    setStarting(true);
    setMessage("");

    try {
      const response = await fetch(
        `${API_URL}/api/campaign/start`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to start campaign"
        );
      }

      setMessage("Campaign started.");
      await fetchStatus();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Failed to start campaign"
      );
    } finally {
      setStarting(false);
    }
  }

  async function fetchStatus() {
    try {
      const response = await fetch(
        `${API_URL}/api/campaign/status`,
        {
          cache: "no-store",
        }
      );

      if (!response.ok) {
        return;
      }

      const data = await response.json();

      setStatus(data);
    } catch {
      // Backend may not be running.
    }
  }

  useEffect(() => {
    fetchStatus();

    const interval = setInterval(
      fetchStatus,
      2000
    );

    return () => clearInterval(interval);
  }, []);

  const progress =
    status.total > 0
      ? Math.round(
          (status.processed / status.total) * 100
        )
      : 0;

  const remaining =
    status.total - status.processed;

  const isRunning =
    status.status === "running";

  return (
    <main className="min-h-screen bg-zinc-950 text-white">
      <div className="mx-auto max-w-5xl px-6 py-12">

        {/* Header */}

        <div className="mb-10">
          <div className="mb-3 inline-flex rounded-full border border-zinc-800 bg-zinc-900 px-3 py-1 text-sm text-zinc-400">
            AI-powered outreach
          </div>

          <h1 className="text-4xl font-semibold tracking-tight">
            AI Email Agent
          </h1>

          <p className="mt-3 max-w-2xl text-zinc-400">
            Upload your leads, generate personalized
            emails with AI, and send your campaign
            through SendGrid.
          </p>
        </div>

        {/* Upload Section */}

        <section className="rounded-2xl border border-zinc-800 bg-zinc-900/60 p-6">

          <h2 className="text-xl font-medium">
            1. Upload leads
          </h2>

          <p className="mt-1 text-sm text-zinc-500">
            CSV must contain name, email, company,
            role, and company_description.
          </p>

          <div className="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center">

            <label className="flex cursor-pointer items-center justify-center rounded-xl border border-dashed border-zinc-700 bg-zinc-950 px-5 py-4 text-sm text-zinc-300 transition hover:border-zinc-500">

              <input
                type="file"
                accept=".csv"
                className="hidden"
                onChange={(event) => {
                  const selectedFile =
                    event.target.files?.[0];

                  if (selectedFile) {
                    setFile(selectedFile);
                    setMessage("");
                  }
                }}
              />

              {file
                ? file.name
                : "Choose CSV file"}
            </label>

            <button
              onClick={uploadCSV}
              disabled={!file || uploading}
              className="rounded-xl bg-white px-5 py-3 text-sm font-medium text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {uploading
                ? "Uploading..."
                : "Upload CSV"}
            </button>

          </div>
        </section>

        {/* Campaign */}

        <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900/60 p-6">

          <div className="flex items-center justify-between">

            <div>
              <h2 className="text-xl font-medium">
                2. Campaign
              </h2>

              <p className="mt-1 text-sm text-zinc-500">
                Start the AI outreach campaign.
              </p>
            </div>

            <button
              onClick={startCampaign}
              disabled={
                status.total === 0 ||
                isRunning ||
                starting
              }
              className="rounded-xl bg-white px-5 py-3 text-sm font-medium text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {starting
                ? "Starting..."
                : isRunning
                ? "Campaign Running"
                : "Start Campaign"}
            </button>

          </div>

        </section>

        {/* Status */}

        <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900/60 p-6">

          <div className="flex items-center justify-between">

            <h2 className="text-xl font-medium">
              Campaign Status
            </h2>

            <span className="rounded-full bg-zinc-800 px-3 py-1 text-xs uppercase tracking-wide text-zinc-400">
              {status.status}
            </span>

          </div>

          {/* Progress */}

          <div className="mt-8">

            <div className="mb-3 flex justify-between text-sm">

              <span className="text-zinc-400">
                Progress
              </span>

              <span className="text-zinc-300">
                {status.processed} /{" "}
                {status.total}
              </span>

            </div>

            <div className="h-3 overflow-hidden rounded-full bg-zinc-800">

              <div
                className="h-full rounded-full bg-white transition-all duration-500"
                style={{
                  width: `${progress}%`,
                }}
              />

            </div>

            <div className="mt-2 text-right text-sm text-zinc-500">
              {progress}%
            </div>

          </div>

          {/* Stats */}

          <div className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-4">

            <Stat
              label="Total"
              value={status.total}
            />

            <Stat
              label="Sent"
              value={status.sent}
            />

            <Stat
              label="Failed"
              value={status.failed}
            />

            <Stat
              label="Remaining"
              value={remaining}
            />

          </div>

          {/* Current lead */}

          {status.current_lead && (
            <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-950 p-4">

              <p className="text-xs uppercase tracking-wide text-zinc-500">
                Currently processing
              </p>

              <p className="mt-1 text-sm text-zinc-200">
                {status.current_lead}
              </p>

            </div>
          )}

        </section>

        {/* Message */}

        {message && (
          <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-4 text-sm text-zinc-300">
            {message}
          </div>
        )}

        {/* Error */}

        {status.error && (
          <div className="mt-6 rounded-xl border border-red-900/50 bg-red-950/30 p-4 text-sm text-red-300">
            {status.error}
          </div>
        )}

      </div>
    </main>
  );
}


function Stat({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-950 p-4">

      <p className="text-sm text-zinc-500">
        {label}
      </p>

      <p className="mt-2 text-2xl font-semibold">
        {value}
      </p>

    </div>
  );
}