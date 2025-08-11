# LLMPlan 기술 명세서

## 🏗️ 시스템 아키텍처

### 레이어 구조

```
┌─────────────────────────────────────┐
│         Presentation Layer          │  ← FastAPI Routes
├─────────────────────────────────────┤
│         Application Layer           │  ← Use Cases, DTOs
├─────────────────────────────────────┤
│           Domain Layer              │  ← Entities, Services
├─────────────────────────────────────┤
│        Infrastructure Layer         │  ← LMStudio Repository
└─────────────────────────────────────┘
```

### 데이터 플로우

```
HTTP Request → Router → Use Case → Domain Service → Repository → LMStudio
                ↓
HTTP Response ← DTO ← Domain Entity ← Summary ← LLM Response
```

## 🔧 핵심 컴포넌트

### 1. Domain Entities

```python
# Summary Entity
class Summary:
    id: str
    original_text: str
    summary_text: str
    created_at: datetime
    model_name: str
    summary_length: int
```

### 2. Value Objects

```python
# Summary Configuration
class SummaryConfig:
    max_tokens: int = 1000
    temperature: float = 0.3
    model_name: str = "qwen/qwen3-4b"
    summary_type: Literal["concise", "detailed", "bullet_points"]
    language: Literal["korean", "english"]

# LMStudio Configuration
class LMStudioConfig:
    base_url: str = "http://localhost:1234/v1"
    api_key: str = "lm-studio"
    timeout: int = 30
    max_retries: int = 3
```

### 3. Repository Interface

```python
class SummaryRepository(ABC):
    async def summarize_text(self, text: str, config: SummaryConfig) -> Summary
    async def health_check(self) -> bool
```

### 4. Use Cases

```python
class SummarizeTextUseCase:
    async def execute(self, request: SummaryRequest) -> SummaryResponse

class HealthCheckUseCase:
    async def execute(self, request: HealthCheckRequest) -> HealthCheckResponse
```

## 🔌 외부 연동

### LMStudio API

```python
# 연결 설정
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="qwen/qwen3-4b",
    max_tokens=1000,
    temperature=0.3
)

# 요약 요청
messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=f"다음 텍스트를 요약해주세요:\n\n{text}")
]
response = await llm.ainvoke(messages)
```

### 프롬프트 엔지니어링

```python
def _get_system_prompt(self, config: SummaryConfig) -> str:
    base_prompt = "당신은 전문적인 텍스트 요약 AI입니다."

    if config.summary_type == "concise":
        return f"{base_prompt} 핵심 내용을 1-2문장으로 간결하게 요약해주세요."
    elif config.summary_type == "detailed":
        return f"{base_prompt} 주요 내용을 상세하게 요약해주세요."
    elif config.summary_type == "bullet_points":
        return f"{base_prompt} 주요 포인트를 불릿 포인트로 정리해주세요."
```

## 📊 데이터 모델

### Request/Response DTOs

```python
# 요약 요청
class SummaryRequest(BaseModel):
    text: str = Field(min_length=10, max_length=50000)
    summary_type: Literal["concise", "detailed", "bullet_points"] = "concise"
    language: Literal["korean", "english"] = "korean"
    max_tokens: int = Field(default=1000, ge=100, le=4000)
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)

# 요약 응답
class SummaryResponse(BaseModel):
    id: str
    original_text: str
    summary_text: str
    created_at: datetime
    model_name: str
    summary_length: int
    original_length: int
    compression_ratio: float
```

### 에러 모델

```python
class ErrorResponse(BaseModel):
    error: str
    error_code: str
    timestamp: datetime
    details: Optional[str] = None
```

## 🔒 보안 및 검증

### 입력 검증

- **텍스트 길이**: 10-50,000자
- **파라미터 범위**: max_tokens(100-4000), temperature(0.0-2.0)
- **허용된 값**: summary_type, language enum 검증
- **XSS 방지**: HTML 태그 제거/이스케이프

### 에러 처리

```python
try:
    summary = await self.summary_service.summarize_text(text, config)
    return SummaryResponse.from_domain_entity(summary)
except ValueError as e:
    raise HTTPException(400, detail=ErrorResponse(...))
except RuntimeError as e:
    raise HTTPException(500, detail=ErrorResponse(...))
except Exception as e:
    raise HTTPException(500, detail=ErrorResponse(...))
```

