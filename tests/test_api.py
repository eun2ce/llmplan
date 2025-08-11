"""Test API endpoints"""

from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient

from app.application.dtos.responses.summary_response import HealthCheckResponse, SummaryResponse
from app.application.use_cases.summary_use_cases import HealthCheckUseCase, SummarizeTextUseCase
from app.config.container import Container
from app.main import create_app


@pytest.fixture
def mock_container():
    """Mock container for dependency injection"""
    container = Mock(spec=Container)

    # Mock use cases
    mock_summarize_use_case = Mock(spec=SummarizeTextUseCase)
    mock_health_use_case = Mock(spec=HealthCheckUseCase)

    container.summarize_text_use_case.return_value = mock_summarize_use_case
    container.health_check_use_case.return_value = mock_health_use_case

    return container, mock_summarize_use_case, mock_health_use_case


@pytest.fixture
def client(mock_container):
    """Test client with mocked dependencies"""
    container, mock_summarize_use_case, mock_health_use_case = mock_container

    app = create_app()
    app.state.container = container

    # Override dependency injection for testing
    app.dependency_overrides = {
        container.summarize_text_use_case: lambda: mock_summarize_use_case,
        container.health_check_use_case: lambda: mock_health_use_case,
    }

    return TestClient(app), mock_summarize_use_case, mock_health_use_case


def test_health_check_endpoint(client):
    """Test health check endpoint"""
    test_client, _, mock_health_use_case = client

    # Arrange
    mock_health_use_case.execute = AsyncMock(
        return_value=HealthCheckResponse(status="healthy", details="Service is running")
    )

    # Act
    response = test_client.get("/api/v1/summary/health")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_summarize_text_endpoint(client, sample_summary):
    """Test text summarization endpoint"""
    test_client, mock_summarize_use_case, _ = client

    # Arrange
    mock_response = SummaryResponse.from_domain_entity(sample_summary)
    mock_summarize_use_case.execute = AsyncMock(return_value=mock_response)

    # Act
    response = test_client.post(
        "/api/v1/summary/",
        json={
            "text": "테스트용 긴 텍스트입니다. 이 텍스트는 요약되어야 합니다.",
            "summary_type": "concise",
            "language": "korean",
        },
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "summary_text" in data
    assert "original_text" in data
    assert "id" in data


def test_summarize_text_validation_error(client):
    """Test text summarization with validation error"""
    test_client, _, _ = client

    # Act - Send invalid request (empty text)
    response = test_client.post(
        "/api/v1/summary/",
        json={
            "text": "",  # Invalid: empty text
            "summary_type": "concise",
        },
    )

    # Assert
    assert response.status_code == 422  # Validation error


def test_summarize_text_invalid_summary_type(client):
    """Test text summarization with invalid summary type"""
    test_client, _, _ = client

    # Act
    response = test_client.post(
        "/api/v1/summary/",
        json={
            "text": "유효한 텍스트입니다. 충분히 긴 텍스트입니다.",
            "summary_type": "invalid_type",  # Invalid summary type
        },
    )

    # Assert
    assert response.status_code == 422  # Validation error
