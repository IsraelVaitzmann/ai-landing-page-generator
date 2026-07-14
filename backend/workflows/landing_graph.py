import logging
import os
from typing import Optional, TypedDict

from langgraph.graph import END, START, StateGraph
from agents.screenshot_agent import select_screenshots
from agents.marketing_agent import analyze_marketing
from agents.copywriter_agent import generate_landing_page_content
from agents.cta_agent import generate_cta_config
from models.schemas import (
    CTAConfig,
    CTAConfigInput,
    CopyStrategy,
    FinalLandingPagePayload,
    GenerateLandingPageRequest,
    GenerationMode,
    LandingPageContent,
    LandingPageVariant,
    MarketingInsights,
    ScreenshotSelection,
)
from services.playstore_service import extract_app_data

logger = logging.getLogger(__name__)


class LandingGraphState(TypedDict, total=False):
    request: GenerateLandingPageRequest
    app_data: dict
    marketing_insights: MarketingInsights
    screenshot_selection: ScreenshotSelection
    landing_page: LandingPageContent
    variants: list[LandingPageVariant]
    cta: CTAConfig
    final_payload: FinalLandingPagePayload

def extraction_node(state: LandingGraphState) -> LandingGraphState:
    logger.info("Graph node started: extraction")

    request = state["request"]
    try:
        app_data = extract_app_data(request.googlePlayUrl)
    except Exception:
        logger.exception("Graph node failed: extraction")
        raise

    logger.info("Graph node finished: extraction (app=%s)", app_data.get("title"))
    return {
        "app_data": app_data,
    }

def marketing_node(state: LandingGraphState) -> LandingGraphState:
    logger.info("Graph node started: marketing")

    app_data = state["app_data"]
    try:
        marketing_insights = analyze_marketing(app_data)
    except Exception:
        logger.exception("Graph node failed: marketing")
        raise

    logger.info("Graph node finished: marketing")
    return {
        "marketing_insights": marketing_insights,
    }

def copywriter_node(state: LandingGraphState) -> LandingGraphState:
    logger.info("Graph node started: copywriter")

    request = state["request"]
    app_data = state["app_data"]
    marketing_insights = state["marketing_insights"]
    screenshot_selection = state["screenshot_selection"]

    try:
        if request.generationMode == GenerationMode.ab_test:
            conservative_page = generate_landing_page_content(
                app_data=app_data,
                marketing_insights=marketing_insights.model_dump(),
                cta_mode=request.ctaMode,
                selected_screenshots=screenshot_selection.gallery_screenshots,
                strategy=CopyStrategy.conservative,
            )

            creative_page = generate_landing_page_content(
                app_data=app_data,
                marketing_insights=marketing_insights.model_dump(),
                cta_mode=request.ctaMode,
                selected_screenshots=screenshot_selection.gallery_screenshots,
                strategy=CopyStrategy.creative,
            )
        else:
            landing_page = generate_landing_page_content(
                app_data=app_data,
                marketing_insights=marketing_insights.model_dump(),
                cta_mode=request.ctaMode,
                selected_screenshots=screenshot_selection.gallery_screenshots,
                strategy=CopyStrategy.balanced,
            )
    except Exception:
        logger.exception("Graph node failed: copywriter")
        raise

    logger.info("Graph node finished: copywriter")

    if request.generationMode == GenerationMode.ab_test:
        return {
            "variants": [
                LandingPageVariant(
                    variant_id="a",
                    variant_name="Variant A — Conservative",
                    strategy=CopyStrategy.conservative,
                    landing_page=conservative_page,
                ),
                LandingPageVariant(
                    variant_id="b",
                    variant_name="Variant B — Creative",
                    strategy=CopyStrategy.creative,
                    landing_page=creative_page,
                ),
            ]
        }

    return {
        "landing_page": landing_page,
    }

def cta_node(state: LandingGraphState) -> LandingGraphState:
    logger.info("Graph node started: cta")

    request = state["request"]

    try:
        cta = generate_cta_config(
            CTAConfigInput(
                cta_mode=request.ctaMode,
                google_play_url=request.googlePlayUrl,
                stripe_checkout_url=request.stripeCheckoutUrl,
                custom_cta_button_text=request.customCtaButtonText,
                plan_id=request.planId,
            )
        )
    except Exception:
        logger.exception("Graph node failed: cta")
        raise

    logger.info("Graph node finished: cta")
    return {
        "cta": cta,
    }

def screenshot_selection_node(state: LandingGraphState) -> LandingGraphState:
    logger.info("Graph node started: screenshot_selection")

    app_data = state["app_data"]
    marketing_insights = state["marketing_insights"]

    try:
        screenshot_selection = select_screenshots(
            screenshots=app_data.get("screenshots", []),
            marketing_insights=marketing_insights,
        )
    except Exception:
        logger.exception("Graph node failed: screenshot_selection")
        raise

    logger.info("Graph node finished: screenshot_selection")
    return {
        "screenshot_selection": screenshot_selection,
    }

def final_payload_node(state: LandingGraphState) -> LandingGraphState:
    logger.info("Graph node started: final_payload")

    request = state["request"]
    app_data = state["app_data"]
    cta = state["cta"]

    final_payload = FinalLandingPagePayload(
        app_name=app_data["title"],
        app_icon=app_data.get("icon"),
        google_play_url=request.googlePlayUrl,
        landing_page=state.get("landing_page"),
        variants=state.get("variants", []),
        cta=cta,
        generation_mode=request.generationMode,
        screenshot_selection=state.get("screenshot_selection"),
    )

    logger.info("Graph node finished: final_payload")
    return {
        "final_payload": final_payload,
    }

def build_landing_graph():
    graph = StateGraph(LandingGraphState)

    graph.add_node("extraction", extraction_node)
    graph.add_node("marketing", marketing_node)
    graph.add_node("screenshot_selection", screenshot_selection_node)
    graph.add_node("copywriter", copywriter_node)
    graph.add_node("cta", cta_node)
    graph.add_node("final_payload", final_payload_node)

    graph.add_edge(START, "extraction")
    graph.add_edge("extraction", "marketing")
    graph.add_edge("marketing", "screenshot_selection")
    graph.add_edge("screenshot_selection", "copywriter")
    graph.add_edge("copywriter", "cta")
    graph.add_edge("cta", "final_payload")
    graph.add_edge("final_payload", END)

    return graph.compile()

def generate_landing_page_graph_workflow(
    request: GenerateLandingPageRequest,
) -> FinalLandingPagePayload:
    if request.ctaMode == "stripe_subscription" and not (
        request.stripeCheckoutUrl or os.getenv("STRIPE_CHECKOUT_URL")
    ):
        raise ValueError(
            "stripeCheckoutUrl is required when ctaMode is stripe_subscription"
        )

    logger.info(
        "Starting landing page pipeline (googlePlayUrl=%s, generationMode=%s)",
        request.googlePlayUrl,
        request.generationMode,
    )

    graph = build_landing_graph()

    result = graph.invoke(
        {
            "request": request,
        }
    )

    logger.info("Landing page pipeline completed")
    return result["final_payload"]