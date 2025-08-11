# LLMPlan 서비스 컨텍스트

## 📋 서비스 개요

### 목적

- **텍스트 요약 서비스**: LMStudio와 Qwen 모델을 활용한 한국어 텍스트 요약
- **REST API**: FastAPI 기반의 고성능 비동기 API 서버
- **마이크로서비스**: Clean Architecture 기반의 확장 가능한 구조

### 핵심 기능

- 긴 텍스트의 자동 요약 (간결, 상세, 요점 정리)
- 한국어 최적화 요약
- 헬스체크 및 모니터링
- 설정 가능한 요약 파라미터

## 🏗️ 아키텍처

### Clean Architecture 구조

```
src/app/
├── domain/              # 비즈니스 로직 (엔티티, 서비스)
├── application/         # 유스케이스, DTO
├── infrastructure/      # 외부 시스템 연동 (LMStudio)
├── presentation/        # API 엔드포인트
└── config/             # 설정 및 DI 컨테이너
```

### 의존성 방향

```
Presentation → Application → Domain ← Infrastructure
```

### 핵심 컴포넌트

- **SummaryService**: 요약 비즈니스 로직
- **LMStudioRepository**: LMStudio API 연동
- **SummarizeTextUseCase**: 요약 실행 유스케이스
- **HealthCheckUseCase**: 헬스체크 유스케이스

## 🔧 기술 스택

### 백엔드

- **Python 3.12**: 메인 언어
- **FastAPI**: 웹 프레임워크
- **Pydantic V2**: 데이터 검증 및 직렬화
- **dependency-injector**: 의존성 주입
- **LangChain**: LLM 추상화 레이어

### AI/ML

- **LMStudio**: 로컬 LLM 서버
- **Qwen 3-4B**: 중국어/한국어 특화 모델
- **OpenAI API 호환**: 표준 Chat Completion API

### 배포

- **Docker**: 컨테이너화
- **Kubernetes**: 오케스트레이션
- **Helm**: 패키지 관리
- **uv**: Python 패키지 관리

## 🌐 API 스펙

### 엔드포인트

#### 1. 텍스트 요약

```http
POST /api/v1/summary/
Content-Type: application/json

{
  "text": "요약할 긴 텍스트...",
  "summary_type": "concise|detailed|bullet_points",
  "language": "korean|english",
  "max_tokens": 1000,
  "temperature": 0.3
}
```

**응답:**

```json
{
  "id": "uuid",
  "original_text": "원본 텍스트",
  "summary_text": "요약된 텍스트",
  "created_at": "2025-01-01T00:00:00Z",
  "model_name": "qwen/qwen3-4b",
  "summary_length": 150,
  "original_length": 1000,
  "compression_ratio": 0.15
}
```

#### 2. 헬스체크

```http
GET /api/v1/summary/health
```

**응답:**

```json
{
  "status": "healthy|unhealthy",
  "service_name": "Text Summarization Service",
  "timestamp": "2025-01-01T00:00:00Z",
  "details": "Service status details"
}
```

### 에러 응답

```json
{
  "error": "Error message",
  "error_code": "VALIDATION_ERROR|SUMMARIZATION_ERROR|INTERNAL_ERROR",
  "timestamp": "2025-01-01T00:00:00Z",
  "details": "Additional error details"
}
```

## 🔧 설정

### 환경 변수

```bash
# LMStudio 연결
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_TIMEOUT=30
LMSTUDIO_MAX_RETRIES=3

# 모델 설정
DEFAULT_MODEL_NAME=qwen/qwen3-4b
DEFAULT_MAX_TOKENS=1000
DEFAULT_TEMPERATURE=0.3
DEFAULT_SUMMARY_TYPE=concise
DEFAULT_LANGUAGE=korean

# 디버그
DEBUG=false
```

### 요약 타입

- **concise**: 간결한 요약 (1-2 문장)
- **detailed**: 상세한 요약 (여러 단락)
- **bullet_points**: 요점 정리 (불릿 포인트)

## 🚀 배포 정보

### Docker 이미지

- **Repository**: `eunheejo/llmplan`
- **Tags**: `latest`, `v0.1.0`, `main`
- **Platforms**: `linux/amd64`, `linux/arm64`

### Helm Chart

