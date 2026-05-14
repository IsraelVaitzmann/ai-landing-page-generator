from typing import Optional, TypedDict

from langgraph.graph import END, START, StateGraph
from agents.screenshot_agent import select_screenshots
from agents.marketing_agent import analyze_marketing
from agents.copywriter_agent import generate_landing_page_content
from agents.cta_agent import generate_cta_config
from models.schemas import (
    CTAConfig,
    CTAConfigInput,
    FinalLandingPagePayload,
    GenerateLandingPageRequest,
    LandingPageContent,
    MarketingInsights,
    ScreenshotSelection,
)
from services.playstore_service import extract_app_data


class LandingGraphState(TypedDict, total=False):
    request: GenerateLandingPageRequest
    app_data: dict
    marketing_insights: MarketingInsights
    landing_page: LandingPageContent
    cta: CTAConfig
    final_payload: FinalLandingPagePayload
    screenshot_selection: ScreenshotSelection

def extraction_node(state: LandingGraphState) -> LandingGraphState:
    print("Graph node: extraction")

    request = state["request"]
    app_data = extract_app_data(request.googlePlayUrl)

    return {
        "app_data": app_data,
    }

def marketing_node(state: LandingGraphState) -> LandingGraphState:
    print("Graph node: marketing")

    app_data = state["app_data"]
    marketing_insights = analyze_marketing(app_data)

    return {
        "marketing_insights": marketing_insights,
    }

def copywriter_node(state: LandingGraphState) -> LandingGraphState:
    print("Graph node: copywriter")

    request = state["request"]
    app_data = state["app_data"]
    marketing_insights = state["marketing_insights"]

    screenshot_selection = state["screenshot_selection"]

    landing_page = generate_landing_page_content(
        app_data=app_data,
        marketing_insights=marketing_insights.model_dump(),
        cta_mode=request.ctaMode,
        selected_screenshots=screenshot_selection.gallery_screenshots,
    )
    return {
        "landing_page": landing_page,
    }

def cta_node(state: LandingGraphState) -> LandingGraphState:
    print("Graph node: cta")

    request = state["request"]

    cta = generate_cta_config(
        CTAConfigInput(
            cta_mode=request.ctaMode,
            google_play_url=request.googlePlayUrl,
            stripe_checkout_url=request.stripeCheckoutUrl,
            custom_cta_button_text=request.customCtaButtonText,
            plan_id=request.planId,
        )
    )

    return {
        "cta": cta,
    }

def screenshot_selection_node(state: LandingGraphState) -> LandingGraphState:
    print("Graph node: screenshot selection")

    app_data = state["app_data"]
    marketing_insights = state["marketing_insights"]

    screenshot_selection = select_screenshots(
        screenshots=app_data.get("screenshots", []),
        marketing_insights=marketing_insights,
    )

    return {
        "screenshot_selection": screenshot_selection,
    }

def final_payload_node(state: LandingGraphState) -> LandingGraphState:
    print("Graph node: final payload")

    request = state["request"]
    app_data = state["app_data"]
    landing_page = state["landing_page"]
    cta = state["cta"]

    final_payload = FinalLandingPagePayload(
        app_name=app_data["title"],
        app_icon=app_data.get("icon"),
        google_play_url=request.googlePlayUrl,
        landing_page=landing_page,
        cta=cta,
        screenshot_selection=state.get("screenshot_selection"),
    )

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
    if request.ctaMode == "stripe_subscription" and not request.stripeCheckoutUrl:
        raise ValueError(
        "stripeCheckoutUrl is required when ctaMode is stripe_subscription"
    )

    graph = build_landing_graph()

    result = graph.invoke(
        {
            "request": request,
        }
    )

    return result["final_payload"]