## 🐳 컨테이너화

### Dockerfile 특징

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# uv를 사용한 빠른 의존성 설치
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

# 보안: non-root 사용자
RUN useradd --create-home --shell /bin/bash app
USER app

# 헬스체크
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -f http://localhost:8000/api/v1/summary/health
```

### 멀티플랫폼 지원

- **linux/amd64**: Intel/AMD 서버
- **linux/arm64**: Apple Silicon, ARM 서버

## ☸️ Kubernetes 배포

### Helm Chart 구조

```
charts/llmplan/
├── Chart.yaml          # 차트 메타데이터
├── values.yaml         # 기본값 설정
└── templates/
    ├── deployment.yaml  # Pod 배포
    ├── service.yaml     # 서비스 노출
    ├── configmap.yaml   # 환경 설정
    ├── ingress.yaml     # 외부 접근 (선택)
    ├── hpa.yaml         # 자동 스케일링 (선택)
    └── lmstudio-service.yaml  # LMStudio 연동
```

### 리소스 요구사항

```yaml
resources:
  requests:
    cpu: 500m # 0.5 CPU 코어
    memory: 512Mi # 512MB RAM
  limits:
    cpu: 1000m # 1 CPU 코어
    memory: 1Gi # 1GB RAM
```

### 스케일링 설정

```yaml
autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

## 🧪 테스트 전략

### 테스트 피라미드

```
        E2E Tests (Manual)
      ┌─────────────────┐
     Integration Tests (3)
   ┌─────────────────────────┐
  Unit Tests (33) - CI Safe
┌─────────────────────────────────┐
```

### CI-Safe 테스트 (36개)

- **Domain Logic**: 비즈니스 규칙 검증
- **Value Objects**: 설정 검증
- **DTOs**: 직렬화/역직렬화
- **Mocked Integration**: LMStudio 모킹

### 테스트 실행 환경

- **Local**: 모든 테스트 (실제 LMStudio 필요)
- **CI**: CI-Safe 테스트만 (모킹 사용)
- **Docker**: 컨테이너 내 테스트

## 🔄 개발 워크플로우

### 로컬 개발

```bash
# 환경 설정
uv sync
source .venv/bin/activate

# LMStudio 시작 (별도)
# Qwen 3-4B 모델 로드

# 개발 서버 실행
uv run uvicorn app.main:app --reload

# 테스트
uv run pytest
```

### 배포 워크플로우

```
Code Push → CI Tests → Docker Build → Docker Push → Helm Package → OCI Push
```

### 브랜치 전략

- **main**: 프로덕션 준비 코드
- **feature/\***: 기능 개발
- **hotfix/\***: 긴급 수정

## 📝 코딩 컨벤션

### Python 스타일

- **Formatter**: Ruff
- **Line Length**: 120자
- **Import Order**: isort 규칙
- **Type Hints**: 모든 함수/메서드

### 네이밍 컨벤션

- **Classes**: PascalCase (`SummaryService`)
- **Functions**: snake_case (`summarize_text`)
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_MODEL_NAME`)
- **Files**: snake_case (`summary_service.py`)

### 문서화

- **Docstrings**: Google 스타일
- **Type Hints**: 모든 public 인터페이스
- **API Docs**: FastAPI 자동 생성 (/docs)

## 🚨 트러블슈팅

### 일반적인 문제들

#### 1. LMStudio 연결 실패

```bash
# 증상: HTTP 503, "LMStudio service is not responding"
# 해결: LMStudio 서버 상태 확인
curl http://localhost:1234/v1/models
```

#### 2. 요약 품질 문제

```bash
# 증상: 이상한 요약 결과
# 해결: temperature, max_tokens 조정
# temperature: 0.1-0.7 (낮을수록 일관성 높음)
# max_tokens: 500-2000 (길수록 상세함)
```

#### 3. 메모리 부족

```bash
# 증상: OOM Killed
# 해결: Kubernetes 리소스 증가
helm upgrade llmplan oci://registry-1.docker.io/eunheejo/llmplan \
  --set resources.limits.memory=2Gi
```

### 디버깅 도구

```bash
# 로그 확인
kubectl logs -f deployment/llmplan -n llmplan

# 헬스체크
curl http://localhost:8000/api/v1/summary/health

# 메트릭 (향후)
curl http://localhost:8000/metrics
```
