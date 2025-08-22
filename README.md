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
