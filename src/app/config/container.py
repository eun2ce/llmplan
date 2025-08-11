"""Dependency injection container"""

from dependency_injector import containers, providers

from app.application.use_cases.summary_use_cases import (
    HealthCheckUseCase,
    SummarizeTextUseCase,
)
from app.config.settings import Settings
from app.domain.services.summary_service import SummaryService
from app.domain.value_objects.summary_config import LMStudioConfig
from app.infrastructure.repositories.lmstudio_summary_repository import (
    LMStudioSummaryRepository,
)


class Container(containers.DeclarativeContainer):
    """Application dependency injection container"""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.presentation.routers.health",
            "app.presentation.routers.summary",
        ],
    )

    # Configuration
    settings = providers.Singleton(Settings)

    lmstudio_config = providers.Factory(
        LMStudioConfig,
        base_url=settings.provided.LMSTUDIO_BASE_URL,
        api_key=settings.provided.LMSTUDIO_API_KEY,
        timeout=settings.provided.LMSTUDIO_TIMEOUT,
        max_retries=settings.provided.LMSTUDIO_MAX_RETRIES,
    )

    # Repositories
    summary_repository = providers.Factory(
        LMStudioSummaryRepository,
        lmstudio_config=lmstudio_config,
    )

    # Services
    summary_service = providers.Factory(
        SummaryService,
        summary_repository=summary_repository,
    )

    # Use Cases
    summarize_text_use_case = providers.Factory(
        SummarizeTextUseCase,
        summary_service=summary_service,
    )

    health_check_use_case = providers.Factory(
        HealthCheckUseCase,
        summary_service=summary_service,
    )
