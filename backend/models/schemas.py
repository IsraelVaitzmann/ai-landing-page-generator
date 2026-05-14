from pydantic import BaseModel, Field
from typing import List, Optional
from typing import Literal


class AppReview(BaseModel):
    score: Optional[int] = None
    content: str


class RawAppData(BaseModel):
    title: str
    description: Optional[str] = None
    summary: Optional[str] = None
    score: Optional[float] = None
    ratings: Optional[int] = None
    installs: Optional[str] = None
    icon: Optional[str] = None
    screenshots: List[str] = []
    reviews: List[AppReview] = []


class HighlightReview(BaseModel):
    quote: str
    reason: str
    score: Optional[int] = None


class SelectedReview(BaseModel):
    user_review: str
    marketing_reason: str
    rating: Optional[int] = None


class MarketingInsights(BaseModel):
    target_audience: str = Field(description="The main audience most likely to convert")
    core_value_proposition: str = Field(description="One clear sentence explaining why users should care")
    top_features: List[str] = Field(description="The top 3-5 most marketable features")
    emotional_hooks: List[str] = Field(description="Emotional motivations that can be used in copy")
    best_reviews: List[SelectedReview] = Field(
        description="Real high-quality reviews selected for social proof"
    )
    landing_page_tone: str = Field(description="Recommended tone for the page")
    hero_angle: str = Field(description="The main angle for the hero section")

class HeroSection(BaseModel):
    headline: str
    subheadline: str
    primary_cta_text: str


class FeatureItem(BaseModel):
    title: str
    description: str


class BenefitItem(BaseModel):
    title: str
    description: str


class SocialProofItem(BaseModel):
    quote: str
    source: str = "Google Play Review"
    rating: Optional[int] = None


class FAQItem(BaseModel):
    question: str
    answer: str


class PageMetadata(BaseModel):
    title: str
    description: str


class LandingPageContent(BaseModel):
    hero: HeroSection
    features: List[FeatureItem]
    benefits: List[BenefitItem]
    social_proof: List[SocialProofItem]
    media_gallery: List[str]
    faq: List[FAQItem]
    metadata: PageMetadata

class CTAConfigInput(BaseModel):
    cta_mode: Literal["install", "stripe_subscription"]
    google_play_url: str
    stripe_checkout_url: Optional[str] = None
    custom_cta_button_text: Optional[str] = None
    plan_id: Optional[str] = None


class CTAConfig(BaseModel):
    mode: Literal["install", "stripe_subscription"]
    text: str
    url: str
    message: str
    plan_id: Optional[str] = None

class ScreenshotSelection(BaseModel):
    hero_screenshot: Optional[str] = None
    gallery_screenshots: List[str] = []
    selection_reason: str

class FinalLandingPagePayload(BaseModel):
    app_name: str
    app_icon: Optional[str] = None
    google_play_url: str
    landing_page: LandingPageContent
    cta: CTAConfig
    screenshot_selection: Optional[ScreenshotSelection] = None

class GenerateLandingPageRequest(BaseModel):
    googlePlayUrl: str
    ctaMode: Literal["install", "stripe_subscription"]
    stripeCheckoutUrl: Optional[str] = None
    customCtaButtonText: Optional[str] = None
    planId: Optional[str] = None

