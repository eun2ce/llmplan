"""Basic tests that don't require external dependencies"""

from datetime import datetime

import pytest

from app.domain.entities.summary import Summary
from app.domain.value_objects.summary_config import LMStudioConfig, SummaryConfig


def test_app_imports():
    """Test that all main modules can be imported"""
    # This ensures basic syntax and import errors are caught
    from app.config.settings import Settings
    from app.domain.entities.summary import Summary
    from app.domain.value_objects.summary_config import SummaryConfig
    from app.main import create_app

    # Basic creation tests
    app = create_app()
    settings = Settings()
    summary = Summary()
    config = SummaryConfig()

    assert app is not None
    assert settings is not None
    assert summary is not None
    assert config is not None


def test_summary_entity_basic():
    """Test basic Summary entity functionality"""
    summary = Summary(original_text="테스트 텍스트", summary_text="요약 텍스트")

    assert summary.original_text == "테스트 텍스트"
    assert summary.summary_text == "요약 텍스트"
    assert isinstance(summary.created_at, datetime)
    assert summary.summary_length == len("요약 텍스트")


def test_summary_config_validation():
    """Test SummaryConfig validation without external dependencies"""
    # Valid config
    config = SummaryConfig(max_tokens=500, temperature=0.5, summary_type="concise", language="korean")
    assert config.max_tokens == 500

    # Invalid max_tokens
    with pytest.raises(ValueError):
        SummaryConfig(max_tokens=0)

    # Invalid temperature
    with pytest.raises(ValueError):
        SummaryConfig(temperature=3.0)

    # Invalid summary_type
    with pytest.raises(ValueError):
        SummaryConfig(summary_type="invalid")


def test_lmstudio_config():
    """Test LMStudioConfig creation"""
    config = LMStudioConfig(base_url="http://test:1234/v1", api_key="test-key")

    assert config.base_url == "http://test:1234/v1"
    assert config.api_key == "test-key"
    assert config.timeout == 30  # default
    assert config.max_retries == 3  # default


def test_settings_creation():
    """Test Settings configuration"""
    from app.config.settings import Settings

    settings = Settings()
    assert settings.APP_NAME == "llmplan"
    assert settings.API_V1_PREFIX == "/api/v1"
    assert settings.DEFAULT_MODEL_NAME == "qwen/qwen3-4b"
