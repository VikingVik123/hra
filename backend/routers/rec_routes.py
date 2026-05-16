"""Routes for recommendation endpoints."""

import logging
from fastapi import APIRouter, HTTPException, status

from schemas.rec_schema import RecommendationRequest, RecommendationResponse
from services.rec_service import RecommendationService

logger = logging.getLogger(__name__)

router = APIRouter()
service = RecommendationService()


@router.post(
    "/recommendations",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get interview questions",
    description="Generate AI-powered interview questions for a given job title using specified model",
)
async def get_recommendations(request: RecommendationRequest) -> RecommendationResponse:
    """Get interview recommendations for a job title.

    Args:
        request: Request containing the job title and model choice

    Returns:
        RecommendationResponse: List of interview questions

    Raises:
        HTTPException: 400 if input is invalid, 500 if AI generation fails
    """
    logger.info(f"Recommendation request for job title: {request.job_title} using model: {request.model}")

    try:
        questions_list = service.fetch_recs(request.job_title, model=request.model)
        logger.info(f"Successfully returned {len(questions_list)} recommendations")
        return RecommendationResponse(questions=questions_list)

    except ValueError as e:
        logger.warning(f"Invalid request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )