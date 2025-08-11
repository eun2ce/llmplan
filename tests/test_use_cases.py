"""Test use cases"""

import pytest
from unittest.mock import AsyncMock

from app.application.use_cases.summary_use_cases import SummarizeTextUseCase, HealthCheckUseCase
from app.application.dtos.requests.summary_request import SummaryRequest, HealthCheckRequest
from app.application.dtos.responses.summary_response import SummaryResponse, HealthCheckResponse


class TestSummarizeTextUseCase:
    """Test SummarizeTextUseCase"""

    @pytest.fixture
    def use_case(self, mock_summary_repository):
        """Create use case with mock service"""
        from app.domain.services.summary_service import SummaryService
        service = SummaryService(mock_summary_repository)
        return SummarizeTextUseCase(service)

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, sample_summary):
        """Test successful use case execution"""
        # Arrange
        request = SummaryRequest(
            text="테스트용 긴 텍스트입니다. 요약 기능을 테스트하기 위한 충분한 길이의 텍스트입니다.",
            summary_type="concise",
            language="korean"
        )
        
        use_case.summary_service.summarize_text = AsyncMock(return_value=sample_summary)
        
        # Act
        result = await use_case.execute(request)
        
        # Assert
        assert isinstance(result, SummaryResponse)
        assert result.summary_text == sample_summary.summary_text
        use_case.summary_service.summarize_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_with_service_error(self, use_case):
        """Test execution when service raises error"""
        # Arrange
        request = SummaryRequest(
            text="테스트용 긴 텍스트입니다. 요약 기능을 테스트하기 위한 충분한 길이의 텍스트입니다.",
            summary_type="concise",
            language="korean"
        )
        
        use_case.summary_service.summarize_text = AsyncMock(
            side_effect=RuntimeError("Summarization failed")
        )
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Summarization failed"):
            await use_case.execute(request)


class TestHealthCheckUseCase:
    """Test HealthCheckUseCase"""

    @pytest.fixture
    def use_case(self, mock_summary_repository):
        """Create use case with mock service"""
        from app.domain.services.summary_service import SummaryService
        service = SummaryService(mock_summary_repository)
        return HealthCheckUseCase(service)

    @pytest.mark.asyncio
    async def test_execute_healthy(self, use_case):
        """Test health check when service is healthy"""
        # Arrange
        use_case.summary_service.check_service_health = AsyncMock(return_value=True)
        request = HealthCheckRequest()
        
        # Act
        result = await use_case.execute(request)
        
        # Assert
        assert isinstance(result, HealthCheckResponse)
        assert result.status == "healthy"
        assert "responding correctly" in result.details

    @pytest.mark.asyncio
    async def test_execute_unhealthy(self, use_case):
        """Test health check when service is unhealthy"""
        # Arrange
        use_case.summary_service.check_service_health = AsyncMock(return_value=False)
        request = HealthCheckRequest()
        
        # Act
        result = await use_case.execute(request)
        
        # Assert
        assert isinstance(result, HealthCheckResponse)
        assert result.status == "unhealthy"
        assert "not responding" in result.details

    @pytest.mark.asyncio
    async def test_execute_exception(self, use_case):
        """Test health check when exception occurs"""
        # Arrange
        use_case.summary_service.check_service_health = AsyncMock(
            side_effect=Exception("Connection error")
        )
        request = HealthCheckRequest()
        
        # Act
        result = await use_case.execute(request)
        
        # Assert
        assert isinstance(result, HealthCheckResponse)
        assert result.status == "unhealthy"
        assert "Health check failed" in result.details
