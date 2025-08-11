"""Test configuration and fixtures"""

from unittest.mock import AsyncMock, Mock

import pytest

from app.domain.entities.summary import Summary
from app.domain.repositories.summary_repository import SummaryRepository
from app.domain.value_objects.summary_config import LMStudioConfig, SummaryConfig


@pytest.fixture
def sample_text():
    """Sample text for testing"""
    return "이것은 테스트용 텍스트입니다. 요약 기능을 테스트하기 위한 충분한 길이의 텍스트입니다."


@pytest.fixture
def summary_config():
    """Sample summary configuration"""
    return SummaryConfig(
        max_tokens=500, temperature=0.3, model_name="qwen/qwen3-4b", summary_type="concise", language="korean"
    )


@pytest.fixture
def lmstudio_config():
    """Sample LMStudio configuration"""
    return LMStudioConfig(base_url="http://localhost:1234/v1", api_key="test-key", timeout=30, max_retries=3)


@pytest.fixture
def sample_summary():
    """Sample summary entity"""
    return Summary(
        id="test-id",
        original_text="원본 텍스트입니다.",
        summary_text="요약된 텍스트입니다.",
        model_name="qwen/qwen3-4b",
        summary_length=10,
    )


@pytest.fixture
def mock_summary_repository():
    """Mock summary repository"""
    repository = Mock(spec=SummaryRepository)
    repository.summarize_text = AsyncMock()
    repository.health_check = AsyncMock()
    return repository
