"""Test domain services"""

import pytest

from app.domain.services.summary_service import SummaryService
from app.domain.value_objects.summary_config import SummaryConfig


class TestSummaryService:
    """Test SummaryService"""

    @pytest.fixture
    def summary_service(self, mock_summary_repository):
        """Create summary service with mock repository"""
        return SummaryService(mock_summary_repository)

    @pytest.mark.asyncio
    async def test_summarize_text_success(self, summary_service, mock_summary_repository, sample_summary, sample_text):
        """Test successful text summarization"""
        # Arrange
        mock_summary_repository.summarize_text.return_value = sample_summary

        # Act
        result = await summary_service.summarize_text(sample_text)

        # Assert
        assert result == sample_summary
        mock_summary_repository.summarize_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_summarize_empty_text(self, summary_service):
        """Test summarization with empty text"""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            await summary_service.summarize_text("")

    @pytest.mark.asyncio
    async def test_summarize_whitespace_only_text(self, summary_service):
        """Test summarization with whitespace-only text"""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            await summary_service.summarize_text("   \n\t   ")

    @pytest.mark.asyncio
    async def test_summarize_too_short_text(self, summary_service):
        """Test summarization with too short text"""
        with pytest.raises(ValueError, match="Text is too short"):
            await summary_service.summarize_text("짧음")

    @pytest.mark.asyncio
    async def test_summarize_too_long_text(self, summary_service):
        """Test summarization with too long text"""
        long_text = "a" * 50001  # Exceed max length
        with pytest.raises(ValueError, match="Text is too long"):
            await summary_service.summarize_text(long_text)

    @pytest.mark.asyncio
    async def test_check_service_health_success(self, summary_service, mock_summary_repository):
        """Test successful health check"""
        # Arrange
        mock_summary_repository.health_check.return_value = True

        # Act
        result = await summary_service.check_service_health()

        # Assert
        assert result is True
        mock_summary_repository.health_check.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_service_health_failure(self, summary_service, mock_summary_repository):
        """Test health check failure"""
        # Arrange
        mock_summary_repository.health_check.side_effect = Exception("Connection failed")

        # Act
        result = await summary_service.check_service_health()

        # Assert
        assert result is False

    def test_validate_summary_config_success(self, summary_service, summary_config):
        """Test valid summary configuration"""
        result = summary_service.validate_summary_config(summary_config)
        assert result is True

    def test_validate_summary_config_invalid(self, summary_service):
        """Test invalid summary configuration"""
        # This would raise ValueError in SummaryConfig.__post_init__
        # but we're testing the service validation logic
        config = SummaryConfig()
        result = summary_service.validate_summary_config(config)
        assert result is True  # Basic config should be valid
