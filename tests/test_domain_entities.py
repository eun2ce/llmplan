"""Test domain entities"""

from datetime import datetime

from app.domain.entities.summary import Summary


class TestSummary:
    """Test Summary entity"""

    def test_summary_creation(self):
        """Test summary entity creation"""
        summary = Summary(
            id="test-id",
            original_text="원본 텍스트",
            summary_text="요약 텍스트",
            model_name="qwen/qwen3-4b"
        )

        assert summary.id == "test-id"
        assert summary.original_text == "원본 텍스트"
        assert summary.summary_text == "요약 텍스트"
        assert summary.model_name == "qwen/qwen3-4b"
        assert isinstance(summary.created_at, datetime)
        assert summary.summary_length == len("요약 텍스트")

    def test_summary_auto_fields(self):
        """Test automatic field population"""
        summary = Summary(
            original_text="테스트",
            summary_text="요약"
        )

        # created_at should be auto-populated
        assert summary.created_at is not None
        assert isinstance(summary.created_at, datetime)

        # summary_length should be auto-calculated
        assert summary.summary_length == len("요약")

    def test_summary_with_empty_summary_text(self):
        """Test summary with empty summary text"""
        summary = Summary(
            original_text="테스트",
            summary_text=""
        )

        # summary_length should remain None for empty text
        assert summary.summary_length is None
