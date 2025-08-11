# llmplan

## Author

- **eun2ce** - joeun2ce@gmail.com
- **Start Date**: 2025-08-11

## Architecture

This project follows Domain-Driven Design (DDD) principles with a clean architecture approach.

## Getting Started

### 1. Installation

```bash
# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### 2. Setup LMStudio

1. Install and run LMStudio
2. Load the `qwen/qwen3-4b` model
3. Start the server on port 1234 (default)

### 3. Run the Service

```bash
# With uv (recommended)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API

**Health Check:**

```bash
curl -X GET "http://localhost:8000/api/v1/summary/health"
```

**Response:**

```json
{
  "status": "healthy",
  "service_name": "Text Summarization Service",
  "timestamp": "2025-08-11T10:32:03.546194",
  "details": "LMStudio service is responding correctly"
}
```

**Text Summarization:**

```bash
curl -X POST "http://localhost:8000/api/v1/summary/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "「2025년도 제1차 지역사회 환경정비 계획 수립에 관한 보고서」\n\nⅠ. 추진 배경\n최근 3년간 우리 시의 생활환경 관련 민원이 지속적으로 증가하고 있으며, 특히 쓰레기 불법투기, 무단 방치 차량, 공공시설 훼손 등의 사례가 빈번히 보고되고 있습니다. 이에 따라 시민 생활환경 개선과 도시 미관 회복을 위해 2025년도 제1차 지역사회 환경정비 계획을 수립하게 되었습니다.\n\nⅡ. 주요 추진 과제\n생활쓰레기 관리 강화: 무단투기 단속 전담반 확대 편성(기존 5개조 → 8개조), 상습 투기지역에 CCTV 20대 추가 설치, 재활용품 분리배출 안내 캠페인 분기별 시행.\n방치 차량 및 불법 주정차 해소: 장기 방치 차량 데이터베이스 구축 및 월별 정비 계획 수립, 불법 주정차 단속 차량(이동형 카메라) 3대 추가 도입.\n\nⅢ. 기대 효과\n본 계획을 통해 생활환경 민원 건수를 전년 대비 30% 이상 감소시키고, 방치 차량 및 불법 주정차 건수를 40% 이상 줄일 수 있을 것으로 기대됩니다.",
    "summary_type": "concise",
    "language": "korean",
    "max_tokens": 300
  }'
```

**Response:**

```json
{
  "id": "af084aab-fae7-473c-98db-cb398ff7c427",
  "original_text": "「2025년도 제1차 지역사회 환경정비 계획 수립에 관한 보고서」\n\nⅠ. 추진 배경\n최근 3년간 우리 시의 생활환경 관련 민원이 지속적으로 증가하고 있으며...",
  "summary_text": "**2025년도 제1차 지역사회 환경정비 계획 요약**\n\n**추진 배경**: 최근 3년간 생활환경 민원(쓰레기 불법투기, 무단 방치 차량 등)이 증가하여 시민 생활환경 개선과 도시 미관 회복을 위한 환경정비 계획을 수립함.\n\n**주요 추진 과제**:\n- 생활쓰레기 관리 강화: 단속 전담반 확대(5개조→8개조), CCTV 20대 추가 설치, 분기별 재활용품 분리배출 캠페인\n- 방치 차량 해소: 장기 방치 차량 데이터베이스 구축, 이동형 카메라 3대 도입\n\n**기대 효과**: 생활환경 민원 30% 이상 감소, 방치 차량 및 불법 주정차 40% 이상 감소 예상",
  "created_at": "2025-08-11T10:32:28.410194",
  "model_name": "qwen/qwen3-4b",
  "summary_length": 284,
  "original_length": 658,
  "compression_ratio": 0.432
}
```

### 5. API Parameters

| Parameter      | Type   | Default   | Description                                   |
| -------------- | ------ | --------- | --------------------------------------------- |
| `text`         | string | -         | Text to summarize (10-50,000 chars)           |
| `max_tokens`   | int    | 1000      | Maximum tokens (50-4000)                      |
| `temperature`  | float  | 0.3       | Generation temperature (0.0-2.0)              |
| `summary_type` | string | "concise" | Style: `concise`, `detailed`, `bullet_points` |
| `language`     | string | "korean"  | Language: `korean`, `english`, `japanese`     |

## Deployment

### 🐳 Docker Deployment

See [docker/README.md](docker/README.md) for detailed Docker deployment instructions.

**Quick Start:**

```bash
# Using Docker Hub image
docker run -d -p 8000:8000 \
  -e LMSTUDIO_BASE_URL=http://host.docker.internal:1234/v1 \
  --add-host host.docker.internal:host-gateway \
  eunheejo/llmplan:latest

# Using Docker Compose
cd docker/ && docker-compose up -d
```

### ⚓ Kubernetes Deployment

#### Using Helm Chart (Recommended)

```bash
# Install from OCI registry
helm install llmplan oci://registry-1.docker.io/eunheejo/llmplan --namespace llmplan --create-namespace

# Or with custom values
helm install llmplan oci://registry-1.docker.io/eunheejo/llmplan \
  --namespace llmplan --create-namespace \
  --set lmstudio.externalName=my-lmstudio-host.local
```

#### Using Kubernetes Manifests

```bash
# Apply manifests directly
kubectl apply -f k8s/manifests/

# Port forward for testing
kubectl port-forward svc/llmplan 8000:8000 -n llmplan
```

**📚 Detailed Instructions:**

- **Helm Charts**: See [charts/README.md](charts/README.md)
- **Kubernetes Manifests**: See [k8s/README.md](k8s/README.md)
- **Docker**: See [docker/README.md](docker/README.md)

## Project Structure

```
llmplan/
├── src/app/                 # Application source code
│   ├── application/         # Application layer (DTOs, Use Cases)
│   ├── domain/             # Domain layer (Entities, Services)
│   ├── infrastructure/     # Infrastructure layer (Repositories)
│   ├── presentation/       # Presentation layer (API Routes)
│   └── config/             # Configuration and DI container
├── docker/                 # Docker deployment files
│   ├── docker-compose.yml  # Docker Compose configuration
│   ├── nginx.conf          # Nginx reverse proxy config
│   └── README.md           # Docker deployment guide
├── charts/                 # Helm charts
│   └── llmplan/            # Main Helm chart
│       ├── Chart.yaml      # Chart metadata
│       ├── values.yaml     # Default values
│       └── templates/      # Kubernetes templates
├── k8s/                    # Raw Kubernetes manifests
│   ├── manifests/          # YAML manifests
│   └── README.md           # K8s deployment guide
├── .github/workflows/      # CI/CD pipelines
│   ├── ci.yml              # Continuous integration
│   ├── docker-publish.yml  # Docker image publishing
│   └── helm-release.yml    # Helm chart releasing
├── Dockerfile              # Docker image definition
└── README.md               # This file
```

## CI/CD Pipeline

The project includes automated CI/CD pipelines:

1. **🔄 CI Pipeline** (`ci.yml`): Code testing and validation
2. **🐳 Docker Publishing** (`docker-publish.yml`): Builds and pushes to Docker Hub
3. **📦 Helm Releasing** (`helm-release.yml`): Packages and publishes Helm charts

### Automated Releases

- **Docker Images**: Pushed to `eunheejo/llmplan` on Docker Hub
- **Helm Charts**: Published to GitHub Pages and OCI registry
- **Versioning**: Automatic tagging and versioning
