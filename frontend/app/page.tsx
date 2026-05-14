"use client";

import { FormEvent, useEffect, useState } from "react";
import { generateLandingPage } from "../src/lib/api";
import { CTAMode, FinalLandingPagePayload } from "../src/types/landing-page";
import { LandingPagePreview } from "../src/components/LandingPagePreview";

const STRIPE_CHECKOUT_URL = "https://buy.stripe.com/test_00w28rforcdd95H8HX6Vq00";

const loadingSteps = [
  "Extracting Google Play app data",
  "Analyzing reviews and value proposition",
  "Selecting strongest screenshots",
  "Generating landing page copy",
  "Configuring CTA behavior",
];

function CircularProgress({
  progress,
  label,
}: {
  progress: number;
  label: string;
}) {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center rounded-3xl border bg-white p-6 shadow-sm">
      <div className="relative h-28 w-28">
        <svg className="h-28 w-28 -rotate-90">
          <circle
            cx="56"
            cy="56"
            r={radius}
            stroke="currentColor"
            strokeWidth="10"
            fill="transparent"
            className="text-slate-200"
          />
          <circle
            cx="56"
            cy="56"
            r={radius}
            stroke="currentColor"
            strokeWidth="10"
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="text-blue-600 transition-all duration-700"
          />
        </svg>

        <div className="absolute inset-0 flex items-center justify-center text-sm font-black">
          {progress}%
        </div>
      </div>

      <p className="mt-4 text-center text-sm font-bold text-slate-900">
        {label}
      </p>
    </div>
  );
}

export default function Home() {
  const [googlePlayUrl, setGooglePlayUrl] = useState(
    "https://play.google.com/store/apps/details?id=com.spotify.music"
  );

  const [ctaMode, setCtaMode] = useState<CTAMode>("install");
  const [result, setResult] = useState<FinalLandingPagePayload | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [loading, setLoading] = useState(false);
  const [seconds, setSeconds] = useState(0);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    if (!loading) return;

    const interval = setInterval(() => {
      setSeconds((value) => value + 1);
      setCurrentStepIndex((value) =>
        value < loadingSteps.length - 1 ? value + 1 : value
      );
    }, 2500);

    return () => clearInterval(interval);
  }, [loading]);

  const progress = loading
    ? Math.min(
        95,
        Math.round(((currentStepIndex + 1) / loadingSteps.length) * 100)
      )
    : result
      ? 100
      : 0;

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setLoading(true);
    setError(null);
    setResult(null);
    setSeconds(0);
    setCurrentStepIndex(0);

    try {
      const data = await generateLandingPage({
        googlePlayUrl,
        ctaMode,
        stripeCheckoutUrl:
          ctaMode === "stripe_subscription" ? STRIPE_CHECKOUT_URL : undefined,
        customCtaButtonText:
          ctaMode === "stripe_subscription" ? "Start Premium" : undefined,
        planId: ctaMode === "stripe_subscription" ? "pro_monthly" : undefined,
      });

      localStorage.setItem("generatedLandingPage", JSON.stringify(data));
      setResult(data);
      setCurrentStepIndex(loadingSteps.length - 1);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  function openLandingPage() {
    const stored = localStorage.getItem("generatedLandingPage");

    if (!stored) {
      setError("Landing page data was not found. Please generate again.");
      return;
    }

    window.open("/preview", "_blank", "noopener,noreferrer");
  }

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top_left,#dbeafe,transparent_35%),linear-gradient(to_bottom,#f8fafc,#e2e8f0)] px-4 py-8 text-slate-950 md:px-8">
      <div className="mx-auto max-w-6xl">
        <section className="mb-8 rounded-[2rem] border border-white/70 bg-white/90 p-8 shadow-xl md:p-12">
          <p className="text-sm font-black uppercase tracking-[0.25em] text-blue-700">
            AI Agent Developer Assignment
          </p>

          <h1 className="mt-4 text-4xl font-black tracking-tight md:text-6xl">
            Automated Landing Page Generator
          </h1>

          <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-600">
            Generate a mobile app landing page from a Google Play URL using a
            multi-agent AI workflow with dynamic CTA logic.
          </p>

        </section>

        <form
          onSubmit={onSubmit}
          className="rounded-[2rem] border border-white/70 bg-white/95 p-6 shadow-xl md:p-8"
        >
          <div className="grid gap-5">
            <div>
              <label className="text-sm font-bold text-slate-700">
                Google Play URL
              </label>

              <input
                value={googlePlayUrl}
                onChange={(event) => setGooglePlayUrl(event.target.value)}
                className="mt-2 w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none focus:border-slate-950 focus:ring-4 focus:ring-slate-200"
              />
            </div>

            <div>
              <label className="text-sm font-bold text-slate-700">
                CTA Mode
              </label>

              <select
                value={ctaMode}
                onChange={(event) => setCtaMode(event.target.value as CTAMode)}
                className="mt-2 w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none focus:border-slate-950 focus:ring-4 focus:ring-slate-200"
              >
                <option value="install">Install / Google Play</option>
                <option value="stripe_subscription">
                  Stripe Subscription
                </option>
              </select>

              <div className="mt-3 rounded-2xl bg-slate-50 p-4 text-sm text-slate-600">
                {ctaMode === "install" ? (
                  <p>
                    The generated landing page CTA will send users directly to
                    the Google Play Store.
                  </p>
                ) : (
                  <p>
                    The generated landing page CTA will become a subscription
                    CTA and redirect users to Stripe Checkout.
                  </p>
                )}
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="rounded-2xl bg-slate-950 px-6 py-4 font-black text-white shadow-lg transition hover:-translate-y-0.5 hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Generating..." : "Generate Landing Page"}
            </button>
          </div>

          {loading && (
            <div className="mt-6 grid gap-5 rounded-3xl border bg-slate-50 p-5 md:grid-cols-[220px_1fr]">
              <CircularProgress
                progress={progress}
                label={loadingSteps[currentStepIndex]}
              />

              <div>
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-black">Processing pipeline</h3>
                  <span className="rounded-full bg-slate-950 px-3 py-1 text-sm font-bold text-white">
                    {seconds}s
                  </span>
                </div>

                <div className="mt-5 space-y-3">
                  {loadingSteps.map((step, index) => (
                    <div
                      key={step}
                      className={`rounded-2xl border p-4 text-sm font-semibold ${
                        index <= currentStepIndex
                          ? "border-blue-200 bg-blue-50 text-blue-900"
                          : "bg-white text-slate-500"
                      }`}
                    >
                      {index + 1}. {step}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {result && !loading && (
            <div className="mt-6 rounded-3xl border border-emerald-200 bg-emerald-50 p-6">
              <h3 className="text-xl font-black text-emerald-950">
                Landing page is ready
              </h3>

              <p className="mt-2 text-sm text-emerald-800">
                CTA mode:{" "}
                <span className="font-bold">
                  {result.cta.mode === "install"
                    ? "Google Play Install"
                    : "Stripe Subscription"}
                </span>
              </p>

              <p className="mt-1 text-sm text-emerald-800">
                CTA destination:{" "}
                <span className="font-bold break-all">{result.cta.url}</span>
              </p>

              <button
                type="button"
                onClick={openLandingPage}
                className="mt-4 rounded-2xl bg-emerald-700 px-6 py-3 font-bold text-white transition hover:bg-emerald-800"
              >
                Open Landing Page
              </button>
            </div>
          )}

          {error && (
            <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
              {error}
            </div>
          )}
        </form>
      </div>
    </main>
  );
}