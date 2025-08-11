"""Test value objects"""

import pytest

from app.domain.value_objects.summary_config import SummaryConfig, LMStudioConfig


class TestSummaryConfig:
    """Test SummaryConfig value object"""

    def test_default_config(self):
        """Test default configuration"""
        config = SummaryConfig()
        
        assert config.max_tokens == 1000
        assert config.temperature == 0.3
        assert config.model_name == "qwen/qwen3-4b"
        assert config.summary_type == "concise"
        assert config.language == "korean"

    def test_custom_config(self):
        """Test custom configuration"""
        config = SummaryConfig(
            max_tokens=500,
            temperature=0.5,
            summary_type="detailed",
            language="english"
        )
        
        assert config.max_tokens == 500
        assert config.temperature == 0.5
        assert config.summary_type == "detailed"
        assert config.language == "english"

    def test_invalid_max_tokens(self):
        """Test invalid max_tokens validation"""
        with pytest.raises(ValueError, match="max_tokens must be positive"):
            SummaryConfig(max_tokens=0)

    def test_invalid_temperature_low(self):
        """Test invalid temperature (too low)"""
        with pytest.raises(ValueError, match="temperature must be between"):
            SummaryConfig(temperature=-0.1)

    def test_invalid_temperature_high(self):
        """Test invalid temperature (too high)"""
        with pytest.raises(ValueError, match="temperature must be between"):
            SummaryConfig(temperature=2.1)

    def test_invalid_summary_type(self):
        """Test invalid summary type"""
        with pytest.raises(ValueError, match="summary_type must be one of"):
            SummaryConfig(summary_type="invalid")


class TestLMStudioConfig:
    """Test LMStudioConfig value object"""

    def test_default_config(self):
        """Test default LMStudio configuration"""
        config = LMStudioConfig()
        
        assert config.base_url == "http://localhost:1234/v1"
        assert config.api_key == "lm-studio"
        assert config.timeout == 30
        assert config.max_retries == 3

    def test_custom_config(self):
        """Test custom LMStudio configuration"""
        config = LMStudioConfig(
            base_url="http://custom:5000/v1",
            api_key="custom-key",
            timeout=60,
            max_retries=5
        )
        
        assert config.base_url == "http://custom:5000/v1"
        assert config.api_key == "custom-key"
        assert config.timeout == 60
        assert config.max_retries == 5
