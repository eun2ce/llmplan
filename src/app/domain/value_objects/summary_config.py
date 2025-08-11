"""Summary configuration value objects"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SummaryConfig:
    """Configuration for text summarization"""

    max_tokens: int = 1000
    temperature: float = 0.3
    model_name: str = "qwen/qwen3-4b"
    summary_type: str = "concise"  # concise, detailed, bullet_points
    language: str = "korean"

    def __post_init__(self):
        """Validate configuration values"""
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")

        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")

        if self.summary_type not in ["concise", "detailed", "bullet_points"]:
            raise ValueError(
                "summary_type must be one of: concise, detailed, bullet_points"
            )


@dataclass(frozen=True)
class LMStudioConfig:
    """LMStudio server configuration"""

    base_url: str = "http://localhost:1234/v1"
    api_key: str = "lm-studio"
    timeout: int = 30
    max_retries: int = 3
