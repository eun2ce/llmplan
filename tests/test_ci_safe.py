"""CI-safe tests that don't require external services"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.application.dtos.requests.summary_request import SummaryRequest
from app.domain.entities.summary import Summary
from app.domain.services.summary_service import SummaryService
from app.domain.value_objects.summary_config import LMStudioConfig, SummaryConfig


class TestCISafe:
    """Tests that are safe to run in CI environment without external dependencies"""

    def test_summary_config_validation(self):
        """Test SummaryConfig validation logic"""
        # Valid config
        config = SummaryConfig()
        assert config.max_tokens == 1000
        assert config.temperature == 0.3

        # Invalid configs
        with pytest.raises(ValueError):
            SummaryConfig(max_tokens=-1)

        with pytest.raises(ValueError):
            SummaryConfig(temperature=3.0)

        with pytest.raises(ValueError):
            SummaryConfig(summary_type="invalid")

    def test_summary_entity_creation(self):
        """Test Summary entity creation and auto-fields"""
        summary = Summary(original_text="테스트 텍스트", summary_text="요약된 텍스트")

        assert summary.original_text == "테스트 텍스트"
        assert summary.summary_text == "요약된 텍스트"
        assert summary.summary_length == len("요약된 텍스트")
        assert summary.created_at is not None

    @pytest.mark.asyncio
    async def test_summary_service_validation(self):
        """Test SummaryService validation without external calls"""
        # Mock repository
        mock_repo = Mock()
        mock_repo.summarize_text = AsyncMock()
        mock_repo.health_check = AsyncMock()

        service = SummaryService(mock_repo)

        # Test validation
        with pytest.raises(ValueError, match="Text cannot be empty"):
            await service.summarize_text("")

        with pytest.raises(ValueError, match="Text is too short"):
            await service.summarize_text("짧음")

    def test_pydantic_request_validation(self):
        """Test Pydantic request validation"""
        # Valid request
        request = SummaryRequest(
            text="테스트용 충분히 긴 텍스트입니다. 이 텍스트는 요약 기능을 테스트하기 위한 것입니다.",
            summary_type="concise",
            language="korean",
        )
        assert request.text.startswith("테스트용")
        assert request.summary_type == "concise"

        # Invalid summary_type should raise validation error
        with pytest.raises(ValueError):
            SummaryRequest(text="유효한 텍스트입니다.", summary_type="invalid_type")

    def test_app_creation_basic(self):
        """Test basic app creation without starting server"""
        from app.main import create_app

        app = create_app()
        assert app is not None
        assert hasattr(app.state, "container")
        assert hasattr(app.state, "settings")

    @pytest.mark.asyncio
    async def test_mocked_repository_flow(self):
        """Test complete flow with fully mocked repository"""
        # Mock the LangChain ChatOpenAI completely
        with patch("app.infrastructure.repositories.lmstudio_summary_repository.ChatOpenAI") as mock_llm:
            mock_instance = Mock()
            mock_response = Mock()
            mock_response.content = "모킹된 요약 결과입니다."
            mock_instance.ainvoke = AsyncMock(return_value=mock_response)
            mock_llm.return_value = mock_instance

            # Test the repository
            from app.infrastructure.repositories.lmstudio_summary_repository import LMStudioSummaryRepository

            config = LMStudioConfig()
            repo = LMStudioSummaryRepository(config)

            summary_config = SummaryConfig()
            result = await repo.summarize_text("테스트 텍스트", summary_config)

            assert isinstance(result, Summary)
            assert result.summary_text == "모킹된 요약 결과입니다."
            assert mock_instance.ainvoke.called
