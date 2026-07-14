import logging

from fastapi import APIRouter, HTTPException

from models.schemas import GenerateLandingPageRequest, FinalLandingPagePayload
from workflows.landing_graph import generate_landing_page_graph_workflow

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/generate-landing-page", response_model=FinalLandingPagePayload)
def generate_landing_page(request: GenerateLandingPageRequest):
    logger.info(
        "Received /generate-landing-page request (googlePlayUrl=%s, ctaMode=%s, generationMode=%s)",
        request.googlePlayUrl,
        request.ctaMode,
        request.generationMode,
    )
    try:
        return generate_landing_page_graph_workflow(request)
    except ValueError as error:
        logger.warning("Request rejected: %s", error)
        raise HTTPException(status_code=400, detail=str(error))
    except Exception:
        logger.exception("Unhandled error while generating landing page")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate landing page",
        )