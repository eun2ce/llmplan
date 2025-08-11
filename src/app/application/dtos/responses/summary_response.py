"""Summary response DTOs"""

from datetime import datetime

from pydantic import BaseModel, Field


class SummaryResponse(BaseModel):
    """Response DTO for text summarization"""

    id: str = Field(..., description="Unique identifier for the summary")

    original_text: str = Field(..., description="Original text that was summarized")

    summary_text: str = Field(..., description="Generated summary text")

    created_at: datetime = Field(..., description="Timestamp when summary was created")

    model_name: str = Field(..., description="Name of the model used for summarization")

    summary_length: int = Field(..., description="Length of the summary in characters")

    original_length: int = Field(..., description="Length of the original text in characters")

    compression_ratio: float = Field(..., description="Ratio of summary length to original length")

    @classmethod
    def from_domain_entity(cls, summary) -> "SummaryResponse":
        """Create response DTO from domain entity"""
        original_length = len(summary.original_text)
        compression_ratio = summary.summary_length / original_length if original_length > 0 else 0.0

        return cls(
            id=summary.id,
            original_text=summary.original_text,
            summary_text=summary.summary_text,
            created_at=summary.created_at,
            model_name=summary.model_name,
            summary_length=summary.summary_length,
            original_length=original_length,
            compression_ratio=round(compression_ratio, 3),
        )


class HealthCheckResponse(BaseModel):
    """Response DTO for health check"""

    status: str = Field(..., description="Health status: healthy or unhealthy")

    service_name: str = Field(default="Text Summarization Service", description="Name of the service")

    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of health check")

    details: str | None = Field(default=None, description="Additional details about health status")


class ErrorResponse(BaseModel):
    """Response DTO for error cases"""

    error: str = Field(..., description="Error message")

    error_code: str = Field(..., description="Error code for client handling")

    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp when error occurred")

    details: str | None = Field(default=None, description="Additional error details")
