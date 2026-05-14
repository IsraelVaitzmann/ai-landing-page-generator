from fastapi import APIRouter, HTTPException

from models.schemas import GenerateLandingPageRequest, FinalLandingPagePayload
from workflows.landing_graph import generate_landing_page_graph_workflow

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/generate-landing-page", response_model=FinalLandingPagePayload)
def generate_landing_page(request: GenerateLandingPageRequest):
    try:
        return generate_landing_page_graph_workflow(request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate landing page",
        )