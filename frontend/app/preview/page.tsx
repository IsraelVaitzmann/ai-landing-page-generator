"use client";

import { useEffect, useState } from "react";
import { FinalLandingPagePayload } from "../../src/types/landing-page";
import { LandingPagePreview } from "../../src/components/LandingPagePreview";

export default function PreviewPage() {
  const [data, setData] = useState<FinalLandingPagePayload | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("generatedLandingPage");

    if (stored) {
      setData(JSON.parse(stored));
    }
  }, []);

  if (!data) {
    return (
      <main className="min-h-screen bg-slate-100 p-8 text-slate-950">
        <div className="mx-auto max-w-3xl rounded-3xl bg-white p-8 shadow-sm">
          <h1 className="text-2xl font-bold">No landing page found</h1>
          <p className="mt-2 text-slate-600">
            Generate a landing page first, then this preview will open here.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-8 md:px-8">
      <div className="mx-auto max-w-6xl">
        <LandingPagePreview data={data} />
      </div>
    </main>
  );
}