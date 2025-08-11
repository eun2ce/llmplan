"""Summary API router"""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.requests.summary_request import (
    HealthCheckRequest,
    SummaryRequest,
)
from app.application.dtos.responses.summary_response import (
    ErrorResponse,
    HealthCheckResponse,
    SummaryResponse,
)
from app.application.use_cases.summary_use_cases import (
    HealthCheckUseCase,
    SummarizeTextUseCase,
)
from app.config.container import Container

router = APIRouter(prefix="/summary", tags=["summary"])


@router.post(
    "/",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
    summary="Summarize text",
    description="Summarize the provided text using LMStudio and Qwen model",
)
@inject
async def summarize_text(
    request: SummaryRequest,
    use_case: SummarizeTextUseCase = Depends(Provide[Container.summarize_text_use_case]),
) -> SummaryResponse:
    """
    Summarize text endpoint

    Args:
        request: Summary request containing text and configuration
        use_case: Injected summarize text use case

    Returns:
        Summary response with original text and generated summary

    Raises:
        HTTPException: If summarization fails
    """
    try:
        return await use_case.execute(request)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse(
                error=str(e),
                error_code="VALIDATION_ERROR",
                details="Request validation failed",
            ).model_dump(mode="json"),
        ) from e

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error=str(e),
                error_code="SUMMARIZATION_ERROR",
                details="Failed to generate summary",
            ).model_dump(mode="json"),
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="Internal server error",
                error_code="INTERNAL_ERROR",
                details=str(e),
            ).model_dump(mode="json"),
        ) from e


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Check service health",
    description="Check if the text summarization service is healthy and responsive",
)
@inject
async def health_check(
    use_case: HealthCheckUseCase = Depends(Provide[Container.health_check_use_case]),
) -> HealthCheckResponse:
    """
    Health check endpoint

    Args:
        use_case: Injected health check use case

    Returns:
        Health check response with service status
    """
    try:
        request = HealthCheckRequest()
        response = await use_case.execute(request)

        # Return appropriate HTTP status based on health
        if response.status == "unhealthy":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=response.model_dump(mode="json")
            )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        # Handle unexpected errors
        error_response = HealthCheckResponse(status="unhealthy", details=f"Health check failed: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=error_response.model_dump(mode="json"),
        ) from e
