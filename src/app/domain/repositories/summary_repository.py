"""Summary repository interface"""

from abc import ABC, abstractmethod

from app.domain.entities.summary import Summary
from app.domain.value_objects.summary_config import SummaryConfig


class SummaryRepository(ABC):
    """Abstract repository for text summarization"""

    @abstractmethod
    async def summarize_text(self, text: str, config: SummaryConfig) -> Summary:
        """
        Summarize the given text

        Args:
            text: Text to summarize
            config: Summary configuration

        Returns:
            Summary entity with original text and summary
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the summarization service is healthy

        Returns:
            True if service is healthy, False otherwise
        """
        pass
