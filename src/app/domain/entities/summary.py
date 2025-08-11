"""Summary domain entity"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Summary:
    """Text summary entity"""

    id: str | None = None
    original_text: str = ""
    summary_text: str = ""
    created_at: datetime | None = None
    model_name: str = "qwen/qwen3-4b"
    summary_length: int | None = None

    def __post_init__(self):
        """Post-initialization processing"""
        if self.created_at is None:
            self.created_at = datetime.now()

        if self.summary_length is None and self.summary_text:
            self.summary_length = len(self.summary_text)
