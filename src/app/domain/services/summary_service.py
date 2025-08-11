"""Summary domain service"""

from app.domain.entities.summary import Summary
from app.domain.repositories.summary_repository import SummaryRepository
from app.domain.value_objects.summary_config import SummaryConfig


class SummaryService:
    """Domain service for text summarization business logic"""

    def __init__(self, summary_repository: SummaryRepository):
        """
        Initialize summary service

        Args:
            summary_repository: Repository for text summarization
        """
        self.summary_repository = summary_repository

    async def summarize_text(self, text: str, config: SummaryConfig | None = None) -> Summary:
        """
        Summarize the given text with business logic validation

        Args:
            text: Text to summarize
            config: Optional summary configuration

        Returns:
            Summary entity

        Raises:
            ValueError: If text is empty or too short
            RuntimeError: If summarization fails
        """
        # Validate input text
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Check minimum text length
        if len(text.strip()) < 10:
            raise ValueError("Text is too short to summarize (minimum 10 characters)")

        # Check maximum text length (to prevent excessive API usage)
        max_length = 50000  # Approximately 50KB
        if len(text) > max_length:
            raise ValueError(f"Text is too long (maximum {max_length} characters)")

        # Use default config if none provided
        if config is None:
            config = SummaryConfig()

        # Perform summarization
        summary = await self.summary_repository.summarize_text(text, config)

        # Validate summary result
        if not summary.summary_text or not summary.summary_text.strip():
            raise RuntimeError("Failed to generate summary: empty result")

        return summary

    async def check_service_health(self) -> bool:
        """
        Check if the summarization service is available

        Returns:
            True if service is healthy, False otherwise
        """
        try:
            return await self.summary_repository.health_check()
        except Exception:
            return False

    def validate_summary_config(self, config: SummaryConfig) -> bool:
        """
        Validate summary configuration

        Args:
            config: Configuration to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            # SummaryConfig validation is handled in __post_init__
            # This method can be extended for additional business rules
            return True
        except ValueError:
            return False
