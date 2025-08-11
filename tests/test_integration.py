"""Integration tests that mock external dependencies"""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.domain.entities.summary import Summary
from app.main import create_app


@pytest.fixture
def mock_langchain_llm():
    """Mock LangChain LLM for testing without actual LMStudio"""
    with patch("app.infrastructure.repositories.lmstudio_summary_repository.ChatOpenAI") as mock_llm_class:
        mock_llm_instance = Mock()
        mock_response = Mock()
        mock_response.content = "이것은 모킹된 요약 결과입니다. 테스트를 위한 가짜 응답입니다."
        mock_llm_instance.ainvoke = AsyncMock(return_value=mock_response)
        mock_llm_class.return_value = mock_llm_instance
        yield mock_llm_instance


@pytest.fixture
def test_app():
    """Create test FastAPI app"""
    return create_app()


@pytest.fixture
def client(test_app):
    """Test client"""
    return TestClient(test_app)


class TestIntegration:
    """Integration tests with mocked external services"""

    @pytest.mark.asyncio
    async def test_full_summarization_flow_mocked(self, mock_langchain_llm):
        """Test full summarization flow with mocked LLM"""
        from app.domain.value_objects.summary_config import LMStudioConfig, SummaryConfig
        from app.infrastructure.repositories.lmstudio_summary_repository import LMStudioSummaryRepository

        # Arrange
        lmstudio_config = LMStudioConfig()
        summary_config = SummaryConfig()
        repository = LMStudioSummaryRepository(lmstudio_config)

        # Act
        result = await repository.summarize_text("테스트용 긴 텍스트입니다.", summary_config)

        # Assert
        assert isinstance(result, Summary)
        assert result.original_text == "테스트용 긴 텍스트입니다."
        assert result.summary_text == "이것은 모킹된 요약 결과입니다. 테스트를 위한 가짜 응답입니다."
        assert result.model_name == "qwen/qwen3-4b"
        assert mock_langchain_llm.ainvoke.called

    @pytest.mark.asyncio
    async def test_health_check_mocked(self, mock_langchain_llm):
        """Test health check with mocked LLM"""
        from app.domain.value_objects.summary_config import LMStudioConfig
        from app.infrastructure.repositories.lmstudio_summary_repository import LMStudioSummaryRepository

        # Arrange
        lmstudio_config = LMStudioConfig()
        repository = LMStudioSummaryRepository(lmstudio_config)

        # Act
        result = await repository.health_check()

        # Assert
        assert result is True
        assert mock_langchain_llm.ainvoke.called

    def test_api_endpoint_with_mocked_service(self, client, mock_langchain_llm):
        """Test API endpoint with mocked LangChain service"""
        test_client = client

        # Act
        response = test_client.post(
            "/api/v1/summary/",
            json={
                "text": "테스트용 긴 텍스트입니다. 이 텍스트는 요약되어야 합니다. 충분히 긴 텍스트로 만들어 봅시다.",
                "summary_type": "concise",
                "language": "korean",
            },
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "summary_text" in data
        assert "original_text" in data
        assert data["model_name"] == "qwen/qwen3-4b"
