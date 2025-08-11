# llm text summary api

## getting started

```bash
// local
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

// docker
docker run -d -p 8000:8000 -e LMSTUDIO_BASE_URL=http://host.docker.internal:1234/v1 --add-host host.docker.internal:host-gateway eunheejo/llmplan:latest

// helm
helm install llmplan oci://registry-1.docker.io/eunheejo/llmplan --namespace llmplan --create-namespace

// test
uv run pytest
```

## layer

```bash
llmplan/
├── src/app/                 # 애플리케이션 소스코드
│   ├── domain/             # 도메인 레이어 (엔티티, 서비스)
│   ├── application/        # 애플리케이션 레이어 (유스케이스, DTO)
│   ├── infrastructure/     # 인프라 레이어 (LMStudio 연동)
│   ├── presentation/       # 프레젠테이션 레이어 (API 라우터)
│   └── config/             # 설정 및 DI 컨테이너
├── tests/                  # 테스트 코드
├── charts/llmplan/         # Helm 차트
├── .github/workflows/      # CI/CD 파이프라인
└── .github/prd/           # 서비스 컨텍스트 문서
```
