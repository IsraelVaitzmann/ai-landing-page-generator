import { CTAMode, FinalLandingPagePayload } from "../types/landing-page";

export type GenerateLandingPageRequest = {
  googlePlayUrl: string;
  ctaMode: CTAMode;
  stripeCheckoutUrl?: string;
  customCtaButtonText?: string;
  planId?: string;
};

export async function generateLandingPage(
  payload: GenerateLandingPageRequest
): Promise<FinalLandingPagePayload> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  if (!apiUrl) {
    throw new Error("NEXT_PUBLIC_API_URL is not configured");
  }

  const response = await fetch(`${apiUrl}/generate-landing-page`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => null);
    throw new Error(error?.detail || "Failed to generate landing page");
  }

  return response.json();
}