- **OCI Registry**: `oci://registry-1.docker.io/eunheejo/llmplan`
- **Version**: `0.1.0`
- **Namespace**: `llmplan` (권장)

### 배포 명령어

```bash
# Docker
docker run -d -p 8000:8000 eunheejo/llmplan:latest

# Kubernetes
helm install llmplan oci://registry-1.docker.io/eunheejo/llmplan \
  --namespace llmplan --create-namespace

# 로컬 개발
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔍 모니터링

### 헬스체크

- **URL**: `GET /api/v1/summary/health`
- **정상**: HTTP 200, `{"status": "healthy"}`
- **비정상**: HTTP 503, `{"status": "unhealthy"}`

### 로그 레벨

- **INFO**: 정상 요청/응답
- **WARNING**: 검증 실패, 재시도
- **ERROR**: LMStudio 연결 실패, 요약 실패

### 메트릭 (향후 추가 예정)

- 요약 요청 수
- 평균 응답 시간
- LMStudio 연결 상태
- 에러율

## 🧪 테스트

### 테스트 구조

- **Unit Tests**: 도메인 로직, 값 객체 검증
- **Integration Tests**: 모킹된 LMStudio 연동
- **API Tests**: FastAPI 엔드포인트
- **CI-Safe Tests**: 외부 의존성 없는 테스트

### 실행 명령어

```bash
# 전체 테스트
uv run pytest

# CI 안전 테스트만
uv run pytest tests/test_basic.py tests/test_ci_safe.py \
              tests/test_domain_entities.py tests/test_value_objects.py \
              tests/test_domain_services.py tests/test_use_cases.py

# 커버리지
uv run pytest --cov=src
```

## 🔄 CI/CD 파이프라인

### 트리거

- **Push to main**: Docker + Helm 배포
- **Tag push (v\*)**: 버전 릴리즈
- **Pull Request**: 테스트만 실행

### 파이프라인 단계

1. **Code Quality**: Ruff 린팅, 포맷팅 검사
2. **Testing**: 36개 CI-safe 테스트 실행
3. **Docker Build**: 멀티플랫폼 이미지 빌드
4. **Docker Push**: Docker Hub에 푸시
5. **Helm Package**: 차트 패키징
6. **Helm Push**: OCI Registry에 푸시

### 배포 아티팩트

- **Docker**: `eunheejo/llmplan:latest`
- **Helm**: `oci://registry-1.docker.io/eunheejo/llmplan`

## 🔗 외부 의존성

### LMStudio

- **역할**: 로컬 LLM 서버
- **모델**: Qwen 3-4B
- **API**: OpenAI 호환 Chat Completion
- **연결**: HTTP REST API

### 의존성 처리

- **연결 실패**: Graceful degradation, 503 에러 반환
- **재시도**: 최대 3회 재시도
- **타임아웃**: 30초 기본값

## 📈 성능 특성

### 리소스 요구사항

- **CPU**: 500m (요청), 1000m (제한)
- **Memory**: 512Mi (요청), 1Gi (제한)
- **Storage**: 임시 데이터만 사용 (상태 없음)

### 확장성

- **Horizontal**: HPA로 CPU 기반 자동 스케일링
- **Vertical**: 리소스 요구량 조정 가능
- **Stateless**: 세션 상태 없음, 무제한 확장 가능

## 🛡️ 보안

### 컨테이너 보안

- **Non-root user**: UID 1000으로 실행
- **Read-only filesystem**: 가능한 경우
- **Capability drop**: 모든 불필요한 권한 제거

### API 보안

- **Input validation**: Pydantic으로 엄격한 검증
- **Error handling**: 민감한 정보 노출 방지
- **Rate limiting**: 향후 추가 예정

## 🔮 향후 계획

### 단기 (v0.2.0)

- [ ] 요약 품질 메트릭 추가
- [ ] 배치 요약 기능
- [ ] 요약 히스토리 저장

### 중기 (v0.3.0)

- [ ] 다국어 지원 확장
- [ ] 요약 스타일 커스터마이징
- [ ] 웹 UI 추가

### 장기 (v1.0.0)

- [ ] 다중 모델 지원
- [ ] 요약 품질 평가
- [ ] 실시간 스트리밍 요약
