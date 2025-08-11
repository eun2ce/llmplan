"""LMStudio implementation of summary repository"""

import uuid
from datetime import datetime

from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.domain.entities.summary import Summary
from app.domain.repositories.summary_repository import SummaryRepository
from app.domain.value_objects.summary_config import LMStudioConfig, SummaryConfig


class LMStudioSummaryRepository(SummaryRepository):
    """LMStudio-based implementation of summary repository"""

    def __init__(self, lmstudio_config: LMStudioConfig):
        """
        Initialize LMStudio summary repository

        Args:
            lmstudio_config: LMStudio configuration
        """
        self.config = lmstudio_config
        self._llm: ChatOpenAI | None = None

    def _get_llm(self, summary_config: SummaryConfig) -> ChatOpenAI:
        """Get or create LLM instance"""
        if self._llm is None:
            self._llm = ChatOpenAI(
                base_url=self.config.base_url,
                api_key=self.config.api_key,
                model=summary_config.model_name,
                temperature=summary_config.temperature,
                max_tokens=summary_config.max_tokens,
                timeout=self.config.timeout,
                max_retries=self.config.max_retries,
            )
        return self._llm

    def _get_system_prompt(self, config: SummaryConfig) -> str:
        """Generate system prompt based on configuration"""
        language_instruction = {
            "korean": "한국어로 답변해주세요.",
            "english": "Please respond in English.",
            "japanese": "日本語で答えてください。",
        }.get(config.language, "한국어로 답변해주세요.")

        summary_style = {
            "concise": "간결하고 핵심적인 내용으로 요약해주세요.",
            "detailed": "상세하고 포괄적인 내용으로 요약해주세요.",
            "bullet_points": "주요 내용을 불릿 포인트 형태로 정리해주세요.",
        }.get(config.summary_type, "간결하고 핵심적인 내용으로 요약해주세요.")

        return f"""당신은 전문적인 텍스트 요약 어시스턴트입니다.
주어진 텍스트를 분석하여 핵심 내용을 추출하고 요약해주세요.

요약 지침:
- {summary_style}
- {language_instruction}
- 원본 텍스트의 주요 정보와 맥락을 유지해주세요.
- 불필요한 세부사항은 제거하되, 중요한 내용은 누락하지 마세요.
- 명확하고 이해하기 쉬운 문장으로 작성해주세요."""

    async def summarize_text(self, text: str, config: SummaryConfig) -> Summary:
        """
        Summarize text using LMStudio

        Args:
            text: Text to summarize
            config: Summary configuration

        Returns:
            Summary entity
        """
        try:
            llm = self._get_llm(config)

            system_prompt = self._get_system_prompt(config)
            user_prompt = f"다음 텍스트를 요약해주세요:\n\n{text}"

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]

            response = await llm.ainvoke(messages)
            summary_text = response.content.strip()

            return Summary(
                id=str(uuid.uuid4()),
                original_text=text,
                summary_text=summary_text,
                created_at=datetime.now(),
                model_name=config.model_name,
                summary_length=len(summary_text),
            )

        except Exception as e:
            raise RuntimeError("Failed to summarize text") from e

    async def health_check(self) -> bool:
        """
        Check if LMStudio service is healthy

        Returns:
            True if healthy, False otherwise
        """
        try:
            # Create a minimal configuration for health check
            config = SummaryConfig(max_tokens=50, temperature=0.1)
            llm = self._get_llm(config)

            # Send a simple test message
            test_message = [HumanMessage(content="Hello")]
            response = await llm.ainvoke(test_message)

            return bool(response.content.strip())
        except Exception:
            return False
