from agents.marketing_agent import analyze_marketing
from agents.copywriter_agent import generate_landing_page_content
from agents.cta_agent import generate_cta_config
from models.schemas import (
    CTAConfigInput,
    FinalLandingPagePayload,
    GenerateLandingPageRequest,
)
from services.playstore_service import extract_app_data


def generate_landing_page_workflow(
    request: GenerateLandingPageRequest,
) -> FinalLandingPagePayload:
    if request.ctaMode == "stripe_subscription" and not request.stripeCheckoutUrl:
        raise ValueError("stripeCheckoutUrl is required when ctaMode is stripe_subscription")
    print("1. Starting workflow")
    app_data = extract_app_data(request.googlePlayUrl)
    print("2. App data extracted")
    marketing_insights = analyze_marketing(app_data)
    print("3. Marketing insights analyzed")

    landing_page = generate_landing_page_content(
        app_data=app_data,
        marketing_insights=marketing_insights.model_dump(),
        cta_mode=request.ctaMode,
    )
    print("4. Landing page content generated")
    cta = generate_cta_config(
        CTAConfigInput(
            cta_mode=request.ctaMode,
            google_play_url=request.googlePlayUrl,
            stripe_checkout_url=request.stripeCheckoutUrl,
            custom_cta_button_text=request.customCtaButtonText,
            plan_id=request.planId,
        )
    )
    print("5. CTA config generated")
    return FinalLandingPagePayload(
        app_name=app_data["title"],
        app_icon=app_data.get("icon"),
        google_play_url=request.googlePlayUrl,
        landing_page=landing_page,
        cta=cta,
    )