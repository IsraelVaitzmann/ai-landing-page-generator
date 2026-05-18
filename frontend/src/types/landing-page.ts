export type CTAMode = "install" | "stripe_subscription";
export type GenerationMode = "single" | "ab_test";
export type CopyStrategy = "balanced" | "conservative" | "creative";

export type LandingPageVariant = {
  variant_id: string;
  variant_name: string;
  strategy: CopyStrategy;
  landing_page: LandingPageContent;
  design_direction?: DesignDirection | null;
};

export type CTAConfig = {
  mode: CTAMode;
  text: string;
  url: string;
  message: string;
  plan_id?: string | null;
};

export type HeroSection = {
  headline: string;
  subheadline: string;
  primary_cta_text: string;
};

export type FeatureItem = {
  title: string;
  description: string;
};

export type SocialProofItem = {
  quote: string;
  source: string;
  rating?: number | null;
};

export type FAQItem = {
  question: string;
  answer: string;
};

export type LandingPageContent = {
  hero: HeroSection;
  features: FeatureItem[];
  benefits: FeatureItem[];
  social_proof: SocialProofItem[];
  media_gallery: string[];
  faq: FAQItem[];
  metadata: {
    title: string;
    description: string;
  };
};

export type ScreenshotSelection = {
  hero_screenshot?: string | null;
  gallery_screenshots: string[];
  selection_reason: string;
};

export type FinalLandingPagePayload = {
  app_name: string;
  app_icon?: string | null;
  google_play_url: string;
  landing_page?: LandingPageContent | null;
  variants: LandingPageVariant[];
  cta: CTAConfig;
  generation_mode: GenerationMode;
  screenshot_selection?: ScreenshotSelection | null;
};

export type DesignDirection = {
  theme: "clean_light" | "bold_gradient" | "dark_premium" | "playful";
  hero_layout: "split" | "centered" | "app_showcase";
  section_style: "cards" | "minimal" | "magazine";
  visual_tone: string;
  reason: string;
};