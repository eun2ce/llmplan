"""Summary request DTOs"""

from pydantic import BaseModel, Field, field_validator


class SummaryRequest(BaseModel):
    """Request DTO for text summarization"""

    text: str = Field(..., min_length=10, max_length=50000, description="Text to be summarized")

    max_tokens: int | None = Field(default=1000, ge=50, le=4000, description="Maximum number of tokens for summary")

    temperature: float | None = Field(
        default=0.3,
        ge=0.0,
        le=2.0,
        description="Temperature for text generation (0.0 to 2.0)",
    )

    summary_type: str | None = Field(
        default="concise",
        description="Type of summary: concise, detailed, bullet_points",
    )

    language: str | None = Field(default="korean", description="Language for summary output")

    @field_validator("summary_type")
    @classmethod
    def validate_summary_type(cls, v):
        """Validate summary type"""
        allowed_types = ["concise", "detailed", "bullet_points"]
        if v not in allowed_types:
            raise ValueError(f"summary_type must be one of: {', '.join(allowed_types)}")
        return v

    @field_validator("language")
    @classmethod
    def validate_language(cls, v):
        """Validate language"""
        allowed_languages = ["korean", "english", "japanese"]
        if v not in allowed_languages:
            raise ValueError(f"language must be one of: {', '.join(allowed_languages)}")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        """Validate text content"""
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class HealthCheckRequest(BaseModel):
    """Request DTO for health check"""

    pass
