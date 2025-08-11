"""Summary use cases"""

from app.application.dtos.requests.summary_request import (
    HealthCheckRequest,
    SummaryRequest,
)
from app.application.dtos.responses.summary_response import (
    HealthCheckResponse,
    SummaryResponse,
)
from app.domain.services.summary_service import SummaryService
from app.domain.value_objects.summary_config import SummaryConfig


class SummarizeTextUseCase:
    """Use case for text summarization"""

    def __init__(self, summary_service: SummaryService):
        """
        Initialize summarize text use case

        Args:
            summary_service: Domain service for text summarization
        """
        self.summary_service = summary_service

    async def execute(self, request: SummaryRequest) -> SummaryResponse:
        """
        Execute text summarization use case

        Args:
            request: Summary request DTO

        Returns:
            Summary response DTO

        Raises:
            ValueError: If request validation fails
            RuntimeError: If summarization fails
        """
        # Create summary configuration from request
        config = SummaryConfig(
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            summary_type=request.summary_type,
            language=request.language,
        )

        # Validate configuration
        if not self.summary_service.validate_summary_config(config):
            raise ValueError("Invalid summary configuration")

        # Perform summarization
        summary = await self.summary_service.summarize_text(
            text=request.text, config=config
        )

        # Convert to response DTO
        return SummaryResponse.from_domain_entity(summary)


class HealthCheckUseCase:
    """Use case for service health check"""

    def __init__(self, summary_service: SummaryService):
        """
        Initialize health check use case

        Args:
            summary_service: Domain service for text summarization
        """
        self.summary_service = summary_service

    async def execute(self, request: HealthCheckRequest) -> HealthCheckResponse:
        """
        Execute health check use case

        Args:
            request: Health check request DTO

        Returns:
            Health check response DTO
        """
        try:
            is_healthy = await self.summary_service.check_service_health()

            if is_healthy:
                return HealthCheckResponse(
                    status="healthy", details="LMStudio service is responding correctly"
                )
            else:
                return HealthCheckResponse(
                    status="unhealthy", details="LMStudio service is not responding"
                )

        except Exception as e:
            return HealthCheckResponse(
                status="unhealthy", details=f"Health check failed: {str(e)}"
            )
