from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel


class GenerationMode(str, Enum):
    single = "single"
    ab_test = "ab_test"


class CopyStrategy(str, Enum):
    balanced = "balanced"
    conservative = "conservative"
    creative = "creative"


class HeroSection(BaseModel):
    headline: str
    subheadline: str
    primary_cta_text: str


class FeatureItem(BaseModel):
    title: str
    description: str


class SocialProofItem(BaseModel):
    quote: str
    source: str
    rating: Optional[float] = None


class FAQItem(BaseModel):
    question: str
    answer: str


class PageMetadata(BaseModel):
    title: str
    description: str


class LandingPageContent(BaseModel):
    hero: HeroSection
    features: List[FeatureItem]
    benefits: List[FeatureItem]
    social_proof: List[SocialProofItem]
    media_gallery: List[str]
    faq: List[FAQItem]
    metadata: PageMetadata


class CTAConfig(BaseModel):
    mode: Literal["install", "stripe_subscription"]
    text: str
    url: str
    message: str
    plan_id: Optional[str] = None


class CTAConfigInput(BaseModel):
    cta_mode: str
    google_play_url: str
    stripe_checkout_url: Optional[str] = None
    custom_cta_button_text: Optional[str] = None
    plan_id: Optional[str] = None


class ScreenshotSelection(BaseModel):
    hero_screenshot: Optional[str] = None
    gallery_screenshots: List[str]
    selection_reason: str


class MarketingInsights(BaseModel):
    target_audience: str
    value_proposition: str
    key_features: List[str]
    emotional_hooks: List[str]
    selected_reviews: List[str]
    tone: str
    hero_angle: str


class DesignDirection(BaseModel):
    theme: Literal["clean_light", "bold_gradient", "dark_premium", "playful"]
    hero_layout: Literal["split", "centered", "app_showcase"]
    section_style: Literal["cards", "minimal", "magazine"]
    visual_tone: str
    reason: str


class LandingPageVariant(BaseModel):
    variant_id: str
    variant_name: str
    strategy: CopyStrategy
    landing_page: LandingPageContent
    design_direction: Optional[DesignDirection] = None


class GenerateLandingPageRequest(BaseModel):
    googlePlayUrl: str
    ctaMode: Literal["install", "stripe_subscription"]
    generationMode: GenerationMode = GenerationMode.single
    stripeCheckoutUrl: Optional[str] = None
    customCtaButtonText: Optional[str] = None
    planId: Optional[str] = None


class FinalLandingPagePayload(BaseModel):
    app_name: str
    app_icon: Optional[str] = None
    google_play_url: str
    landing_page: Optional[LandingPageContent] = None
    variants: List[LandingPageVariant] = []
    cta: CTAConfig
    generation_mode: GenerationMode = GenerationMode.single
    screenshot_selection: Optional[ScreenshotSelection] = None